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
            + _qt(n, "Multiple choice", q_en, q_ar) + f'<ol class="opts">{lis}</ol>'
            + _box("why", "Explanation", why_en, why_ar) + "</div>")

def tf(q_en, q_ar, answer, why_en="", why_ar="", src="", ref=""):
    """answer = True / False."""
    return (lambda n: f'<div class="q" data-type="tf" data-answer="{str(bool(answer)).lower()}"{_attrs(src, ref)}>'
            + _qt(n, "True or False", q_en, q_ar)
            + _box("why", "Explanation", why_en, why_ar) + "</div>")

def essay(q_en, q_ar, model_en, model_ar, src="", ref=""):
    """Open question: the student writes, then reveals the model answer and marks themself."""
    return (lambda n: f'<div class="q" data-type="essay"{_attrs(src, ref)}>'
            + _qt(n, "Written answer", q_en, q_ar)
            + _box("model", "Model answer", model_en, model_ar) + "</div>")

def quiz(title_en, title_ar, questions, sid="quiz", mode="instant", intro=None):
    """A graded quiz section. mode: 'instant' (feedback per question) or 'exam' (feedback after Submit).
    intro = (en, ar) optional. The toolkit adds the score bar, True/False buttons, answer boxes."""
    qs = "".join(q(i + 1) for i, q in enumerate(questions))
    it = (f'<div class="bi"><p class="e" dir="ltr">{intro[0]}</p><p class="a" dir="rtl">{intro[1]}</p></div>' if intro else "")
    return (f'<section id="{sid}" class="quiz" data-mode="{mode}"><h2><span class="t"><span class="te" dir="ltr">{title_en}</span>'
            f'<span class="ta" dir="rtl">{title_ar}</span></span></h2>{it}{qs}</section>')

def add_toolkit(path, chapter=None, gloss=None, quiz_lang=None, symbols=None, tk_id=None, css=None, js=None):
    """symbols = {"V": ("Voltage", "الجهد", "V"), "R_th": ("Thevenin resistance", "مقاومة ثيفنن", "Ω")} for symbols
    used outside a law() box. Symbols from law() variables are picked up automatically."""
    """Inject the study toolkit (translator, highlighter, notes, search, sources, TOC, dark mode, quiz)
    into a page written by write_page(). chapter = label shown in source references."""
    css = css or open(os.path.join(_HERE, "toolkit.css"), encoding="utf-8").read()
    js = js or open(os.path.join(_HERE, "toolkit.js"), encoding="utf-8").read()
    s = open(path, encoding="utf-8").read()
    meta = ""
    if chapter:
        meta += f'<meta name="chapter" content="{_h.escape(chapter)}">'
    if symbols:
        import json
        sy = {k.replace("{", "").replace("}", ""): list(v) for k, v in symbols.items()}
        meta += '<script type="application/json" id="tk-syms">' + json.dumps(sy, ensure_ascii=False).replace("<", "\\u003c") + "</script>"
    if quiz_lang:
        meta += f'<meta name="tk-quiz-lang" content="{quiz_lang}">'
    if tk_id:
        meta += f'<meta name="tk-id" content="{_h.escape(tk_id)}">'
    if gloss:
        import json
        meta += '<script type="application/json" id="tk-gloss">' + json.dumps(gloss, ensure_ascii=False).replace("<", "\\u003c") + "</script>"
    meta += '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap">'
    s = s.replace("</head>", f"{meta}<style>{css}</style>\n</head>", 1)
    if 'class="tk-sig"' not in s:
        s = s.replace("</body>", '<footer class="tk-sig tk-x">Eyad Al-Mahrouqi · @q7r_9</footer>\n</body>', 1)
    s = s.replace("</body>", f"<script>{js}</script>\n</body>", 1)
    open(path, "w", encoding="utf-8").write(s)
    return os.path.getsize(path)


# ---------------------------------------------------------------- math
import re as _re

def m(expr):
    """Mini math markup -> HTML. x_i or x_{avg} = subscript, x^2 or x^{-9} = superscript,
    [[a || b]] = stacked fraction (nestable), * = ×, Σ, Δ etc. pass through, letters become italic vars.
    Example: m("CPU time = [[IC × CPI || f]]")"""
    s = expr.replace("*", "×").replace("<=", "≤").replace(">=", "≥").replace("!=", "≠")
    while "[[" in s:
        s2 = _re.sub(r"\[\[((?:(?!\[\[).)*?)\|\|((?:(?!\[\[).)*?)\]\]",
                     lambda k: f'<span class="fr"><span class="nu">{k.group(1).strip()}</span><span class="de">{k.group(2).strip()}</span></span>', s)
        if s2 == s:
            break
        s = s2
    s = _re.sub(r"_\{([^}]*)\}", r"<sub>\1</sub>", s)
    s = _re.sub(r"\^\{([^}]*)\}", r"<sup>\1</sup>", s)
    s = _re.sub(r"_([A-Za-z0-9]+)", r"<sub>\1</sub>", s)
    s = _re.sub(r"\^(-?[A-Za-z0-9.]+)", r"<sup>\1</sup>", s)
    return f'<span class="mx" dir="ltr">{s}</span>'

