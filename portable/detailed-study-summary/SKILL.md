---
name: detailed-study-summary
description: Detailed Study Summary (التلخيص المفصل). Turns course slides, PDF chapters or lecture notes into one compact, source-faithful HTML study page with concept cards, explained diagrams, formulas solved step by step, graded tests and a review sheet, in English with short Arabic. Use when the user shares course material and asks to summarize, explain, study, make notes or a test, or writes لخّص / اشرح الفصل / اختبار.
license: MIT
compatibility: Needs Python 3.9+ and permission to run commands and write files. Image viewing, internet (GitHub) and LibreOffice make it better; bundled fallbacks cover their absence.
metadata:
  author: Eyad Al-Mahrouqi
  version: "2.0"
  repository: https://github.com/Al-Mahrouqi1/study-toolkit
---

# Detailed Study Summary

Make the page a good tutor would hand a student before an exam: complete for the exam, short to read,
faithful to the course's own wording, with ideas linked. Then keep tutoring.

All paths below are relative to this skill's folder (the folder containing this file); call it SKILL_DIR.

## Step 0 — prepare the environment (always first)

Run `python SKILL_DIR/scripts/setup_env.py work` (use `python3` if `python` is missing).
It prints JSON. Follow it exactly:
- `toolkit.path` → add it to `sys.path` in your build script (it contains `study_tools.py`).
- `output_dir` and `deliver` → where to save the final file and how to hand it to the user.
- `notes` → what to do because something is missing (no renderer, no package, no internet).
If you cannot run commands at all, read `references/platforms.md` → "No code execution".
Tool-specific behaviour (Claude, ChatGPT, Codex, Gemini CLI, Cursor, Copilot, …): `references/platforms.md`.

## Golden rules (never break)

1. The uploaded material is the only source. Never add outside facts silently; if one is truly needed,
   put it under "Additional explanation — not from the provided material:".
2. Course definitions are copied verbatim. Only explanations are simplified.
3. Gaps are flagged, never filled: cut-off text, unreadable symbols, undefined terms →
   `warn("... This is not covered in the provided chapters.")`.
4. Every number is computed in Python, never in your head; each answer is checked a second way.
5. Your own examples or scenarios are labelled "my example". Never write "will be on the exam".
6. Write the whole page with one build script; run `check_html()` once; fix only real errors.

## Workflow

1. **Extract.** PPTX: `python SKILL_DIR/scripts/extract_pptx.py FILE work/` (if python-pptx is missing:
   `extract_pptx_basic.py`). PDF: extract text with PyMuPDF (`pymupdf`) or `pdftotext`. Read `slides.txt` fully.
2. **Look at visual slides only.** `python SKILL_DIR/scripts/render_slides.py FILE work/render` → view the
   `sheet_K.png` files that contain pictures, diagrams, tables or coloured emphasis. Exit code 3 means no
   renderer: view `work/blobs/` instead. If you cannot view images, follow the note in the setup report.
3. **Plan by concepts, not slides** — the method in `references/method.md` (concept list, dependency
   order, 3–7 sections).
4. **Crop diagrams** with `scripts/crop_tools.py` (`crop`, `blob`, `stack`, `montage`); check one montage.
5. **Build the page** in one Python script (template: `assets/build_template.py`):
   `bigpicture` → per section `lead`, `concept` cards, `compare`, `fig`, `law`/`solved`, `keypoints` →
   `cheatsheet` → `practice` → `status`. Formulas and math: `references/math.md`.
   Finish with `add_toolkit(out, chapter="Chapter N: Title", gloss={...})`.
6. **Tests** (when asked for a test/quiz/اختبار): `references/tests.md`; use `quiz_lang="en"`.
7. **Deliver** to `output_dir` as the setup report says. Reply briefly in the user's language: what the
   file contains, the gaps you flagged, one question to start studying.
8. **Tutor**: one question at a time, evaluate, correct with the reason, hint before revealing.

## Style defaults (the user's choices)

- Compact: about a third of the slides' word count, no repeated ideas, bullets ≤ 15 words, ≤ 5 per list.
- Simple words in explanations; English is the main text; Arabic only as one short line per concept,
  the big idea and section leads (never translate whole paragraphs).
- `gloss`: 40–120 entries, English → Arabic, the meaning in this course (not literal), multi-word terms
  included, keys lowercase singular. It powers the page's offline translation.
- Light look by default; the toolkit adds dark mode, translation, highlighter, notes, drawing,
  whiteboard, search, keyboard shortcuts and export.

## Files

- `scripts/setup_env.py` environment check + toolkit + output folder · `scripts/extract_pptx.py`,
  `extract_pptx_basic.py` text and pictures · `scripts/render_slides.py` page images and contact sheets ·
  `scripts/crop_tools.py` image crops · `scripts/bilingual_lib.py` page shell, `fig`, `warn`, `dtable`.
- `assets/toolkit/` bundled toolkit (`study_tools.py` blocks, CSS, JS) · `assets/build_template.py`.
- `references/method.md` summary method · `tests.md` tests · `math.md` formulas and accuracy ·
  `platforms.md` per-tool notes · `markup.md` raw HTML for tools without Python · `conditions.md` full rules.
