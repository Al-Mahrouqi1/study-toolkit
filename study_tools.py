"""Quiz helpers + toolkit injection for bilingual_lib pages.

    from bilingual_lib import *; from study_tools import *
    body += quiz("Chapter test", "اختبار الفصل", [
        mcq("Question?", "السؤال؟", [("Option A", "الخيار أ"), ("Option B", "الخيار ب")], 1,
            "Why B is right.", "لماذا ب صحيح.", src="Slides 14–19", ref="s3"),
        tf("Statement.", "العبارة.", False, "Why.", "لماذا.", src="Slide 7", ref="s2"),
        essay("Explain X.", "اشرح X.", "Model answer.", "الإجابة النموذجية.", src="Slides 3–6", ref="s1"),
    ], mode="instant")            # or mode="exam": answers shown only after "Submit"
    write_page(out, ...); add_toolkit(out, chapter="Chapter 2: ERD")
"""
import os, html as _h

_HERE = os.path.dirname(os.path.abspath(__file__))

def _attrs(src, ref):
    s = f' data-src="{_h.escape(src)}"' if src else ""
    return s + (f' data-ref="{ref}"' if ref else "")

def _qt(n, kind, q_en, q_ar):
    return (f'<div class="qt"><span class="qn">{n}</span><div class="bi"><span class="kind">{kind}</span>'
            f'<p class="e" dir="ltr">{q_en}</p><p class="a" dir="rtl">{q_ar}</p></div></div>')

def _box(cls, label, en, ar):
    if not (en or ar):
        return ""
    return (f'<div class="{cls}"><b>{label}</b><div class="bi"><p class="e" dir="ltr">{en}</p>'
            + (f'<p class="a" dir="rtl">{ar}</p>' if ar else "") + "</div></div>")

def mcq(q_en, q_ar, options, answer, why_en="", why_ar="", src="", ref=""):
    """options = [(en, ar), ...] or [en, ...]; answer = 0-based index of the correct option."""
    lis = "".join(
        f'<li><span class="e" dir="ltr">{o[0]}</span>' + (f'<span class="a" dir="rtl">{o[1]}</span>' if o[1] else "") + "</li>"
        if isinstance(o, (tuple, list)) else f'<li><span class="e" dir="ltr">{o}</span></li>' for o in options)
    return (lambda n: f'<div class="q" data-type="mcq" data-answer="{answer}"{_attrs(src, ref)}>'
            + _qt(n, "Multiple choice · اختيار من متعدد", q_en, q_ar) + f'<ol class="opts">{lis}</ol>'
            + _box("why", "Explanation · الشرح", why_en, why_ar) + "</div>")

def tf(q_en, q_ar, answer, why_en="", why_ar="", src="", ref=""):
    """answer = True / False."""
    return (lambda n: f'<div class="q" data-type="tf" data-answer="{str(bool(answer)).lower()}"{_attrs(src, ref)}>'
            + _qt(n, "True or False · صح أم خطأ", q_en, q_ar)
            + _box("why", "Explanation · الشرح", why_en, why_ar) + "</div>")

def essay(q_en, q_ar, model_en, model_ar, src="", ref=""):
    """Open question: the student writes, then reveals the model answer and marks themself."""
    return (lambda n: f'<div class="q" data-type="essay"{_attrs(src, ref)}>'
            + _qt(n, "Written answer · سؤال مقالي", q_en, q_ar)
            + _box("model", "Model answer · الإجابة النموذجية", model_en, model_ar) + "</div>")

def quiz(title_en, title_ar, questions, sid="quiz", mode="instant", intro=None):
    """A graded quiz section. mode: 'instant' (feedback per question) or 'exam' (feedback after Submit).
    intro = (en, ar) optional. The toolkit adds the score bar, True/False buttons, answer boxes."""
    qs = "".join(q(i + 1) for i, q in enumerate(questions))
    it = (f'<div class="bi"><p class="e" dir="ltr">{intro[0]}</p><p class="a" dir="rtl">{intro[1]}</p></div>' if intro else "")
    return (f'<section id="{sid}" class="quiz" data-mode="{mode}"><h2><span class="t"><span class="te" dir="ltr">{title_en}</span>'
            f'<span class="ta" dir="rtl">{title_ar}</span></span></h2>{it}{qs}</section>')

def add_toolkit(path, chapter=None, gloss=None, tk_id=None, css=None, js=None):
    """Inject the study toolkit (translator, highlighter, notes, search, sources, TOC, dark mode, quiz)
    into a page written by write_page(). chapter = label shown in source references."""
    css = css or open(os.path.join(_HERE, "toolkit.css"), encoding="utf-8").read()
    js = js or open(os.path.join(_HERE, "toolkit.js"), encoding="utf-8").read()
    s = open(path, encoding="utf-8").read()
    meta = ""
    if chapter:
        meta += f'<meta name="chapter" content="{_h.escape(chapter)}">'
    if tk_id:
        meta += f'<meta name="tk-id" content="{_h.escape(tk_id)}">'
    if gloss:
        import json
        meta += '<script type="application/json" id="tk-gloss">' + json.dumps(gloss, ensure_ascii=False).replace("<", "\\u003c") + "</script>"
    s = s.replace("</head>", f"{meta}<style>{css}</style>\n</head>", 1)
    if 'class="tk-sig"' not in s:
        s = s.replace("</body>", '<footer class="tk-sig tk-x">Eyad Al-Mahrouqi · @q7r_9</footer>\n</body>', 1)
    s = s.replace("</body>", f"<script>{js}</script>\n</body>", 1)
    open(path, "w", encoding="utf-8").write(s)
    return os.path.getsize(path)