def law(name_en, name_ar, expr, variables=(), when_en="", when_ar="", note_en="", note_ar=""):
    """A course formula in a coloured box. expr uses m() syntax.
    variables = [(symbol, meaning_en, meaning_ar, unit), ...]"""
    rows = "".join(f'<tr><td>{m(v[0])}</td><td><span dir="ltr">{v[1]}</span>' + (f'<span class="a" dir="rtl">{v[2]}</span>' if len(v) > 2 and v[2] else "")
                   + f'</td><td dir="ltr">{v[3] if len(v) > 3 else ""}</td></tr>' for v in variables)
    import json as _j
    syms = {v[0].replace("{", "").replace("}", "").strip(): [v[1], v[2] if len(v) > 2 else "", v[3] if len(v) > 3 else ""] for v in variables}
    out = (f'<div class="law" data-syms="{_h.escape(_j.dumps(syms, ensure_ascii=False))}"><div class="lh"><span dir="ltr">Law · {name_en}</span><span dir="rtl">القانون · {name_ar}</span></div>'
           f'<div class="lf">{m(expr)}</div>')
    if rows:
        out += f'<table class="lv" dir="ltr"><thead><tr><th>Symbol</th><th>Meaning · المعنى</th><th>Unit</th></tr></thead><tbody>{rows}</tbody></table>'
    if when_en or when_ar:
        out += f'<div class="bi lw"><p class="e" dir="ltr"><b>When to use:</b> {when_en}</p><p class="a" dir="rtl"><b>متى نستخدمه:</b> {when_ar}</p></div>'
    if note_en or note_ar:
        out += f'<div class="bi lw"><p class="e" dir="ltr"><b>Watch out:</b> {note_en}</p><p class="a" dir="rtl"><b>انتبه:</b> {note_ar}</p></div>'
    return out + "</div>"

def steps(items, answer=None, check=None):
    """Worked solution, one step per line. items = [(math_or_text, why_en, why_ar), ...]
    The first element goes through m(). answer = (math, words_en). check = (math, words_en)."""
    lis = "".join(f'<li><div class="sx">{m(it[0])}</div>'
                  + (f'<div class="sn" dir="ltr">{it[1]}</div>' if len(it) > 1 and it[1] else "")
                  + (f'<div class="sn a" dir="rtl">{it[2]}</div>' if len(it) > 2 and it[2] else "") + "</li>" for it in items)
    out = f'<ol class="steps">{lis}</ol>'
    if answer:
        out += f'<div class="ans"><span class="lb">Answer · الإجابة</span>{m(answer[0])}' + (f'<span class="aw" dir="ltr">{answer[1]}</span>' if len(answer) > 1 else "") + "</div>"
    if check:
        out += f'<div class="chk"><span class="lb">Check · تحقق</span>{m(check[0])}' + (f'<span class="aw" dir="ltr">{check[1]}</span>' if len(check) > 1 else "") + "</div>"
    return out

def solved(title_en, title_ar, problem_en, problem_ar, given=(), find="", items=(), answer=None, check=None, src=""):
    """A full worked example: problem, Given / Find, the law used, steps, boxed answer, check."""
    g = "".join(f"<li>{m(x)}</li>" for x in given)
    head = f'<div class="solved"><h4 dir="ltr">{title_en} <span class="h3a" dir="rtl">{title_ar}</span>' + (f' <span class="src">{src}</span>' if src else "") + "</h4>"
    head += f'<div class="bi"><p class="e" dir="ltr">{problem_en}</p><p class="a" dir="rtl">{problem_ar}</p></div>'
    if g or find:
        head += f'<div class="gf" dir="ltr"><div><b>Given</b><ul>{g}</ul></div><div><b>Find</b><p>{m(find) if find else ""}</p></div></div>'
    return head + steps(items, answer, check) + "</div>"


# ---------------------------------------------------------------- real summary blocks
def _ul(items):
    if isinstance(items, str):
        return f"<p>{items}</p>"
    return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

def bigpicture(idea_en, idea_ar, center, branches, src=""):
    """Chapter opener: the big idea in 1–2 sentences + a concept map.
    branches = [(label, [children...], relation), ...] — relation is a short verb phrase shown on the link,
    label/children may be (text, concept_id) to link to a concept card."""
    def lk(x):
        if isinstance(x, (tuple, list)):
            return f'<a href="#c-{x[1]}">{x[0]}</a>'
        return x
    br = "".join(
        f'<li><span class="rel">{b[2] if len(b) > 2 else ""}</span><div class="nd">{lk(b[0])}</div>'
        + ("<ul>" + "".join(f'<li><div class="nd sm">{lk(c)}</div></li>' for c in b[1]) + "</ul>" if len(b) > 1 and b[1] else "")
        + "</li>" for b in branches)
    return (f'<section id="big" class="bigp"><div class="idea"><span class="lbl">The big idea · الفكرة الكبيرة</span>'
            f'<p class="e" dir="ltr">{idea_en}</p><p class="a" dir="rtl">{idea_ar}</p></div>'
            f'<div class="cmap" dir="ltr"><ul><li><div class="nd root">{center}</div><ul>{br}</ul></li></ul></div>'
            + (f'<p class="slides">{src}</p>' if src else "") + "</section>")

