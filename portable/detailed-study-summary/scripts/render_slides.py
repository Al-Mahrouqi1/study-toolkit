#!/usr/bin/env python3
"""Render slides/pages to images and build numbered contact sheets (2x2) for visual review.

Usage: python render_slides.py FILE(.pptx/.docx/.pdf) OUTDIR [--dpi 170]

Writes OUTDIR/h-NN.png (one per slide/page) and OUTDIR/sheet_K.png (four per sheet, numbered).
Uses LibreOffice to turn PPTX/DOCX into PDF, then pdftoppm or PyMuPDF to rasterize.
If no renderer is available it exits with code 3 and a message: then use the picture files that
extract_pptx.py saved (pictures.json / blobs/) and say in the summary that slides were not rendered.
"""
import glob, os, shutil, subprocess, sys
from PIL import Image, ImageDraw

def to_pdf(path, out):
    if path.lower().endswith(".pdf"):
        return path
    exe = shutil.which("soffice") or shutil.which("libreoffice")
    if not exe:
        print("NO_RENDERER: LibreOffice not found. Use pictures.json / blobs/ from extract_pptx.py instead.")
        sys.exit(3)
    try:
        subprocess.run([exe, "--headless", "--convert-to", "pdf", "--outdir", out, path],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
    except Exception as e:
        print(f"NO_RENDERER: LibreOffice failed ({e}). Use pictures.json / blobs/ from extract_pptx.py instead.")
        sys.exit(3)
    return os.path.join(out, os.path.splitext(os.path.basename(path))[0] + ".pdf")

def rasterize(pdf, out, dpi):
    if shutil.which("pdftoppm"):
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", pdf, os.path.join(out, "h")], check=True)
        return
    try:
        import pymupdf as fitz
    except ImportError:
        try:
            import fitz  # older PyMuPDF
        except ImportError:
            fitz = None
    if fitz is None:
        print("NO_RENDERER: neither pdftoppm nor PyMuPDF is available (pip install pymupdf).")
        sys.exit(3)
    doc = fitz.open(pdf)
    for i, page in enumerate(doc, 1):
        page.get_pixmap(dpi=dpi).save(os.path.join(out, f"h-{i:02d}.png"))

def main(path, out, dpi=170):
    os.makedirs(out, exist_ok=True)
    rasterize(to_pdf(path, out), out, dpi)
    files = sorted(glob.glob(os.path.join(out, "h-*.png")), key=lambda f: int(os.path.basename(f).split("-")[1].split(".")[0]))
    cell_w = 1000
    for k in range(0, len(files), 4):
        cells = []
        for f in files[k:k + 4]:
            im = Image.open(f).convert("RGB"); r = cell_w / im.size[0]
            im = im.resize((cell_w, int(im.size[1] * r)))
            n = int(os.path.basename(f).split("-")[1].split(".")[0])
            d = ImageDraw.Draw(im); d.rectangle((0, 0, 70, 34), fill=(47, 91, 234)); d.text((8, 8), f"#{n}", fill="white")
            cells.append(im)
        ch = max(c.size[1] for c in cells)
        S = Image.new("RGB", (2 * cell_w, 2 * ch), "white")
        for i, c in enumerate(cells): S.paste(c, ((i % 2) * cell_w, (i // 2) * ch))
        S.save(os.path.join(out, f"sheet_{k // 4 + 1}.png"))
    print(f"{len(files)} pages rendered, {(len(files) + 3) // 4} contact sheets in {out}")

if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    main(a[0], a[1], int(a[a.index("--dpi") + 1]) if "--dpi" in a else 170)
