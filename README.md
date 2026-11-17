# study-toolkit

Reader tools for bilingual (English/Arabic) study summaries and tests: translation on selection (chapter glossary offline, Google/MyMemory/Lingva online), highlighter with 4 colours + underline, notes, eraser and undo, source of any text (chapter › section › slides), search, table of contents with progress, dark mode, font size, drawing layer (multi-colour pen, marker, text box, eraser), Excalidraw whiteboard (loaded on first open), graded quizzes (MCQ, True/False, written; Arabic shown on demand), autosave and export.

Used by the `detailed-study-summary` skill:

```bash
mkdir -p work/tk && for f in toolkit.css toolkit.js study_tools.py; do
  curl -fsSL "https://raw.githubusercontent.com/Al-Mahrouqi1/study-toolkit/main/$f" -o "work/tk/$f"; done
```

```python
sys.path.insert(0, "work/tk"); from study_tools import *
body += quiz("Chapter 2 test", "اختبار الفصل الثاني", [mcq(...), tf(...), essay(...)])
write_page(out, ...); add_toolkit(out, chapter="Chapter 2: ERD", gloss={"entity": "كيان"})
```

`template.html` is a demo page.

## skill/

The `detailed-study-summary` (التلخيص المفصل) skill, with the toolkit download step, understanding-based
questions, and compact-summary rules. Zip the `skill` folder to upload it to Claude.

## portable/ — works with any AI tool that supports Agent Skills

`portable/detailed-study-summary/` is a spec-valid Agent Skill (checked with `agentskills validate`) for Claude,
Claude Code, ChatGPT, OpenAI Codex, Gemini CLI, Cursor, GitHub Copilot, Windsurf, OpenCode and others.
It bundles the toolkit (works offline), checks the environment first (`scripts/setup_env.py`), and falls back
when LibreOffice, python-pptx, image viewing or internet are missing. Install guide: `portable/INSTALL.md`.
Ready-to-upload archive: `portable/detailed-study-summary.zip`.

When the root toolkit changes, copy `toolkit.css`, `toolkit.js` and `study_tools.py` into
`portable/detailed-study-summary/assets/toolkit/` and rebuild the zip.
