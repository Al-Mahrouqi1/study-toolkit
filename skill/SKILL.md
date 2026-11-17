---
name: "detailed-study-summary"
description: التلخيص المفصل — turns uploaded course material (PPTX slides, PDF chapters, lecture notes) into a detailed, source-grounded study summary delivered as one light, modern, large-font HTML file, with every diagram/image from the slides embedded and explained, written in both English and Arabic, and built under strict tutor rules (stay inside the provided material, keep the course's exact definitions and terminology, flag gaps instead of guessing, practice questions without answers). Use this whenever the user uploads slides, chapters or notes and asks to summarize, study, explain, make notes, "لخّص", "التلخيص المفصل", "اشرح الفصل", or prepare for an exam from their course, even if they do not mention HTML, images, Arabic, or this skill by name.
---

# التلخيص المفصل (Detailed Study Summary)

Produce the kind of summary a good tutor would hand a student before an exam: complete, faithful to the
course's own wording, with the original diagrams explained, in English and Arabic, as a clean HTML page.
Then continue as a tutor (quiz, feedback), because a summary alone does not make the student learn.

Why the strictness: the student will be tested on *their* course. Outside knowledge that sneaks in, a
paraphrased definition, or a dropped minor detail can cost marks, and a guessed explanation of an unclear
diagram teaches something wrong. So fidelity beats polish, and honesty about gaps beats a smooth text.
The rules in this file are enough for a normal chapter; open `references/conditions.md` or
`references/html-design.md` only when a case is unclear (they cost time and tokens).

## Keep it short and fast

The user wants complete but compact summaries and quick replies.
- **Complete, not long:** every exam-relevant point and every course definition stays, but in the
  fewest words. Bullets over paragraphs. Simple explanation: 1–2 sentences. Do not repeat the same idea
  in `bi`, `card` and `review`. `review` lists items only, no prose.
- **Arabic is a short gloss**, not a full re-translation: key sentences and explanations only; skip
  Arabic for lists of names, tables, and anything already obvious from the English.
- **Look only where needed:** read `slides.txt` fully, but view rendered slides only for slides that
  have pictures, diagrams, tables or highlighted text (from `pictures.json` and the text). Do not view
  text-only slides. Crop diagrams in one pass and check them with one montage.
- **One build:** write the whole page in one build script, run `check_html()` once, fix only real errors.
- **Short reply:** what the file contains, the gaps you flagged, one question to start. Nothing else.

## Workflow

1. **Inspect the material.** For a PPTX:
   `python scripts/extract_pptx.py FILE.pptx work/` → `slides.txt` (all text, tables, notes) and
   `pictures.json` (picture positions as fractions of the slide). Read `slides.txt` completely.
   For PDF/DOCX use the `pdf` / `docx` skills for text, and `render_slides.py` for page images.
2. **Look at the visual slides.** `python scripts/render_slides.py FILE.pptx work/render` makes numbered
   contact sheets (`sheet_K.png`, four slides each). View the sheets that contain slides with pictures,
   diagrams, tables or colour emphasis; skip sheets that are text only. If a render looks broken, use the
   original picture file from `pictures.json` instead.
3. **Build the learning map** (topics, main concepts, dependencies, recommended order) and split the
   material into sections that follow the chapter's own order.
4. **Crop the diagrams** with `scripts/crop_tools.py` (`crop`, `blob`, `stack`), save as
   `img/c_s<slide>.png`, then `montage` and *view* the result. Fix stray text at the edges. Details and
   the choice between picture file and render crop: `references/html-design.md`.
5. **Write the page** with `scripts/bilingual_lib.py` (start from `assets/build_template.py`). One
   `section()` per topic, containing, in this rhythm: course definitions (`term`), explanation (`bi`),
   the figure with its explanation (`fig`), examples from the slides (`card`/`bil`), tables from the
   slides (`dtable`), gaps and cautions (`warn`), and a `review` box of what appears important.
6. **End the page** with: practice questions without answers (`practice`) including the slides' own
   exercises, and the review-status table (`status`, everything "Not yet tested").
   When the user asks for a test, quiz or mock exam (اختبار), build it with the toolkit's `quiz()`
   (graded `mcq`, `tf`, and `essay` with a model answer). Every question gets `src=` (e.g.
   "Section 3 · Slides 14–19") and `ref=` (the section id) so the student can jump to the source.

   **Questions must test understanding, not only memory.** In every practice set or test, at most
   about a third are recall (define, list). The rest are understanding questions, mixed across:
   - *Why / explain:* why a rule exists, what problem a concept solves.
   - *Apply:* a short new scenario (labelled "my scenario") where the student must use the concept,
     e.g. choose the right construct, classify items, draw or complete a diagram.
   - *Compare:* the difference between two close concepts, when to use one over the other.
   - *Find the error:* a wrong statement, design or example to correct.
   - *Predict / reason:* what happens if a condition changes.
   MCQ distractors are plausible misconceptions, not obviously wrong. Scenarios may be new, but every
   concept and rule they need must come from the provided material.
7. **Add the study toolkit, check, then deliver.** Download the toolkit (no tokens):
   `mkdir -p work/tk && for f in toolkit.css toolkit.js study_tools.py; do curl -fsSL
   "https://raw.githubusercontent.com/Al-Mahrouqi1/study-toolkit/main/$f" -o "work/tk/$f"; done`.
   Then `sys.path.insert(0, "work/tk"); from study_tools import *`, and after `write_page()` call
   `add_toolkit(out, chapter="Chapter N: Title", gloss={...})`. `gloss` maps every course term and hard
   word in the chapter to its Arabic meaning (English → Arabic); it gives instant translation even
   offline. If the download fails, deliver without the toolkit and say so in one line.
   Run `check_html()` once (tag balance, image count) and check against the rules in this file; save to
   `/mnt/user-data/outputs/`, call `present_files`.
8. **Reply briefly** in the user's language: what the file contains, every gap or uncertainty you flagged
   (cut-off text, unreadable symbols, undefined terms, my own readings), that it was validated but not
   opened in a browser, and one question to start tutoring.
9. **Continue as tutor** when the user answers or asks to study: one question (or a small closely related
   group) at a time, no answer hidden in the question, evaluate → say what is right → correct what is wrong
   and why → hint before revealing → move on or return to a shaky prerequisite. Keep the status table
   honest (Strong / Needs more practice / Weak / Not yet tested, from real answers only). When the
   material is finished, give a final review and a test weighted toward weak areas.

## What every section must contain

- **Slide references** ("Slides 14–19") so the student can find the source.
- **Course definition** verbatim + **simple explanation** in both languages (`term`). If the slides give two
  wordings, keep both and say so.
- **Every image/diagram** embedded with a caption, and an explanation of what it shows and how it connects
  to the text. Describe only what is visible or written; mark anything you cannot read reliably.
- **Examples from the slides**; any extra example is labelled as yours ("(my scenario)" / "من وضعي").
- **Emphasis preserved**: things the slide highlights (red, bold, underlined, numbered lists, repeated
  ideas) appear in `review` as "appears important to study". Never write "will be on the exam".
- **Formulas** (if any): formula, meaning, variables, units, conditions, when to use it, an example.
- **Gaps flagged, never filled**: cut-off text, contradictions between slides, terms used but not defined
  in the chapter, pictures that cannot be interpreted. Use `warn()` with the exact line
  "This is not covered in the provided chapters." where relevant. Any outside knowledge, only if truly
  needed, goes under "Additional explanation — not from the provided material:".

## Language and look

The toolkit adds: translation on selection (chapter glossary + online), highlighter, notes, eraser
and undo, source of any text, search, contents with progress, dark mode, font size, export.
Light is the default look.
English first, Arabic directly under it (short), for each explanatory unit. Course terms stay in English inside Arabic
text (`L("term")`). Light, modern, big type: use `assets/style.css` unchanged unless the user asks for a
different look. If the user wants only one language, drop the other half. Ask nothing about format
unless the request is ambiguous; the defaults above are what the user has already approved.

## Output

One self-contained file, e.g. `chapterN_summary_bilingual.html` (images inlined, ~1 MB). Put it in
`/mnt/user-data/outputs/` and present it. For several chapters, make one file per chapter in the same style.

## Scripts and references

- `scripts/extract_pptx.py` text + picture inventory · `scripts/render_slides.py` page images + contact
  sheets · `scripts/crop_tools.py` crop/stack/montage · `scripts/bilingual_lib.py` HTML helpers.
- `assets/style.css` the design · `assets/build_template.py` a runnable skeleton.
- `references/conditions.md` all rules + final checklist · `references/html-design.md` design, bilingual
  rules, image handling, pitfalls.
