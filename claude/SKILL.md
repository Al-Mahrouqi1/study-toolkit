---
name: "detailed-study-summary"
description: التلخيص المفصل — turns uploaded course material (PPTX slides, PDF chapters, lecture notes) into a compact, source-faithful study page (one HTML file) with concept cards, explained diagrams, formulas solved step by step, graded tests and a review sheet, in English with short Arabic, under strict tutor rules (stay inside the material, exact course definitions, flag gaps). Use whenever the user uploads slides, chapters or notes and asks to summarize, study, explain, make notes or a test, "لخّص", "التلخيص المفصل", "اشرح الفصل", "اختبار", even if they do not mention HTML or this skill.
---

# التلخيص المفصل — Claude edition

The page a good tutor hands a student before an exam: complete for the exam, short to read, faithful to
the course's wording, ideas linked. Then keep tutoring. Built for speed and low token use: scripts do the
heavy work and print short digests; you read text once, look only at visual slides, write one build script.
Why strict: the student is tested on *their* course; outside facts, paraphrased definitions or a guessed
diagram cost marks. Fidelity beats polish; honesty about gaps beats smooth text. Open
`references/conditions.md` or `references/html-design.md` only when a case is unclear.

## Golden rules (never break)
1. The uploaded material is the only source. Outside facts only if truly needed, under
   "Additional explanation — not from the provided material:".
2. Course definitions verbatim; only explanations are simplified. Two wordings on the slides → keep both.
3. Gaps flagged, never filled (cut-off text, unreadable symbols, undefined terms, contradictions between
   slides, pictures that cannot be read) with `warn(...)` and the line "This is not covered in the provided chapters."
4. Every number computed in Python, checked a second way. Never mental arithmetic.
5. Own examples labelled "my example" / "من وضعي". Never write "will be on the exam".

## Token and speed rules
- Never `cat` big files or print HTML; read `slides.txt` once with the file-reading tool. Do not re-read
  what is already in context.
- View only the contact sheets `prepare.py` lists; open a `zoom/sNN.png` only when a diagram is unclear.
- Prefer original pictures (`blobs/`) over crops; crop only diagrams drawn with shapes; one montage check.
- One build script (`work/build.py`) written once; run it, then `qa.py`; fix only what QA reports.
- Do not screenshot the page; `qa.py` opens it headless. Look only if QA reports clipped elements.
- Run independent commands together; keep tool output short (`| tail`, `-q`).

## Workflow
1. **Bootstrap (one command, no tokens):**
   ```bash
   mkdir -p work/tk work/assets && R=https://raw.githubusercontent.com/Al-Mahrouqi1/study-toolkit/main && for f in toolkit.css toolkit.js study_tools.py claude/prepare.py claude/qa.py claude/build_template.py skill/scripts/bilingual_lib.py skill/scripts/crop_tools.py; do curl -fsSL "$R/$f" -o "work/tk/${f##*/}" || echo "MISSING $f"; done; curl -fsSL "$R/style.css" -o work/assets/style.css || echo "MISSING style.css"
   ```
   If anything is MISSING (no network): copy `bilingual_lib.py`, `crop_tools.py` from this skill's
   `scripts/` and `style.css` from its `assets/` into the same places, build without the toolkit, and
   say so in one line. Never open the toolkit files.
2. **Prepare:** `python work/tk/prepare.py /mnt/user-data/uploads/FILE …` → prints slide count, word
   count, summary target (≈ ⅓ of the words), visual slides, which sheets to view, and bold/coloured
   text (must-know candidates). Read `work/<stem>/slides.txt` once. View only the listed sheets.
3. **Plan by concepts (in your head, no plan file):** list the concepts; merge slides that repeat; order by
   dependency; group into 3–7 sections; note which concepts students confuse (→ `compare`).
4. **Build:** write `work/build.py` from `work/tk/build_template.py`, then
   `python work/build.py && python work/tk/qa.py OUT --slides work/<stem>/slides.txt`.
   Fix ERROR lines, then WARN lines that matter; re-run once. The page is checked in a headless browser
   by `qa.py`, so do not open it yourself.
5. **Deliver:** the file is in `/mnt/user-data/outputs/`; present it with `present_files` (or the file-send
   tool). One self-contained file per chapter (`chapterN_summary.html`, images inlined), same `work/tk`.
   Reply briefly in the user's language: what the page contains, every gap or uncertainty you flagged
   (cut-off text, unreadable symbols, undefined terms, your own readings), one question to start studying.
6. **Tutor:** one question (or a small related group) at a time, no answer hidden in it; evaluate, say what
   is right, correct with the reason, hint before revealing; return to a weak prerequisite when needed.
   Keep the status table honest (Strong / Needs more practice / Weak / Not yet tested, from real answers
   only). When the material is finished: a final review and a test weighted toward weak areas.

