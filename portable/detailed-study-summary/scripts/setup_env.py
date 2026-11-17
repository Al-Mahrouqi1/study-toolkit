#!/usr/bin/env python3
"""Run this FIRST. Prepares the environment and prints a JSON report the agent must follow.

Usage: python <skill>/scripts/setup_env.py [WORKDIR]      (default WORKDIR: ./work)

- Installs missing Python packages if possible (python-pptx, Pillow, PyMuPDF).
- Puts the study toolkit in WORKDIR/tk (latest from GitHub, or the bundled copy if offline).
- Finds where to save the final file (output_dir) for this platform.
- Reports which renderers exist and what to do when something is missing ("notes").
"""
import importlib, json, os, shutil, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
WORK = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "work")
RAW = os.environ.get("STUDY_TOOLKIT_URL", "https://raw.githubusercontent.com/Al-Mahrouqi1/study-toolkit/main/")  # set to "offline" to force the bundled copy
rep = {"python": sys.version.split()[0], "skill_dir": SKILL, "work_dir": WORK, "notes": []}

def importable(mod):
    return subprocess.run([sys.executable, "-c", f"import {mod}"], capture_output=True).returncode == 0

def pip_install(pkg):
    for extra in ([], ["--user"], ["--break-system-packages"]):
        try:
            r = subprocess.run([sys.executable, "-m", "pip", "install", "-q", pkg] + extra,
                               capture_output=True, timeout=240)
            if r.returncode == 0:
                return True
        except Exception:
            pass
    return False

for mod, pkg in (("PIL", "Pillow"), ("pptx", "python-pptx"), ("pymupdf", "pymupdf")):
    ok = importable(mod) or (mod == "pymupdf" and importable("fitz")) or (pip_install(pkg) and (importable(mod) or importable("fitz")))
    rep[pkg] = ok
importlib.invalidate_caches()

rep["libreoffice"] = bool(shutil.which("soffice") or shutil.which("libreoffice"))
rep["pdftoppm"] = bool(shutil.which("pdftoppm"))
rep["can_render_pdf"] = rep["pdftoppm"] or rep["pymupdf"]
rep["can_render_pptx"] = rep["libreoffice"] and rep["can_render_pdf"]

# toolkit: latest from GitHub, else bundled copy
tk = os.path.join(WORK, "tk"); os.makedirs(tk, exist_ok=True)
src = "github"
try:
    if RAW == "offline":
        raise OSError("offline")
    for f in ("toolkit.css", "toolkit.js", "study_tools.py"):
        data = urllib.request.urlopen(RAW + f, timeout=10).read()
        if len(data) < 500:
            raise ValueError("short file")
        open(os.path.join(tk, f), "wb").write(data)
except Exception:
    src = "bundled"
    for f in ("toolkit.css", "toolkit.js", "study_tools.py"):
        shutil.copy(os.path.join(SKILL, "assets", "toolkit", f), tk)
rep["toolkit"] = {"path": tk, "source": src}

# where to save the final HTML
plat, out = "local", None
for cand, name in (("/mnt/user-data/outputs", "claude-app"), ("/mnt/data", "chatgpt")):
    if os.path.isdir(cand) and os.access(cand, os.W_OK):
        plat, out = name, cand
        break
if not out:
    out = os.path.abspath("study-output"); os.makedirs(out, exist_ok=True)
rep["platform_guess"] = plat
rep["output_dir"] = out
rep["deliver"] = {
    "claude-app": "Save in output_dir, then call the present_files tool on the file if it exists.",
    "chatgpt": "Save in output_dir and give the user a download link: sandbox:/mnt/data/<file>.html",
    "local": "Save in output_dir (inside the user's project/folder) and tell the user the full path.",
}[plat]

n = rep["notes"]
if not rep["Pillow"]:
    n.append("Pillow missing and not installable: skip cropping; embed slide pictures as-is or describe them in text, and say so.")
if not rep["python-pptx"]:
    n.append("python-pptx missing: use scripts/extract_pptx_basic.py (no packages needed) instead of extract_pptx.py.")
if not rep["can_render_pptx"]:
    n.append("Cannot render PPTX slides (no LibreOffice or rasterizer): view the picture files in blobs/ instead of contact sheets; for PDFs use PyMuPDF/pdftoppm if available.")
if src == "bundled":
    n.append("No internet: using the bundled toolkit (works fully offline; online translation needs internet when the student opens the page).")
n.append("If you cannot view images, describe diagrams only from slide text and flag each figure as 'not visually checked'.")
print(json.dumps(rep, indent=1))