def lead(why_en, builds_on="", leads_to="", why_ar=""):
    """Section opener: why this topic matters + how it links to the previous/next topic."""
    chain = ""
    if builds_on or leads_to:
        chain = '<div class="chain" dir="ltr">' + (f'<span>Builds on <b>{builds_on}</b></span>' if builds_on else "") + \
                (f'<span class="ar">→</span><span>Leads to <b>{leads_to}</b></span>' if leads_to else "") + "</div>"
    return f'<div class="lead">{chain}<p dir="ltr">{why_en}</p>' + (f'<p class="a" dir="rtl">{why_ar}</p>' if why_ar else "") + "</div>"

def concept(cid, name, definition="", plain="", how=None, example="", mistake="", connects=None, ar="", src="", extra=""):
    """One concept card. definition = the course's exact wording (no paraphrase). plain = one simple sentence.
    how = str or list (how it works / parts / rules). connects = [(concept_id, "how they relate"), ...].
    ar = ONE short Arabic line with the meaning (not a translation of the card). extra = any HTML (fig, law, table)."""
    rows = ""
    if definition:
        rows += f'<div class="r def"><span class="cl">Definition</span><div class="cv"><q>{definition}</q></div></div>'
    if plain:
        rows += f'<div class="r"><span class="cl">In plain words</span><div class="cv">{plain}</div></div>'
    if how:
        rows += f'<div class="r"><span class="cl">How it works</span><div class="cv">{_ul(how)}</div></div>'
    if example:
        rows += f'<div class="r"><span class="cl">Example</span><div class="cv">{example}</div></div>'
    if mistake:
        rows += f'<div class="r mis"><span class="cl">Common mistake</span><div class="cv">{mistake}</div></div>'
    if connects:
        rows += ('<div class="r con"><span class="cl">Connects to</span><div class="cv"><ul>'
                 + "".join(f'<li><a href="#c-{c[0]}">{c[0].replace("-", " ").title() if len(c) < 3 else c[2]}</a> — {c[1]}</li>' for c in connects)
                 + "</ul></div></div>")
    return (f'<div class="concept" id="c-{cid}"><div class="chd"><h4 dir="ltr">{name}</h4>'
            + (f'<span class="src">{src}</span>' if src else "") + "</div>"
            + (f'<div class="car" dir="rtl">{ar}</div>' if ar else "") + rows + extra + "</div>")

def compare(title, headers, rows, note=""):
    """Side-by-side comparison of close concepts. headers = ["", "A", "B"], rows = [["Aspect", a, b], ...]."""
    h = "".join(f"<th>{x}</th>" for x in headers)
    r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return (f'<div class="cmp"><div class="cmh">{title}</div><table dir="ltr"><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table>'
            + (f'<p class="cmn">{note}</p>' if note else "") + "</div>")

def keypoints(items, title="Key points · أهم النقاط"):
    """At most 5, most important first. items = ["point", ("core point", True), ...]; core = must-know."""
    lis = ""
    for x in items[:5]:
        t, core = (x if isinstance(x, (tuple, list)) else (x, False))
        lis += f'<li class="{"core" if core else ""}">{t}</li>'
    return f'<div class="kp"><div class="kph">{title}</div><ol dir="ltr">{lis}</ol></div>'

def cheatsheet(definitions=(), formulas=(), differences=(), traps=(), sid="cheat"):
    """One-page quick review at the end. definitions = [(term, short meaning)], formulas = [m-expr or (name, m-expr)],
    differences = [(A, B, "difference")], traps = ["..."]."""
    out = f'<section id="{sid}" class="cheat"><h2><span class="t"><span class="te" dir="ltr">Quick review sheet</span><span class="ta" dir="rtl">ورقة المراجعة السريعة</span></span></h2><div class="cg" dir="ltr">'
    if definitions:
        out += '<div class="cb"><h5>Definitions</h5><dl>' + "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in definitions) + "</dl></div>"
    if formulas:
        out += '<div class="cb"><h5>Formulas</h5><ul class="fm">' + "".join(
            f"<li><span class=\"fl\">{f[0]}</span>{m(f[1])}</li>" if isinstance(f, (tuple, list)) else f"<li>{m(f)}</li>" for f in formulas) + "</ul></div>"
    if differences:
        out += '<div class="cb"><h5>Don\'t confuse</h5><ul>' + "".join(f"<li><b>{a}</b> vs <b>{b}</b>: {d}</li>" for a, b, d in differences) + "</ul></div>"
    if traps:
        out += '<div class="cb trap"><h5>Exam traps</h5><ul>' + "".join(f"<li>{t}</li>" for t in traps) + "</ul></div>"
    return out + "</div></section>"
