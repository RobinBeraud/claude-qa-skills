#!/usr/bin/env python3
"""Render docs/assets/demo.gif: a terminal typing real commands on examples/ and showing their real output.

Needs Pillow (pip install pillow). Run from the repo root: python tools/make_demo_gif.py
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, PAD, LH, FS = 1040, 600, 26, 25, 17
BG, BAR, FG, DIM = (15, 23, 42), (30, 41, 66), (226, 232, 240), (120, 136, 160)
GREEN, RED, YELLOW, CYAN, ORANGE = (74, 222, 128), (248, 113, 113), (250, 204, 21), (103, 232, 249), (255, 145, 60)
FONT = next((f for f in [r"C:\Windows\Fonts\consola.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                         "/System/Library/Fonts/Menlo.ttc"] if os.path.exists(f)), None)
BOLD = next((f for f in [r"C:\Windows\Fonts\consolab.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"]
             if os.path.exists(f)), FONT)
font = ImageFont.truetype(FONT, FS)
bold = ImageFont.truetype(BOLD, FS)
small = ImageFont.truetype(FONT, 14)

SCENES = [
    ("# Fake but valid French business ids: SIREN, VAT, IBAN",
     "python fr_test_data.py validate 732829320 FR44732829320 FR7630006000011234567890189 123456789",
     ["plugins/qa-shift-left/skills/test-data-fr/scripts/fr_test_data.py", "validate", "732829320", "FR44732829320",
      "FR7630006000011234567890189", "123456789"]),
    ("# EN 16931 arithmetic of an e-invoice (CII / Factur-X)",
     "python cii_check.py examples/invoice-wrong-vat.xml",
     ["plugins/qa-business-apps/skills/einvoice-consistency/scripts/cii_check.py", "examples/invoice-wrong-vat.xml"]),
    ("# Flaky tests across 6 CI runs",
     "python flaky_tests.py examples/junit-runs --format csv",
     ["plugins/qa-ci-insights/skills/flaky-test-hunter/scripts/flaky_tests.py", "examples/junit-runs", "--format", "csv"]),
    ("# Permissions: expected matrix vs what the app really allows",
     "python rbac_matrix.py compare examples/rbac-matrix.csv examples/rbac-observed.csv",
     ["plugins/qa-business-apps/skills/permissions-matrix/scripts/rbac_matrix.py", "compare", "examples/rbac-matrix.csv",
      "examples/rbac-observed.csv"]),
]


def run(args):
    out = subprocess.run([sys.executable, "-I"] + args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    return [l for l in out.stdout.rstrip().splitlines()]


def colour(line):
    for word, c in (("FAIL", RED), ("INVALID", RED), ("SECURITY", RED), ("FUNCTIONAL", YELLOW), (" OK", GREEN)):
        if word in line:
            return c
    if line.startswith(("test,", "|", "#")):
        return CYAN
    return FG


def frame(lines, title):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 38], fill=BAR)
    for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d.ellipse([16 + i * 22, 13, 28 + i * 22, 25], fill=c)
    d.text((W // 2, 19), title, font=small, fill=DIM, anchor="mm")
    y = 38 + PAD - 6
    for kind, text in lines[-20:]:
        if kind == "cmd":
            d.text((PAD, y), "$ ", font=bold, fill=GREEN)
            d.text((PAD + 22, y), text, font=bold, fill=FG)
        elif kind == "comment":
            d.text((PAD, y), text, font=font, fill=ORANGE)
        else:
            t = text if len(text) <= 104 else text[:103] + "…"
            d.text((PAD, y), t, font=font, fill=colour(text))
        y += LH
    return im


def main():
    title = "claude-qa-skills · bundled tools · Python standard library only"
    frames, durations = [], []
    for comment, shown, args in SCENES:
        output = run(args)
        lines = [("comment", comment)]
        frames.append(frame(lines, title)); durations.append(600)
        for i in range(0, len(shown) + 4, 4):
            frames.append(frame(lines + [("cmd", shown[:i] + ("▌" if i < len(shown) else ""))], title))
            durations.append(45)
        lines = lines + [("cmd", shown)]
        for out_line in output:
            lines.append(("out", out_line))
            frames.append(frame(lines, title)); durations.append(70)
        durations[-1] = 2600
    pal = frames[0].quantize(colors=64, method=Image.Quantize.MEDIANCUT)
    q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
    out = os.path.join(ROOT, "docs", "assets", "demo.gif")
    q[0].save(out, save_all=True, append_images=q[1:], duration=durations, loop=0, optimize=True)
    print("wrote %s (%d frames, %d KB)" % (out, len(q), os.path.getsize(out) // 1024))


if __name__ == "__main__":
    main()