## Page structure (helpers from `study_tools` + `bilingual_lib`)
- `bigpicture(idea_en, idea_ar, center, branches)` — main idea in 1–2 sentences + concept map;
  `branches=[((label, concept_id), [children], "verb"), …]` (plain label if no card).
- Per section `section(n, en, ar, "Slides 3–6", "الشرائح 3–6", [...])`:
  `lead(why_en, builds_on=, leads_to=, why_ar=)` → `concept(cid, name, definition=, plain=, how=[…],
  example=, mistake=, connects=[(id, relation, label)], ar=, src="Slide 4", extra=fig(...)/law(...))` per
  concept → `compare(title, ["", "A", "B"], rows)` → `keypoints([("must-know", True), …])` (≤ 5).
  `warn(en, ar)` for gaps; `dtable(head, rows)` for slide tables. Every exam-relevant picture is embedded
  with `fig(name, slide, cap_en, cap_ar, en, ar)` (`set_image_dir` first): caption, what it shows, how it
  connects to the text; only what is visible; mark anything you cannot read. Every section cites its slides.
- End: `cheatsheet(definitions, formulas, differences, traps)` → `practice(...)` → `status([...])`.
- `add_toolkit(OUT, chapter="Chapter N: Title", gloss={...})`; `gloss` = 40–120 entries, English → Arabic,
  the meaning in this course (not literal), the Arabic term Arabic textbooks use, multi-word terms as their
  own entries ("weak entity", "clock rate"), keys lowercase singular. It is shown above machine translation.

Writing style: compact (≈ ⅓ of the slides' words), simple words, bullets ≤ 15 words and ≤ 5 per list,
start with the key term, no filler. English is the main text; Arabic is one short line per concept, the big
idea and section leads only (never translate whole paragraphs). Course terms stay in English inside Arabic
(`L("term")`). If the user wants one language only, drop the other. Card rows: Definition (verbatim) → In plain
words (one sentence) → How it works (2–4 bullets) → Example → Common mistake → Connects to. Skip empty rows.
Slide emphasis (bold/colour/repeated) → must-know key points and the cheatsheet. Your own simple SVG
diagrams are welcome where they help (flows, formula breakdowns, charts of a slide's numbers): label them
"My diagram (from the slide content)", use only the material's facts, white background (works in dark mode).
Light look by default; ask nothing about format unless the request is ambiguous.

## Formulas
`m("CPU time = [[IC × CPI || f]]")` — `x_i`/`x_{avg}` subscript, `x^2`/`10^{-9}` power, `[[a || b]]`
fraction, `*` → ×; numbers inside sentences through `m()` too. Each law: `law(name_en, name_ar, expr,
[(symbol, meaning_en, meaning_ar, unit)], when_en, when_ar, note_en, note_ar)` (symbols become
hover/tap meanings; same spelling everywhere; extra symbols via `add_toolkit(symbols={...})`).
Then `solved(title_en, title_ar, problem_en, problem_ar, given=[…], find=…, items=[(math, why_en, why_ar)…],
answer=(…), check=(…), src=…)`: one operation per line (law → substitute with units → each step → result),
a short plain-words reason under each step, boxed answer with unit, check by a second method. Units
converted in their own step; round only the final answer (3 s.f. unless the course says otherwise). Use the
course's exact formula and symbols; if the slides show two forms, show both and how they connect.

## Tests (when asked: test / quiz / اختبار)
Parts, each `quiz(title_en, title_ar, [...], sid="partA", mode="instant"|"exam")`: A MCQ `mcq(q_en, q_ar,
[(opt_en, opt_ar)…], answer_index, why_en, why_ar)` · B True/False `tf(...)` · C Fill in the blank (`essay`,
short) · D Calculations (`essay` with `steps(...)` model answers) · E Understanding. ≈ 50–70 questions per
chapter, every section, all slide exercises; every question has `src=` and `ref=`. At most a third recall;
the rest why/explain, apply to "my scenario", compare, find the error, predict. Calculations: direct,
inverse, unit traps, multi-step, compare two cases, find-the-error; distractors from real mistakes.
MCQ distractors are plausible misconceptions; new scenarios use only concepts from the material.
Add `quiz_lang="en"` to `add_toolkit` (English UI, Arabic behind "Show Arabic"); still fill Arabic arguments;
do not add your own toggle or patch labels. Without a test request, end with `practice` (no answers).

## Offline fallback
If the bootstrap fails, this skill's own `scripts/` (`extract_pptx.py`, `render_slides.py`, `crop_tools.py`,
`bilingual_lib.py`) still build a plain page: use `term`, `bi`, `card`, `fig`, `warn`, `review`, `practice`,
`status`, `write_page`, `check_html`, and tell the user the interactive tools were not added.
