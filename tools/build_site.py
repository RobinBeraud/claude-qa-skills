#!/usr/bin/env python3
"""Build docs/index.html, the GitHub Pages landing page, from marketplace.json and every SKILL.md.

Run after adding or editing skills:  python tools/build_site.py
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "RobinBeraud/claude-qa-skills"
META = {
    "qa-test-strategy": ("🗺️", "#FF7A00", "Strategy"),
    "qa-shift-left": ("🧭", "#FFC400", "Design"),
    "qa-unit-testing": ("🧪", "#2F6BFF", "Unit"),
    "qa-mutation-testing": ("🧬", "#7B61FF", "Mutation"),
    "qa-automation": ("🤖", "#16B3A6", "Automation"),
    "qa-explore-and-report": ("🔎", "#F2448B", "Explore"),
    "qa-ci-insights": ("📈", "#22C55E", "CI"),
    "qa-release": ("🚀", "#F97316", "Release"),
    "dora-metrics": ("📊", "#06B6D4", "DORA"),
    "evidence-based-management": ("🎯", "#EAB308", "EBM"),
    "qa-ai-era": ("🧠", "#A855F7", "AI era"),
    "qa-business-apps": ("🏦", "#EF4444", "Business apps"),
}


def front(path):
    text = open(path, encoding="utf-8").read()
    m = re.search(r"^description:\s*(.*)$", text, re.M)
    v = m.group(1).strip()
    desc = json.loads(v) if v.startswith('"') else v
    title = re.search(r"^# (.+)$", text, re.M)
    return desc, title.group(1).strip() if title else None


def data():
    mp = json.load(open(os.path.join(ROOT, ".claude-plugin", "marketplace.json"), encoding="utf-8"))
    plugins, scripts = [], 0
    for e in mp["plugins"]:
        base = os.path.join(ROOT, e["source"])
        pj = json.load(open(os.path.join(base, ".claude-plugin", "plugin.json"), encoding="utf-8"))
        skills = []
        for s in sorted(os.listdir(os.path.join(base, "skills"))):
            sd = os.path.join(base, "skills", s)
            desc, title = front(os.path.join(sd, "SKILL.md"))
            has = os.path.isdir(os.path.join(sd, "scripts"))
            scripts += len([f for f in os.listdir(os.path.join(sd, "scripts")) if f.endswith(".py")]) if has else 0
            what = re.split(r"(?<=[.])\s+Use ", desc, maxsplit=1)
            skills.append({"name": s, "title": title or s, "what": what[0], "when": ("Use " + what[1]) if len(what) > 1 else "",
                           "script": has, "url": "https://github.com/%s/blob/main/%s" % (REPO, os.path.relpath(os.path.join(sd, "SKILL.md"), ROOT).replace(os.sep, "/"))})
        icon, color, short = META.get(e["name"], ("✨", "#2F6BFF", e["name"]))
        plugins.append({"name": e["name"], "desc": pj["description"], "icon": icon, "color": color, "short": short,
                        "version": pj.get("version", ""), "skills": skills})
    return mp, plugins, scripts


PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>claude-qa-skills · __NSKILLS__ QA skills for Claude Code</title>
<meta name="description" content="__NSKILLS__ quality-engineering skills for Claude Code in __NPLUGINS__ installable plugins: test strategy, unit and mutation testing, automation, exploratory testing, CI insights, DORA metrics, Evidence-Based Management, AI-era QA, ERP and e-invoicing.">
<meta property="og:title" content="claude-qa-skills · __NSKILLS__ QA skills for Claude Code">
<meta property="og:description" content="Test strategy, unit and mutation testing, DORA, EBM, AI-era QA and business software, as installable Claude Code plugins.">
<meta property="og:image" content="https://robinberaud.github.io/claude-qa-skills/assets/social-preview.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔎</text></svg>">
<style>
  :root{--bg:#0B1226;--bg2:#111a33;--card:#141f3d;--line:#24335e;--ink:#EAF0FF;--muted:#9BAAD0;--o:#FF7A00;--y:#FFC400;--b:#2F6BFF;--v:#7B61FF;--t:#16B3A6;--p:#F2448B;
        --font:system-ui,-apple-system,'Segoe UI',Roboto,Inter,sans-serif;--mono:ui-monospace,'Cascadia Code',Consolas,Menlo,monospace;}
  *{box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font);line-height:1.55}
  a{color:#9CC0FF}
  .wrap{max-width:1180px;margin:0 auto;padding:0 22px}
  nav{position:sticky;top:0;z-index:10;background:rgba(11,18,38,.82);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
  nav .wrap{display:flex;align-items:center;gap:22px;height:60px}
  nav .brand{font-weight:800;font-size:18px;color:var(--ink);text-decoration:none}
  nav .brand b{color:var(--o)}
  nav .links{display:flex;gap:18px;margin-left:auto;font-size:14px}
  nav .links a{color:var(--muted);text-decoration:none}
  nav .links a:hover{color:var(--ink)}
  .gh{display:inline-flex;align-items:center;gap:8px;background:#fff;color:#0B1226!important;font-weight:700;padding:8px 14px;border-radius:999px;text-decoration:none;font-size:14px}
  header.hero{position:relative;overflow:hidden;border-bottom:1px solid var(--line)}
  header.hero .art{position:absolute;inset:0;background:url(assets/hero.jpg) right center/auto 100% no-repeat;opacity:.95}
  header.hero .shade{position:absolute;inset:0;background:linear-gradient(90deg,var(--bg) 40%,rgba(11,18,38,.82) 56%,rgba(11,18,38,.15) 78%,rgba(11,18,38,0) 90%)}
  header.hero .wrap{position:relative;padding:92px 22px 84px}
  .eyebrow{font-family:var(--mono);font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--y)}
  h1{font-size:clamp(38px,5.4vw,62px);line-height:1.02;margin:14px 0 18px;letter-spacing:-.03em;max-width:600px}
  h1 span{background:linear-gradient(90deg,var(--o),var(--y));-webkit-background-clip:text;background-clip:text;color:transparent}
  .lead{font-size:20px;color:#C9D5F3;max-width:600px;margin:0 0 26px}
  .stats{display:flex;flex-wrap:wrap;gap:12px;margin:0 0 30px}
  .stat{background:rgba(20,31,61,.85);border:1px solid var(--line);border-radius:14px;padding:10px 16px}
  .stat b{display:block;font-size:24px;line-height:1}
  .stat span{font-size:12px;color:var(--muted)}
  .install{max-width:640px;background:#060b1a;border:1px solid var(--line);border-radius:14px;overflow:hidden}
  .install .tabs{display:flex;border-bottom:1px solid var(--line)}
  .install .tabs button{flex:1;background:none;border:0;color:var(--muted);padding:10px;font:600 13px var(--font);cursor:pointer}
  .install .tabs button.on{color:var(--ink);background:var(--bg2)}
  .cmd{display:flex;align-items:center;gap:10px;padding:10px 14px;font-family:var(--mono);font-size:14px;border-top:1px solid #0f1a36}
  .cmd:first-child{border-top:0}
  .cmd code{flex:1;color:#E2E8F0;white-space:nowrap;overflow-x:auto}
  .cmd code i{color:var(--t);font-style:normal}
  .copy{background:var(--b);color:#fff;border:0;border-radius:8px;padding:5px 10px;font:600 12px var(--font);cursor:pointer}
  .copy.ok{background:var(--t)}
  .pane{display:none}.pane.on{display:block}
  .cta{display:flex;gap:12px;margin-top:22px;flex-wrap:wrap}
  .btn{display:inline-block;padding:12px 20px;border-radius:12px;font-weight:700;text-decoration:none}
  .btn.primary{background:linear-gradient(90deg,var(--o),var(--y));color:#0B1226}
  .btn.ghost{border:1px solid var(--line);color:var(--ink)}
  section{padding:76px 0;border-bottom:1px solid var(--line)}
  h2{font-size:clamp(28px,3.6vw,40px);letter-spacing:-.02em;margin:0 0 10px}
  .sub{color:var(--muted);max-width:720px;margin:0 0 34px;font-size:17px}
  .why{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
  .why div{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px}
  .why h3{margin:10px 0 6px;font-size:18px}
  .why p{margin:0;color:var(--muted);font-size:14.5px}
  .why .e{font-size:28px}
  .demo{display:grid;grid-template-columns:1.25fr 1fr;gap:28px;align-items:center}
  .demo img{width:100%;border-radius:14px;border:1px solid var(--line);box-shadow:0 20px 60px rgba(0,0,0,.45)}
  .demo ol{margin:0;padding-left:20px;color:#C9D5F3}
  .demo li{margin-bottom:12px}
  .toolbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:22px}
  .search{flex:1;min-width:240px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;color:var(--ink);font-size:15px}
  .chip{border:1px solid var(--line);background:var(--card);color:var(--ink);padding:7px 13px;border-radius:999px;font-size:13px;cursor:pointer}
  .chip.on{background:var(--ink);color:#0B1226;border-color:var(--ink)}
  .count{color:var(--muted);font-size:14px;margin-bottom:14px}
  .plugin{background:var(--card);border:1px solid var(--line);border-radius:18px;margin-bottom:18px;overflow:hidden}
  .plugin .ph{display:flex;gap:14px;align-items:flex-start;padding:20px 22px;border-left:6px solid var(--c)}
  .plugin .ph .ic{font-size:30px}
  .plugin .ph h3{margin:0;font-size:20px}
  .plugin .ph p{margin:4px 0 0;color:var(--muted);font-size:14.5px}
  .plugin .ph .inst{margin-left:auto;display:flex;gap:8px;align-items:center;font-family:var(--mono);font-size:12.5px;background:#060b1a;border:1px solid var(--line);border-radius:10px;padding:6px 8px 6px 12px;white-space:nowrap}
  .skills{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line);border-top:1px solid var(--line)}
  .skill{background:var(--bg2);padding:16px 18px;text-decoration:none;color:var(--ink);display:block}
  .skill:hover{background:#18264a}
  .skill b{font-family:var(--mono);font-size:13.5px;color:#fff}
  .skill .py{font-size:11px;background:var(--t);color:#04211e;border-radius:6px;padding:1px 6px;margin-left:6px;font-weight:700}
  .skill p{margin:6px 0 0;font-size:13.5px;color:#B9C6E6}
  .skill small{display:block;margin-top:6px;color:#7F8FB8;font-size:12.5px}
  .roles{width:100%;border-collapse:collapse;background:var(--card);border-radius:16px;overflow:hidden}
  .roles th,.roles td{padding:14px 16px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;font-size:14.5px}
  .roles th{background:var(--bg2);color:var(--muted);font-size:12px;letter-spacing:.1em;text-transform:uppercase}
  .roles code{font-family:var(--mono);font-size:12.5px;background:#060b1a;padding:2px 6px;border-radius:6px;color:var(--y)}
  .steps{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
  .steps div{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px}
  .steps .n{display:inline-flex;width:34px;height:34px;border-radius:10px;align-items:center;justify-content:center;background:var(--o);color:#0B1226;font-weight:800}
  .steps h3{margin:12px 0 6px}
  .steps p{color:var(--muted);margin:0;font-size:14.5px}
  pre{background:#060b1a;border:1px solid var(--line);border-radius:12px;padding:14px 16px;overflow-x:auto;font-family:var(--mono);font-size:13.5px;color:#E2E8F0}
  details{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin-bottom:10px}
  summary{cursor:pointer;font-weight:700}
  details p{color:var(--muted);margin:10px 0 0}
  .star{text-align:center}
  .star h2{margin-bottom:12px}
  footer{padding:36px 0;color:var(--muted);font-size:14px}
  footer .wrap{display:flex;flex-wrap:wrap;gap:12px;justify-content:space-between}
  @media(max-width:900px){.why,.steps{grid-template-columns:1fr 1fr}.skills{grid-template-columns:1fr 1fr}.demo{grid-template-columns:1fr}.plugin .ph{flex-wrap:wrap}.plugin .ph .inst{margin-left:0}header.hero .art{opacity:.25}}
  @media(max-width:600px){.why,.steps,.skills{grid-template-columns:1fr}nav .links a:not(.gh){display:none}}
</style>
</head>
<body>
<nav><div class="wrap"><a class="brand" href="#">claude-<b>qa</b>-skills</a>
  <div class="links"><a href="#catalogue">Catalogue</a><a href="#roles">By role</a><a href="#team">Team setup</a><a href="#faq">FAQ</a>
  <a class="gh" href="https://github.com/__REPO__">★ Star on GitHub</a></div></div></nav>

<header class="hero"><div class="art"></div><div class="shade"></div><div class="wrap">
  <div class="eyebrow">Claude Code plugin marketplace · MIT</div>
  <h1>Quality engineering skills for <span>Claude Code</span></h1>
  <p class="lead">From a fuzzy user story to a go/no-go decision. Test strategy, unit and mutation testing, DORA metrics, Evidence-Based Management, and the checks that matter when coding agents write the code.</p>
  <div class="stats">
    <div class="stat"><b>__NSKILLS__</b><span>skills</span></div><div class="stat"><b>__NPLUGINS__</b><span>plugins</span></div>
    <div class="stat"><b>__NSCRIPTS__</b><span>tested scripts</span></div><div class="stat"><b>0</b><span>dependencies</span></div>
  </div>
  <div class="install">
    <div class="tabs"><button class="on" data-pane="p1">In Claude Code</button><button data-pane="p2">From a shell</button><button data-pane="p3">Whole team</button></div>
    <div class="pane on" id="p1">
      <div class="cmd"><code><i>/plugin</i> marketplace add __REPO__</code><button class="copy">Copy</button></div>
      <div class="cmd"><code><i>/plugin</i> install qa-test-strategy@claude-qa-skills</code><button class="copy">Copy</button></div>
    </div>
    <div class="pane" id="p2">
      <div class="cmd"><code><i>claude</i> plugin marketplace add __REPO__</code><button class="copy">Copy</button></div>
      <div class="cmd"><code><i>claude</i> plugin install qa-unit-testing@claude-qa-skills</code><button class="copy">Copy</button></div>
    </div>
    <div class="pane" id="p3">
      <div class="cmd"><code><i>claude</i> plugin marketplace add __REPO__ --scope project</code><button class="copy">Copy</button></div>
      <div class="cmd"><code><i>claude</i> plugin install qa-ai-era@claude-qa-skills --scope project</code><button class="copy">Copy</button></div>
    </div>
  </div>
  <div class="cta"><a class="btn primary" href="#catalogue">Browse the __NSKILLS__ skills</a><a class="btn ghost" href="https://github.com/__REPO__/blob/main/docs/GETTING_STARTED.md">Getting started</a><a class="btn ghost" href="https://github.com/__REPO__/blob/main/docs/GUIDE_FR.md">Guide en français</a></div>
</div></header>

<section><div class="wrap">
  <h2>Coding agents made writing code cheap. Verification is the new bottleneck.</h2>
  <p class="sub">These skills make checking faster and harder to fake: they push Claude to plan before editing, write tests that can fail, show evidence before "done", and measure delivery rather than activity.</p>
  <div class="why">
    <div><span class="e">🎓</span><h3>Real testing craft</h3><p>SFDIPOT and tours, FEW HICCUPPS oracles, RIMGEA bug advocacy, example mapping, decision tables, pairwise, property-based and mutation testing.</p></div>
    <div><span class="e">🧠</span><h3>Built for the agent era</h3><p>Review AI-generated PRs, tests first for agents, evidence before done, audit AI-written tests, evaluate and red-team LLM features.</p></div>
    <div><span class="e">📊</span><h3>Measure what matters</h3><p>The five DORA metrics, Evidence-Based Management, quality flow metrics: scripts plus the facilitation to turn numbers into decisions.</p></div>
    <div><span class="e">🏦</span><h3>Business software</h3><p>Accounting invariants, EN 16931 / Factur-X checks, rounding, DST, multi-tenant isolation, RBAC, migrations, FR/ES/PT localisation.</p></div>
  </div>
</div></section>

<section><div class="wrap demo">
  <img src="assets/demo.gif" alt="Terminal demo: identifier validation, e-invoice check, flaky tests and permissions diff">
  <div><h2>Tools that run anywhere</h2><p class="sub">__NSCRIPTS__ bundled scripts, Python standard library only, each covered by unit tests. Skills call them for you; you can also run them yourself.</p>
  <ol><li>Fake but valid SIREN, VAT and IBAN for test data</li><li>EN 16931 arithmetic of CII / Factur-X invoices</li><li>Flaky tests across CI runs, JUnit digests, regression scope from git history</li><li>DORA metrics, EBM scorecard, QA flow metrics, test pyramid scan, mutation report digest</li></ol></div>
</div></section>

<section id="catalogue"><div class="wrap">
  <h2>The catalogue</h2>
  <p class="sub">Install a whole plugin, then just ask. Claude loads the right skill from your request, or call one explicitly with <code style="font-family:var(--mono)">/plugin:skill</code>.</p>
  <div class="toolbar"><input class="search" id="q" placeholder="Search skills: mutation, DORA, flaky, Gherkin, invoice…" aria-label="Search skills"></div>
  <div class="toolbar" id="chips"></div>
  <div class="count" id="count"></div>
  <div id="plugins"></div>
</div></section>

<section id="roles"><div class="wrap">
  <h2>Start with your role</h2>
  <p class="sub">Three plugins each, then ask in your own words. Claude answers in your language.</p>
  <table class="roles">
    <tr><th>You are</th><th>Install</th><th>Try asking</th></tr>
    <tr><td>QA engineer / tester</td><td><code>qa-shift-left</code> <code>qa-explore-and-report</code> <code>qa-automation</code></td><td>"Review the testability of this story" · "Write exploratory charters for the payment screen"</td></tr>
    <tr><td>Developer</td><td><code>qa-unit-testing</code> <code>qa-mutation-testing</code> <code>qa-ai-era</code></td><td>"Write unit tests for invoice.py" · "Review this AI-generated PR against the ticket"</td></tr>
    <tr><td>Tech lead / QA lead</td><td><code>qa-test-strategy</code> <code>qa-ci-insights</code> <code>qa-release</code></td><td>"Write our one-page test strategy" · "Which tests are flaky in these JUnit reports?"</td></tr>
    <tr><td>Agile coach / manager / PO</td><td><code>dora-metrics</code> <code>evidence-based-management</code> <code>qa-test-strategy</code></td><td>"Compute our DORA metrics from this export" · "Define EBM goals and key value measures"</td></tr>
    <tr><td>ERP / finance / SaaS team</td><td><code>qa-business-apps</code></td><td>"Check this Factur-X invoice" · "Generate permission tests from this roles matrix"</td></tr>
  </table>
</div></section>

<section id="team"><div class="wrap">
  <h2>Roll it out to your team</h2>
  <div class="steps">
    <div><span class="n">1</span><h3>Declare it in the repo</h3><p>Run once in your project and commit <code style="font-family:var(--mono)">.claude/settings.json</code>.</p><pre>claude plugin marketplace add __REPO__ --scope project
claude plugin install qa-ai-era@claude-qa-skills --scope project</pre></div>
    <div><span class="n">2</span><h3>Teammates open the project</h3><p>Claude Code registers the marketplace and the plugins for everyone who trusts the folder. Nothing else to install.</p></div>
    <div><span class="n">3</span><h3>Stay current</h3><p>Enable auto-update in <code style="font-family:var(--mono)">/plugin</code> &gt; Marketplaces, or run <code style="font-family:var(--mono)">/plugin marketplace update claude-qa-skills</code>.</p></div>
  </div>
</div></section>

<section id="faq"><div class="wrap">
  <h2>FAQ</h2>
  <details><summary>What is a skill?</summary><p>A folder with a SKILL.md: a description Claude uses to decide when to load it, and instructions it follows (steps, output format, pitfalls), sometimes with a script. Skills only load when relevant, so installing many costs little context.</p></details>
  <details><summary>Do I need Python?</summary><p>Only for the bundled scripts (Python 3.9+, standard library only). All skills work without them.</p></details>
  <details><summary>Does it work in French, Spanish, Portuguese…?</summary><p>Yes. Skills are written in English but tell Claude to answer in your language. Some skills target French business rules (SIREN/SIRET, Factur-X, RGAA).</p></details>
  <details><summary>Can I use only one skill without the plugin system?</summary><p>Copy any <code style="font-family:var(--mono)">plugins/&lt;plugin&gt;/skills/&lt;skill&gt;/</code> folder into <code style="font-family:var(--mono)">~/.claude/skills/</code> or your repo's <code style="font-family:var(--mono)">.claude/skills/</code>.</p></details>
  <details><summary>How do I contribute?</summary><p>Open an issue with your idea, or a pull request following CONTRIBUTING.md. Every skill is validated in CI and every script has a test.</p></details>
</div></section>

<section class="star"><div class="wrap">
  <h2>Useful? Give it a ⭐</h2>
  <p class="sub" style="margin:0 auto 22px">Stars help other testers and developers find these skills. New skills land regularly.</p>
  <a class="btn primary" href="https://github.com/__REPO__">★ Star claude-qa-skills on GitHub</a>
</div></section>

<footer><div class="wrap"><span>Made by <a href="https://coach-agile.com">Robin Béraud-Sudreau</a> · author of <i>Build Your Own AI Workforce</i> · sister project <a href="https://github.com/RobinBeraud/hermes-skills">hermes-skills</a></span><span>MIT licence · not affiliated with Anthropic</span></div></footer>

<script id="data" type="application/json">__DATA__</script>
<script>
(function(){
  var P = JSON.parse(document.getElementById('data').textContent), q = document.getElementById('q'), active = 'all';
  function esc(s){ return s.replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  var chips = document.getElementById('chips');
  chips.innerHTML = '<button class="chip on" data-p="all">All</button>' + P.map(function(p){ return '<button class="chip" data-p="'+p.name+'">'+p.icon+' '+esc(p.short)+'</button>'; }).join('');
  chips.addEventListener('click', function(e){ var b = e.target.closest('.chip'); if(!b) return; active = b.dataset.p;
    chips.querySelectorAll('.chip').forEach(function(c){ c.classList.toggle('on', c===b); }); render(); });
  q.addEventListener('input', render);
  function render(){
    var term = q.value.trim().toLowerCase(), total = 0, out = '';
    P.forEach(function(p){
      if(active !== 'all' && active !== p.name) return;
      var sk = p.skills.filter(function(s){ return !term || (s.name+' '+s.what+' '+s.when+' '+p.name).toLowerCase().indexOf(term) >= 0; });
      if(!sk.length) return; total += sk.length;
      out += '<div class="plugin" style="--c:'+p.color+'"><div class="ph"><span class="ic">'+p.icon+'</span><div><h3>'+esc(p.name)+' <small style="color:var(--muted);font-weight:500;font-size:13px">v'+p.version+' · '+p.skills.length+' skills</small></h3><p>'+esc(p.desc)+'</p></div>'+
        '<span class="inst"><span>/plugin install '+p.name+'@claude-qa-skills</span><button class="copy" data-copy="/plugin install '+p.name+'@claude-qa-skills">Copy</button></span></div><div class="skills">'+
        sk.map(function(s){ return '<a class="skill" href="'+s.url+'"><b>'+esc(s.name)+'</b>'+(s.script?'<span class="py">script</span>':'')+'<p>'+esc(s.what)+'</p>'+(s.when?'<small>'+esc(s.when)+'</small>':'')+'</a>'; }).join('')+'</div></div>';
    });
    document.getElementById('plugins').innerHTML = out || '<p class="sub">No skill matches. Try another word.</p>';
    document.getElementById('count').textContent = total + ' skill' + (total===1?'':'s') + ' shown';
  }
  render();
  document.addEventListener('click', function(e){
    var b = e.target.closest('.copy'); if(!b) return; e.preventDefault();
    var text = b.dataset.copy || b.parentNode.querySelector('code').textContent;
    (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(function(){ b.textContent='Copied'; b.classList.add('ok'); setTimeout(function(){ b.textContent='Copy'; b.classList.remove('ok'); }, 1400); }).catch(function(){});
  });
  document.querySelectorAll('.install .tabs button').forEach(function(t){ t.addEventListener('click', function(){
    document.querySelectorAll('.install .tabs button').forEach(function(x){ x.classList.toggle('on', x===t); });
    document.querySelectorAll('.install .pane').forEach(function(p){ p.classList.toggle('on', p.id===t.dataset.pane); }); }); });
})();
</script>
</body>
</html>
"""


def main():
    mp, plugins, scripts = data()
    n = sum(len(p["skills"]) for p in plugins)
    page = (PAGE.replace("__NSKILLS__", str(n)).replace("__NPLUGINS__", str(len(plugins)))
            .replace("__NSCRIPTS__", str(scripts)).replace("__REPO__", REPO)
            .replace("__DATA__", json.dumps(plugins, ensure_ascii=False).replace("</", "<\\/")))
    out = os.path.join(ROOT, "docs", "index.html")
    open(out, "w", encoding="utf-8", newline="\n").write(page)
    print("site: %d plugins, %d skills, %d scripts -> %s" % (len(plugins), n, scripts, out))


if __name__ == "__main__":
    main()
