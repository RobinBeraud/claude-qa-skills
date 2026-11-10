"""Unit tests for the bundled scripts. Stdlib only:  python -m unittest discover -s tests -v

Git-based scripts are tested against a throw-away repository built in a temporary folder.
"""
import contextlib
import datetime as dt
import importlib.util
import io
import json
import os
import shutil
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "examples")
HAS_GIT = shutil.which("git") is not None


def load(plugin, skill, script):
    path = os.path.join(ROOT, "plugins", plugin, "skills", skill, "scripts", script + ".py")
    spec = importlib.util.spec_from_file_location(script, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def quiet(fn, *args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
        code = fn(*args)
    return code, buf.getvalue()


pr_size = load("dev-workflow", "small-pull-requests", "pr_size")
csproj = load("dev-dotnet", "dotnet-solution-inventory", "csproj_scan")
hotspots = load("dev-legacy", "codebase-hotspots", "hotspots")
backport = load("dev-legacy", "release-backports", "backport_check")
changelog = load("dev-delivery", "conventional-commits", "changelog")
stale = load("dev-delivery", "stale-pr-triage", "stale_prs")
secrets = load("dev-security", "secrets-hygiene", "secret_scan")


class Repo:
    """A tiny git repository with a main branch, a release branch and a feature branch."""

    def __init__(self):
        self.dir = tempfile.mkdtemp(prefix="devskills-")
        self.env = dict(os.environ, GIT_AUTHOR_NAME="Ada", GIT_AUTHOR_EMAIL="ada@example.com",
                        GIT_COMMITTER_NAME="Ada", GIT_COMMITTER_EMAIL="ada@example.com")
        self.git("init", "-q", "-b", "main")
        self.git("config", "commit.gpgsign", "false")

    def git(self, *args, env=None):
        return subprocess.run(["git", "-C", self.dir] + list(args), capture_output=True, text=True, check=True,
                              env=env or self.env).stdout

    def write(self, rel, text):
        p = os.path.join(self.dir, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    def commit(self, msg, author="Ada", date="2026-03-01T10:00:00"):
        self.git("add", "-A")
        env = dict(self.env, GIT_AUTHOR_NAME=author, GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
        self.git("commit", "-q", "-m", msg, env=env)
        return self.git("rev-parse", "HEAD").strip()

    def close(self):
        shutil.rmtree(self.dir, ignore_errors=True)


@unittest.skipUnless(HAS_GIT, "git not installed")
class GitScripts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        r = cls.r = Repo()
        r.write("src/Billing/Invoice.cs", "class Invoice {}\n" * 50)
        r.write("src/Billing/Vat.cs", "class Vat {}\n" * 10)
        r.write("README.md", "hello\n")
        r.commit("feat(billing): add invoice model AB#100", date="2026-01-05T10:00:00")
        r.git("branch", "release/1.0")
        for i in range(4):  # Invoice.cs and Vat.cs always change together
            # each fix adds a distinct line, so patch-ids differ between fixes
            r.write("src/Billing/Invoice.cs", "class Invoice {}\n" * 50 + "".join("// fix %d\n" % k for k in range(i + 1)))
            r.write("src/Billing/Vat.cs", "class Vat {}\n" * 10 + "".join("// vat fix %d\n" % k for k in range(i + 1)))
            r.commit("fix(billing): rounding step %d AB#20%d" % (i, i), author="Bob" if i % 2 else "Ada", date="2026-02-0%dT10:00:00" % (i + 1))
        cls.fix_sha = r.git("rev-parse", "HEAD").strip()
        # backport only the first fix to the release branch, cleanly, and the last one with a conflict-free but different patch
        r.git("checkout", "-q", "release/1.0")
        first = r.git("rev-list", "--reverse", "main").split()[1]
        r.git("cherry-pick", "-x", first)
        r.write("src/Billing/Vat.cs", "class Vat { /* manual backport */ }\n")
        r.commit("fix(billing): rounding step 3 (manual backport) AB#203", date="2026-02-10T10:00:00")
        r.git("checkout", "-q", "main")
        r.git("checkout", "-q", "-b", "feature/big")
        r.write("src/Billing/Dunning.cs", "line\n" * 450)
        r.write("package-lock.json", "{}\n" * 3000)
        r.write("src/Web/app.ts", "let a = 1;\n" * 40)
        r.commit("add dunning letters.", date="2026-03-01T10:00:00")
        r.git("checkout", "-q", "main")

    @classmethod
    def tearDownClass(cls):
        cls.r.close()

    def test_pr_size_counts_generated_apart(self):
        res = pr_size.analyse(pr_size.git_numstat(self.r.dir, "main", "feature/big"), budget=400)
        self.assertEqual(res["changed_lines"], 490)
        self.assertEqual(res["generated_lines"], 3000)
        self.assertEqual(res["verdict"], "large")
        self.assertIn("src/Billing", res["areas"])

    def test_hotspots_and_coupling(self):
        log = hotspots.git_log(self.r.dir, "2025-01-01", None)
        commits = hotspots.parse_log(log, hotspots.DEFAULT_EXCLUDE)
        res = hotspots.compute(commits, hotspots.count_lines(self.r.dir, {f for c in commits for f in c["files"]}))
        top = res["hotspots"][0]
        self.assertEqual(top["path"], "src/Billing/Invoice.cs")
        self.assertEqual(top["authors"], 2)
        self.assertNotIn("README.md", [h["path"] for h in res["hotspots"]])  # *.md excluded
        pair = res["coupling"][0]
        self.assertEqual({pair["a"], pair["b"]}, {"src/Billing/Invoice.cs", "src/Billing/Vat.cs"})
        self.assertFalse(pair["cross_module"])

    def test_backport_statuses(self):
        rows = backport.check(self.r.dir, "main", "release/1.0")
        status = {r["subject"]: r["status"] for r in rows}
        self.assertNotIn("fix(billing): rounding step 0 AB#200", status)          # clean cherry-pick: filtered by git cherry
        self.assertEqual(status["fix(billing): rounding step 1 AB#201"], "MISSING")
        self.assertTrue(status["fix(billing): rounding step 3 AB#203"].startswith("probably backported"))

    def test_changelog_lint_and_notes(self):
        rows = changelog.log(self.r.dir, "main..feature/big")
        self.assertEqual(len(rows), 1)
        self.assertTrue(changelog.lint_subject(rows[0][1]))
        groups = dict(changelog.notes(changelog.log(self.r.dir, "release/1.0..main")))
        self.assertIn("fix", groups)
        self.assertIn("AB#201", groups["fix"][0]["refs"] + groups["fix"][1]["refs"] + groups["fix"][2]["refs"])

    def test_secret_scan_staged(self):
        key = "AKIA" + "ABCDEFGHIJKLMNOP"
        self.r.write("appsettings.json", '{"Storage": "x", "AwsKey": "%s"}\n' % key)
        self.r.git("add", "appsettings.json")
        cwd = os.getcwd()
        try:
            os.chdir(self.r.dir)
            code, out = quiet(secrets.main, ["--staged"])
        finally:
            os.chdir(cwd)
            self.r.git("reset", "-q", "appsettings.json")
            os.remove(os.path.join(self.r.dir, "appsettings.json"))
        self.assertEqual(code, 1)
        self.assertIn("aws_access_key", out)
        self.assertNotIn(key, out)


class Pure(unittest.TestCase):
    def test_changelog_parse(self):
        p = changelog.parse("Merged PR 812: feat(api)!: drop v1 endpoints", "")
        self.assertTrue(p["ok"] and p["breaking"])
        self.assertEqual((p["type"], p["scope"]), ("feat", "api"))
        self.assertIn("PR 812", p["refs"])
        self.assertEqual(changelog.lint_subject("fix(billing): round VAT per line AB#12"), [])
        self.assertTrue(changelog.lint_subject("Fixed stuff."))
        self.assertEqual(changelog.lint_subject("Merge branch 'main' into feature/x"), [])

    def test_pr_size_rename_and_binary(self):
        res = pr_size.analyse("10\t2\tsrc/{Old => New}/A.cs\n-\t-\tdocs/logo.png\n5\t0\tsrc/App/Form.Designer.cs\n")
        self.assertEqual(res["changed_lines"], 12)
        self.assertEqual(res["binary_files"], 1)
        self.assertEqual(res["generated_lines"], 5)
        self.assertEqual(res["largest"][0]["path"], "src/New/A.cs")

    def test_csproj_inventory(self):
        r = csproj.scan(os.path.join(EX, "dotnet-sample"))
        names = {p["name"]: p for p in r["projects"]}
        self.assertEqual(len(names), 4)
        self.assertFalse(names["Legacy.Core"]["sdk_style"])
        self.assertEqual(names["Legacy.Core"]["tfms"], ["net472"])
        self.assertTrue(names["Legacy.Core"]["packages_config"])
        self.assertEqual(names["Billing.Tests"]["tfms"], ["net10.0", "net8.0"])
        self.assertIn("Newtonsoft.Json", r["drift"])
        self.assertIn("Serilog.AspNetCore", r["drift"])  # 8.0.1 from a child <Version> element vs 9.0.0
        order = r["migration_order"]
        self.assertLess(order.index("Billing.Domain"), order.index("Billing.Api"))
        self.assertLess(order.index("Billing.Api"), order.index("Billing.Tests"))
        self.assertEqual(csproj.classify("net8.0")[1], "end of support 2026-11-10")
        self.assertEqual(csproj.classify("net10.0-windows")[0], ".NET")
        self.assertEqual(csproj.classify("net452")[1], "out of support")

    def test_stale_prs_all_formats(self):
        as_of = dt.datetime(2026, 11, 10)
        for name, n in (("prs_azure_devops.json", 3), ("prs_github.json", 2), ("prs_gitlab.json", 1)):
            with open(os.path.join(EX, name), encoding="utf-8") as f:
                prs = stale.normalise(json.load(f))
            self.assertEqual(len(prs), n, name)
            rep = stale.report(prs, as_of, 30)
            self.assertEqual(rep["open"], n)
        with open(os.path.join(EX, "prs_azure_devops.json"), encoding="utf-8") as f:
            az = stale.report(stale.normalise(json.load(f)), as_of)
        self.assertEqual(dict(az["buckets"])["> 1 year"], 1)
        self.assertEqual(dict(az["by_reviewer"]), {"Hugo Dubois": 2})  # group reviewers ignored
        with open(os.path.join(EX, "prs_github.json"), encoding="utf-8") as f:
            gh = stale.report(stale.normalise(json.load(f)), as_of, 30)
        self.assertEqual([p["id"] for p in gh["idle"]], [61])

    def test_secret_rules(self):
        k = lambda line: [f["kind"] for f in secrets.scan_line(line)]
        self.assertEqual(k('"ConnectionStrings": "Server=db;User Id=app;Password=S3cr3t!x;"'), ["connection_string_password"])  # secret-scan: ignore
        self.assertEqual(k("Password=${DB_PASSWORD};"), [])
        self.assertEqual(k('client_secret: "<your-secret>"'), [])
        self.assertEqual(k('"ClientSecret": "q8Z~a1b2c3d4e5f6g7h8"'), ["assignment"])  # secret-scan: ignore
        self.assertIn("github_token", k("token=" + "ghp_" + "A" * 36))
        diff = "+++ b/a.env\n@@ -0,0 +3,2 @@\n+NAME=x\n+API_KEY='abcdefgh12345678'\n"  # secret-scan: ignore
        found = secrets.scan_diff(diff)
        self.assertEqual([(f["file"], f["line"]) for f in found], [("a.env", 4)])
        self.assertEqual(secrets.scan_text("password = 'abcdefgh12345678'  # secret-scan: ignore", "x"), [])
        self.assertTrue(secrets.scan_text("password = 'abcdefgh12345678'", "x"))  # secret-scan: ignore


if __name__ == "__main__":
    unittest.main()
