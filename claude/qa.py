#!/usr/bin/env python3
"""Automatic quality check of a finished study page. Prints a short report; exit 1 if there are errors.

Usage: python work/tk/qa.py OUT.html [--slides work/<stem>/slides.txt] [--no-browser]

Checks: HTML balance, toolkit present, glossary size, sections cite slides, concept cards have a
definition, forbidden wording, English/Arabic duplication, key-point limits, quiz answers valid,
worked solutions have a boxed answer, images embedded, summary length vs slides, and (if Chrome or
Playwright is available) opens the page headless to catch JavaScript errors.
"""
import json, os, re, shutil, sys
from html.parser import HTMLParser

VOID = {"meta", "link", "img", "br", "hr", "input", "source", "col", "area", "base", "wbr", "path", "circle", "rect", "line", "polyline", "polygon", "ellipse"}

class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.st = []; s.err = []; s.cls = []; s.txt = {"e": 0, "a": 0}; s.cur = []
    def handle_starttag(s, t, a):
        d = dict(a)
        if t not in VOID and not t.endswith("/"):
            s.st.append(t); s.cur.append(d.get("class", "") or "")
    def handle_startendtag(s, t, a): pass
    def handle_endtag(s, t):
        if t in VOID: return
        if s.st and s.st[-1] == t:
            s.st.pop(); s.cur.pop()
        else:
            s.err.append(t)
    def handle_data(s, d):
        if not s.cur or "script" in s.st or "style" in s.st: return
        c = " ".join(s.cur[-3:])
        n = len(d.strip())
        if re.search(r"(^|\s)a(\s|$)", s.cur[-1] or "") : s.txt["a"] += n
        elif re.search(r"(^|\s)e(\s|$)", s.cur[-1] or ""): s.txt["e"] += n

def main(path, slides=None, browser=True):
    s = open(path, encoding="utf-8").read()
    errs, warns, info = [], [], []
    p = P(); p.feed(s)
    if p.err: errs.append(f"unbalanced tags near: {', '.join(p.err[:5])}")
    if "tk-bar" not in s and "toolkit" not in s and 'id="tk-' not in s:
        warns.append("study toolkit not added (add_toolkit was not called or failed)")
    m = re.search(r'<script type="application/json" id="tk-gloss">(.*?)</script>', s, re.S)
    g = len(json.loads(m.group(1).replace("\\u003c", "<"))) if m else 0
    (warns if g < 40 else info).append(f"glossary entries: {g}" + (" (aim for 40–120)" if g < 40 else ""))
    secs = re.findall(r'<section id="(s\d+)"(.*?)</section>', s, re.S)
    nos = [sid for sid, body in secs if 'class="slides"' not in body and "Slide" not in body]
    if nos: warns.append(f"sections without slide references: {', '.join(nos)}")
    cards = re.findall(r'<div class="concept" id="c-([\w-]+)">(.*?)(?=<div class="concept"|</section>)', s, re.S)
    nodef = [c for c, b in cards if 'class="r def"' not in b]
    if nodef: warns.append(f"concept cards without a course definition: {', '.join(nodef[:8])}")
    info.append(f"concept cards: {len(cards)}")
    for bad in ("will be on the exam", "will come in the exam", "سيأتي في الاختبار", "سيكون في الامتحان"):
        if bad.lower() in s.lower(): errs.append(f"forbidden wording: '{bad}'")
    links = set(re.findall(r'href="#c-([\w-]+)"', s)); ids = set(c for c, _ in cards)
    broken = sorted(links - ids)
    if broken: errs.append(f"links to missing concept cards: {', '.join(broken[:8])}")
    for kp in re.findall(r'<div class="kp">.*?<ol[^>]*>(.*?)</ol>', s, re.S):
        if kp.count("<li") > 5: warns.append("a key-points box has more than 5 items")
    if p.txt["e"] and p.txt["a"] / p.txt["e"] > 0.7:
        warns.append(f"Arabic text is {p.txt['a'] * 100 // p.txt['e']}% of English — likely duplicated translation")
    for q in re.findall(r'<div class="q" data-type="mcq" data-answer="(\d+)".*?<ol class="opts">(.*?)</ol>', s, re.S):
        if int(q[0]) >= q[1].count("<li"): errs.append("an MCQ answer index points past its options")
    nq = len(re.findall(r'<div class="q" data-type=', s))
    if nq: info.append(f"questions: {nq}")
    for b in re.findall(r'<div class="solved">(.*?)(?=<div class="solved">|</section>)', s, re.S):
        if 'class="ans"' not in b: warns.append("a worked example has no boxed answer")
    imgs = re.findall(r'<img [^>]*src="([^"]+)"', s)
    ext = [i for i in imgs if not i.startswith("data:")]
    if ext: warns.append(f"{len(ext)} image(s) not embedded (will break when the file is moved)")
    info.append(f"images: {len(imgs)} · size: {os.path.getsize(path) // 1024} KB")
    if slides and os.path.exists(slides):
        sw = len(open(slides, encoding="utf-8").read().split())
        text = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", s, flags=re.S)
        ew = len(re.findall(r"[A-Za-z]{2,}", text))
        ratio = ew / max(sw, 1)
        info.append(f"English words: {ew} vs slides {sw} ({ratio:.0%})")
        if ratio > 0.8 and sw > 300: warns.append("summary is long compared with the slides (target ≈ 33%)")
    if browser:
        info.append(browser_check(path, errs))
    print(f"QA {os.path.basename(path)}: {'FAIL' if errs else 'OK'}")
    for e in errs: print("  ERROR  " + e)
    for w in warns: print("  WARN   " + w)
    print("  info   " + " · ".join(i for i in info if i))
    return 1 if errs else 0

def browser_check(path, errs):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return "browser check skipped (no playwright)"
    exe = next((shutil.which(x) for x in ("google-chrome", "chromium", "chromium-browser", "chrome") if shutil.which(x)), None)
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(executable_path=exe, args=["--no-sandbox"]) if exe else pw.chromium.launch()
            pg = b.new_page(viewport={"width": 1280, "height": 900}); js = []
            pg.on("pageerror", lambda e: js.append(str(e)[:120]))
            pg.goto("file://" + os.path.abspath(path)); pg.wait_for_timeout(700)
            ok = pg.evaluate("!!document.querySelector('#tk-bar')")
            clipped = pg.evaluate("[...document.querySelectorAll('main figure img, main table, .law .lf')].filter(e=>e.scrollWidth>e.clientWidth+4&&getComputedStyle(e).overflowX!=='auto').length")
            b.close()
        if js: errs.append("JavaScript errors: " + " | ".join(js[:3]))
        return f"browser: toolkit {'loaded' if ok else 'NOT loaded'}, {clipped} clipped element(s)"
    except Exception as e:
        return f"browser check skipped ({str(e)[:60]})"

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    sl = a[a.index("--slides") + 1] if "--slides" in a else None
    sys.exit(main(a[0], sl, "--no-browser" not in a))
