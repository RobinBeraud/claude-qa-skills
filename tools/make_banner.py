#!/usr/bin/env python3
"""Compose docs/assets/banner.png (README) and docs/assets/social-preview.png (1280x640) from the hero art.

Needs Pillow. Run from the repo root: python tools/make_banner.py <skills> <plugins>
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "docs", "assets")
FONTS = [r"C:\Windows\Fonts\segoeuib.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
REG = [r"C:\Windows\Fonts\segoeui.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
CHIPS = [("test strategy", (255, 122, 0), (15, 27, 51)), ("unit & mutation", (41, 98, 255), (255, 255, 255)),
         ("DORA", (22, 179, 166), (15, 27, 51)), ("EBM", (242, 68, 139), (255, 255, 255)),
         ("AI-era QA", (123, 97, 255), (255, 255, 255)), ("ERP & e-invoicing", (255, 196, 0), (15, 27, 51)),
         (".NET · legacy · DevOps", (56, 189, 248), (15, 27, 51))]


def f(paths, size):
    return ImageFont.truetype(next(p for p in paths if os.path.exists(p)), size)


def compose(w, h, skills, plugins, out):
    hero = Image.open(os.path.join(ASSETS, "hero.jpg")).convert("RGB")
    bg_col = hero.getpixel((20, hero.height // 2))
    canvas = Image.new("RGB", (w, h), bg_col)
    scale = h / hero.height
    art = hero.resize((int(hero.width * scale), h), Image.LANCZOS)
    x0 = w - art.width + int(art.width * 0.04)
    mask = Image.new("L", art.size, 255)
    md = ImageDraw.Draw(mask)
    fade = int(art.width * 0.35)
    for x in range(fade):
        md.line([(x, 0), (x, h)], fill=int(255 * x / fade))
    canvas.paste(art, (x0, 0), mask)
    d = ImageDraw.Draw(canvas)
    s = h / 640
    left = int(64 * s)
    d.text((left, int(150 * s)), "claude-", font=f(FONTS, int(76 * s)), fill=(255, 255, 255))
    wc = d.textlength("claude-", font=f(FONTS, int(76 * s)))
    d.text((left + wc, int(150 * s)), "qa", font=f(FONTS, int(76 * s)), fill=(255, 160, 40))
    wq = d.textlength("qa", font=f(FONTS, int(76 * s)))
    d.text((left + wc + wq, int(150 * s)), "-skills", font=f(FONTS, int(76 * s)), fill=(255, 255, 255))
    d.text((left, int(262 * s)), "%d QA & developer skills for Claude Code" % skills, font=f(REG, int(32 * s)), fill=(210, 220, 240))
    d.text((left, int(310 * s)), "%d installable plugins · tested stdlib scripts · MIT" % plugins, font=f(REG, int(24 * s)), fill=(150, 168, 200))
    x, y = left, int(388 * s)
    cf = f(FONTS, int(19 * s))
    for label, bgc, fg in CHIPS:
        tw = d.textlength(label, font=cf)
        bw = tw + int(30 * s)
        if x + bw > w * 0.62:
            x, y = left, y + int(50 * s)
        d.rounded_rectangle([x, y, x + bw, y + int(40 * s)], radius=int(20 * s), fill=bgc)
        d.text((x + bw / 2, y + int(20 * s)), label, font=cf, fill=fg, anchor="mm")
        x += bw + int(12 * s)
    d.text((left, h - int(56 * s)), "/plugin marketplace add RobinBeraud/claude-qa-skills", font=f(REG, int(20 * s)), fill=(255, 196, 0))
    canvas.save(out, optimize=True)
    print("wrote", out, canvas.size)


def main():
    skills, plugins = int(sys.argv[1]), int(sys.argv[2])
    raw = os.path.join(ASSETS, "hero_raw.png")
    if os.path.exists(raw):
        Image.open(raw).convert("RGB").save(os.path.join(ASSETS, "hero.jpg"), quality=88, optimize=True)
        os.remove(raw)
    compose(1600, 640, skills, plugins, os.path.join(ASSETS, "banner.png"))
    compose(1280, 640, skills, plugins, os.path.join(ASSETS, "social-preview.png"))


if __name__ == "__main__":
    main()
