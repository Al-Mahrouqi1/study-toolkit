# Notes per tool

The skill follows the open Agent Skills format and only needs: read this folder, run Python, write files.
`setup_env.py` detects most of the platform for you; this file covers what it cannot.

| Tool | Save the final file to | Give it to the user | Watch out |
|---|---|---|---|
| Claude (claude.ai / desktop / mobile) | `/mnt/user-data/outputs/` | `present_files` tool | Network may be limited; bundled toolkit is used automatically |
| Claude Code | `./study-output/` | Tell the full path | Commands may need approval |
| ChatGPT (with code / skills) | `/mnt/data/` | Link `sandbox:/mnt/data/<file>.html` | Usually no internet and no pip: rely on bundled toolkit, `extract_pptx_basic.py`, PyMuPDF if present |
| OpenAI Codex (CLI / app) | `./study-output/` | Tell the path | Sandbox may block network: bundled toolkit works offline |
| Gemini CLI | `./study-output/` | Tell the path | Approve shell commands when asked |
| Cursor / Windsurf / Cline / OpenCode | `./study-output/` | Tell the path | Agent/terminal mode must be on to run Python |
| GitHub Copilot (VS Code / CLI) | `./study-output/` | Tell the path | Use Agent mode; terminal commands need approval |

Requirements on the user's own computer (local tools): Python 3.9+. Optional: LibreOffice (renders PPTX
slides), poppler `pdftoppm` (fast PDF pages). `setup_env.py` installs Python packages it can.

## When something is missing
- **No image viewing:** describe figures only from slide text and captions; mark each figure
  "(not visually checked)". Do not invent what a diagram shows.
- **No renderer (exit code 3):** use pictures from `work/blobs/` (from the extractor) instead of contact sheets.
- **No python-pptx and no pip:** `scripts/extract_pptx_basic.py` needs only the standard library.
- **No Pillow:** skip cropping; embed blob images directly or describe them; say so in the reply.
- **No internet:** nothing to do — the bundled toolkit is used and the page works offline (online
  translation in the page will work later when the student has internet).

## No code execution (chat-only models)
Write the HTML yourself following `references/markup.md`: it shows the exact markup of every block and a
page skeleton that loads the toolkit from
`https://cdn.jsdelivr.net/gh/Al-Mahrouqi1/study-toolkit@main/toolkit.css` and `.../toolkit.js`.
Give the full file in one code block named `chapterN_summary.html`. All golden rules still apply; do the
arithmetic carefully and show each step.
