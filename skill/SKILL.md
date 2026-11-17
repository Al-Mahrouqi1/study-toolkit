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
  fewest words (target: the summary has about a third of the slides' word count). Never repeat an idea.
- **No English/Arabic duplication:** English is the main text. Arabic appears only as one short line per
  concept (`concept(ar=...)`), the big idea, and section `lead`s. Never translate bullets, tables or
  whole paragraphs; the reader translates anything else with the toolkit (glossary + selection).
- **Simple words:** explanations (English and Arabic) use plain, everyday words and short sentences,
  like explaining to a friend. Course definitions stay verbatim; only the explanations are simplified.
- **Illustrative diagrams:** besides the slides' own figures, add your own simple inline SVG diagrams
  wherever a picture makes an idea easier (flows, formula breakdowns, before/after bars, charts of a
  slide's numbers). Label each "My diagram (from the slide content)", use only facts and numbers from
  the material (or your clearly labelled working), draw on a white background so it works in dark mode,
  and screenshot them once to check nothing is clipped.
- **Look only where needed:** read `slides.txt` fully, but view rendered slides only for slides that
  have pictures, diagrams, tables or highlighted text (from `pictures.json` and the text). Do not view
  text-only slides. Crop diagrams in one pass and check them with one montage.
- **One build:** write the whole page in one build script, run `check_html()` once, fix only real errors.
- **Short reply:** what the file contains, the gaps you flagged, one question to start. Nothing else.

## How to summarize (the method)

A summary is not the slides in order. Rebuild the chapter around its concepts and how they connect.
1. **List the concepts** from `slides.txt` (terms, laws, processes, components). Merge slides that
   repeat or continue the same idea. Note for each concept what it depends on and what it leads to.
2. **Order by dependency** (what you must know first), keeping the chapter's order when it already works.
   Group concepts into 3–7 sections.
3. **Open the page with `bigpicture()`**: the chapter's main idea in 1–2 sentences + a concept map of
   the sections and their concepts, with a short verb on each link ("stores", "measured by", "causes").
4. **Each section** = `lead()` (why it matters, builds on → leads to) → one `concept()` card per concept
   → `compare()` for any two or more concepts students mix up → slide figures inside the card they
   explain (`extra=`) → `keypoints()` (max 5, most important first, mark the must-knows).
5. **Concept card rows** (skip empty ones, never pad): Definition (course wording, verbatim) → In plain
   words (one sentence) → How it works (2–4 bullets: parts, steps, rules) → Example (from the slides,
   or labelled "my example") → Common mistake → Connects to (links to other cards with the relation).
6. **Bullets:** one idea each, max ~15 words, start with the key term, same grammar across a list,
   most important first, max 5 per list. No filler ("It is important to note that…").
7. **End the page with `cheatsheet()`**: all definitions in one line each, all formulas, "don't confuse"
   pairs, and exam traps, so the student can revise the chapter from one screen.

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
5. **Write the page** with `scripts/bilingual_lib.py` (start from `assets/build_template.py`), plus the
   study toolkit helpers. First download the toolkit (no tokens; never open or read these files):
   `mkdir -p work/tk && for f in toolkit.css toolkit.js study_tools.py; do curl -fsSL
   "https://raw.githubusercontent.com/Al-Mahrouqi1/study-toolkit/main/$f" -o "work/tk/$f"; done`, then
   `sys.path.insert(0, "work/tk"); from study_tools import *` (gives `m`, `law`, `steps`, `solved`,
   `quiz`, `mcq`, `tf`, `essay`, `add_toolkit`, `bigpicture`, `lead`, `concept`, `compare`,
   `keypoints`, `cheatsheet`). Build the page with the method above: `bigpicture()` first, then one
   `section()` per group of concepts using `lead`, `concept`, `compare`, `fig`, `law`/`solved`,
   `dtable`, `warn` and `keypoints`. Do not use `term`, `bi`, `card` or `review` for new summaries.
6. **End the page** with: `cheatsheet()`, practice questions without answers (`practice`) including
   the slides' own exercises, and the review-status table (`status`, everything "Not yet tested").
   When the user asks for a test, quiz or mock exam (اختبار), build it with the toolkit's `quiz()`
   (graded `mcq`, `tf`, and `essay` with a model answer). Every question gets `src=` (e.g.
   "Section 3 · Slides 14–19") and `ref=` (the section id) so the student can jump to the source.

   **Test format (user's standing rules):**
   - **English only by default.** Call `add_toolkit(..., quiz_lang="en")`: quiz labels become English and
     the Arabic is hidden behind a built-in "Show Arabic" button. Still fill every Arabic argument. Do not
     add your own toggle or patch labels.
   - **Many questions, every type.** Split the test into parts, each its own `quiz()`: A Multiple choice,
     B True/False, C Fill in the blank (`essay` with a short answer), D Calculations (when the chapter has
     formulas), E Understanding (explain, predict, find the error, compare). Aim for roughly 50–70
     questions for a normal chapter, covering every section, and include all of the slides' own exercises
     and question-bank items.
   - **Formula questions are solved step by step** with `steps()` as the model answer (or MCQ
     explanation): law → substitution with units → one arithmetic operation per step → boxed answer →
     check by a second formula or method when the chapter offers one.
   - **Problem design:** for each law, write several kinds of problems: direct (find the result),
     inverse (solve for another variable), unit conversion traps (GHz→Hz, ms→s, %), multi-step
     (chain two laws), compare two cases (which is faster / by how much), and find-the-error in a wrong
     solution. Use realistic numbers that give clean results. MCQ distractors come from real mistakes
     (forgot to convert units, inverted the ratio, used the wrong variable, rounding too early).

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
7. **Add the study toolkit, check, then deliver.** After `write_page()` call
   `add_toolkit(out, chapter="Chapter N: Title", gloss={...})` (add `quiz_lang="en"` for tests).
   `gloss` maps every course term and hard word in the chapter to its Arabic meaning (English → Arabic);
   it gives instant translation even offline and is shown first, above the machine translation, so make it
   precise: the meaning **in this course** (not a literal or everyday meaning), the Arabic term Arabic
   textbooks use, multi-word terms as their own entries ("weak entity", "clock rate"), 40–120 entries per
   chapter, keys in lowercase singular. If the download fails, deliver without the toolkit and say
   so in one line.
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
- **Course definition** verbatim + **plain-words sentence** in a `concept()` card. If the slides give two
  wordings, keep both and say so.
- **Every image/diagram** embedded with a caption, and an explanation of what it shows and how it connects
  to the text. Describe only what is visible or written; mark anything you cannot read reliably.
- **Your own illustrative diagrams** where they help (see "Illustrative diagrams" above), each with a
  short, simple explanation.
- **Examples from the slides**; any extra example is labelled as yours ("(my scenario)" / "من وضعي").
- **Emphasis preserved**: things the slide highlights (red, bold, underlined, numbered lists, repeated
  ideas) become must-know `keypoints` and appear in the `cheatsheet`. Never write "will be on the exam".
- **Formulas** (if any): every law goes in `law(name_en, name_ar, expr, variables, when, watch_out)`,
  a coloured boxed card with the formula, a table of each symbol (meaning, unit), when to use it and the
  common mistake. Then at least one `solved()` worked example from the slides (or labelled "my
  example"): Given / Find, then `steps()` with **one step per line** (law → substitute → each
  operation → result), a short plain-words reason under each step, a boxed answer with unit, and a check.
  Write all math with `m()`: `x_i` / `x_{avg}` subscript, `x^2` / `10^{-9}` power, `[[a || b]]`
  fraction (nestable), `*` → ×. Put numbers inside sentences through `m()` too.
  Every symbol in a law's `variables` becomes hoverable/tappable everywhere it appears in `m()` math
  (shows meaning, Arabic, unit). For symbols used outside a `law()` box, pass
  `add_toolkit(..., symbols={"V": ("Voltage", "الجهد", "V")})`. Use the same symbol spelling in every
  `m()` (e.g. `R_th` both in the law and in the steps).
- **Gaps flagged, never filled**: cut-off text, contradictions between slides, terms used but not defined
  in the chapter, pictures that cannot be interpreted. Use `warn()` with the exact line
  "This is not covered in the provided chapters." where relevant. Any outside knowledge, only if truly
  needed, goes under "Additional explanation — not from the provided material:".

## Math accuracy (strict)

- **Compute every number in Python**, never in your head; paste the exact results into the steps.
- Keep units through every step; convert units in their own step before substituting.
- Round only the final answer (3 significant figures unless the course does otherwise), and say so.
- Use the course's exact formula and symbols; if the slides show two forms, show both and how they connect.
- Re-derive each answer a second way (other formula, units check, or plugging back) before publishing;
  if the two disagree, fix it before writing.

## Language and look

The toolkit adds: translation on selection (chapter glossary + online), highlighter, notes, eraser
and undo, source of any text, search, contents with progress, dark mode, font size, export, drawing on
the page (multi-colour pen, marker, text box, eraser), an Excalidraw whiteboard, and math styling.
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