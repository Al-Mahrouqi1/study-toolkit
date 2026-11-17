"""Helpers for building the bilingual (English + Arabic) study-summary HTML page.

Typical use (see assets/build_template.py):

    import sys; sys.path.insert(0, "<skill>/scripts")
    from bilingual_lib import *
    set_image_dir("img")                   # folder holding the cropped PNGs
    body = section(1, "Title", "العنوان", "Slides 3-7", "الشرائح 3-7", [ ...blocks... ])
    write_page("out.html", "Chapter 1: ...", "ملخص ...", lede_en, lede_ar, toc, body)

Every block is a string of HTML. Pass plain strings for the first (English) argument and use
L("English term") inside the Arabic argument so English terms stay left-to-right in RTL text.
Beware f-strings: literal braces such as {Name, Address} must be doubled ({{...}}) or put in L("...").
"""
import base64, io, os
from PIL import Image

_HERE = os.path.dirname(os.path.abspath(__file__))
_IMG = "img"

def set_image_dir(path):
    global _IMG; _IMG = path

def L(t):
    """Keep an English term left-to-right inside Arabic text."""
    return f'<span dir="ltr">{t}</span>'

def b64(name, maxw=1100):
    im = Image.open(os.path.join(_IMG, f"{name}.png")).convert("RGB")
    if im.size[0] > maxw:
        im = im.resize((maxw, int(im.size[1] * maxw / im.size[0])), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=88, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

def bi(en, ar, cls=""):
    """A paragraph in both languages (English first, Arabic below with a side rule)."""
    return f'<div class="bi {cls}"><p class="e" dir="ltr">{en}</p><p class="a" dir="rtl">{ar}</p></div>'

def bil(items, cls="plain"):
    """Bullet list; items = [(english, arabic), ...]. Use '' for an Arabic gloss you do not need."""
    return f'<ul class="{cls}">' + "".join(
        f'<li><span class="e" dir="ltr">{e}</span>' + (f'<span class="a" dir="rtl">{a}</span>' if a else "") + "</li>"
        for e, a in items) + "</ul>"

def numbered(items):
    return '<ol class="order">' + "".join(
        f'<li><span class="e" dir="ltr">{e}</span><span class="a" dir="rtl">{a}</span></li>' for e, a in items) + "</ol>"

def term(defn, en, ar, tag=("Course definition", "التعريف حسب المادة")):
    """Course definition (verbatim wording, English) + simple explanation in both languages."""
    return (f'<div class="term"><span class="tag"><span dir="ltr">{tag[0]}</span> · <span dir="rtl">{tag[1]}</span></span>'
            f'<p class="def" dir="ltr">{defn}</p><div class="bi"><p class="e" dir="ltr"><b>Simple explanation:</b> {en}</p>'
            f'<p class="a" dir="rtl"><b>شرح مبسّط:</b> {ar}</p></div></div>')

def fig(name, slide, cap_en, cap_ar, en, ar, maxw=1100):
    """Embedded picture + caption + 'What the picture shows' in both languages."""
    return (f'<figure><img src="{b64(name, maxw)}" alt="{cap_en}"><figcaption><span dir="ltr">{cap_en}</span> · '
            f'<span dir="rtl">{cap_ar}</span> <span class="src" dir="ltr">Slide {slide}</span></figcaption></figure>'
            f'<div class="explain"><b dir="ltr">What the picture shows</b><b dir="rtl" class="arh">ماذا تعني الصورة؟</b>'
            f'<p class="e" dir="ltr">{en}</p><p class="a" dir="rtl">{ar}</p></div>')

def review(items):
    """'For review' box. items = [(en, ar), ...]. Wording says 'appears important', never 'will be on the exam'."""
    return ('<div class="review"><b><span dir="ltr">For review (appears important to study)</span> · '
            '<span dir="rtl">للمراجعة (يبدو مهمًا للدراسة)</span></b>' + bil(items, "rv") + "</div>")

def warn(en, ar):
    """Yellow note for gaps, unreadable visuals, contradictions, or outside-the-chapter items."""
    return f'<div class="warn"><p class="e" dir="ltr">{en}</p><p class="a" dir="rtl">{ar}</p></div>'

def card(title, en, ar, eg=None, wn=None):
    s = f'<div class="card"><h4 dir="ltr">{title}</h4>{bi(en, ar)}'
    if eg: s += f'<div class="eg">{bi(eg[0], eg[1])}</div>'
    if wn: s += warn(*wn)
    return s + "</div>"

def cards(*items):
    return '<div class="cards">' + "".join(items) + "</div>"

def two(*items):
    return '<div class="two">' + "".join(items) + "</div>"

def h2(n, en, ar, slides_en, slides_ar):
    return (f'<h2><span class="n">{n}</span><span class="t"><span class="te" dir="ltr">{en}</span>'
            f'<span class="ta" dir="rtl">{ar}</span></span></h2>'
            f'<p class="slides"><span dir="ltr">{slides_en}</span> · <span dir="rtl">{slides_ar}</span></p>')

def h3(en, ar):
    return f'<h3 dir="ltr">{en} <span class="h3a" dir="rtl">{ar}</span></h3>'

def dtable(head, rows, cls="data"):
    """A real data table copied from the source (kept LTR)."""
    h = "".join(f"<th>{c}</th>" for c in head)
    r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<table class="{cls}" dir="ltr"><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table>'

def section(n, en, ar, slides_en, slides_ar, blocks, sid=None):
    return f'<section id="{sid or "s%d" % n}">' + h2(n, en, ar, slides_en, slides_ar) + "\n".join(blocks) + "</section>"

def practice(intro_en, intro_ar, questions):
    """Practice questions WITHOUT answers. questions = [(en, ar), ...]"""
    return ('<section id="practice"><h2><span class="t"><span class="te" dir="ltr">Practice questions</span>'
            '<span class="ta" dir="rtl">أسئلة التدريب</span></span></h2>' + bi(intro_en, intro_ar) + numbered(questions) + "</section>")

def status(rows):
    """Review-status table. rows = [section title, ...]. All start as 'Not yet tested' (never label a weakness without evidence)."""
    body = "".join(f"<tr><td>{t}</td><td>Not yet tested · لم يُختبر بعد</td></tr>" for t in rows)
    return ('<section id="status"><h2><span class="t"><span class="te" dir="ltr">Review status</span>'
            '<span class="ta" dir="rtl">حالة المراجعة</span></span></h2><table dir="ltr"><thead><tr>'
            '<th>Section · القسم</th><th>Status · الحالة</th></tr></thead><tbody>' + body + "</tbody></table>"
            + bi("No section is marked as a weakness because no question has been answered yet.",
                 "لم أصنّف أي قسم كنقطة ضعف لأنه لم تُجب عن أي سؤال بعد.", "muted") + "</section>")

def write_page(out, title_en, title_ar, lede_en, lede_ar, toc, body, head_extra=""):
    """toc = [(anchor, label), ...]. Writes one self-contained HTML file (images inlined)."""
    css = open(os.path.join(_HERE, "..", "assets", "style.css"), encoding="utf-8").read()
    nav = "".join(f'<a href="#{a}">{t}</a>' for a, t in toc)
    html = f'''<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_en} · {title_ar}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;700&family=Manrope:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>{css}</style>{head_extra}
</head>
<body>
<main>
<h1>{title_en}<span class="ar" dir="rtl">{title_ar}</span></h1>
<div class="lede"><p class="e" dir="ltr">{lede_en}</p><p class="a" dir="rtl">{lede_ar}</p></div>
<nav class="toc" aria-label="Sections">{nav}</nav>
{body}
</main>
</body>
</html>'''
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    return os.path.getsize(out)

def check_html(path):
    """Tag-balance check; returns (unclosed, errors, image_count)."""
    from html.parser import HTMLParser
    s = open(path, encoding="utf-8").read()
    class P(HTMLParser):
        def __init__(self): super().__init__(); self.st = []; self.err = []
        def handle_starttag(self, t, a):
            if t not in ("meta", "link", "img", "br"): self.st.append(t)
        def handle_endtag(self, t):
            if not self.st or self.st[-1] != t: self.err.append((t, self.st[-3:]))
            else: self.st.pop()
    p = P(); p.feed(s)
    return p.st, p.err[:5], s.count("<img")
