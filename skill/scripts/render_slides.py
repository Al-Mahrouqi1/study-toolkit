#!/usr/bin/env python3
"""Render slides to images and build numbered contact sheets for visual review.

Usage: python render_slides.py FILE(.pptx/.docx/.pdf) OUTDIR [--dpi 170]

Writes OUTDIR/h-NN.png (high-res, for cropping) and OUTDIR/sheet_K.png
(2x2 contact sheets, each cell labelled with its slide number, for viewing).
View every sheet before writing: diagrams are often the exam-relevant part.
Caveat: LibreOffice can render a few slides wrongly (rotated/grouped pictures).
If a slide looks broken, take the picture file from pictures.json instead and say so.
"""
import glob, os, subprocess, sys
from PIL import Image, ImageDraw

def main(path, out, dpi=170):
    os.makedirs(out, exist_ok=True)
    pdf = path
    if not path.lower().endswith(".pdf"):
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", out, path],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
        pdf = os.path.join(out, os.path.splitext(os.path.basename(path))[0] + ".pdf")
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", pdf, os.path.join(out, "h")], check=True)
    files = sorted(glob.glob(os.path.join(out, "h-*.png")))
    cell_w = 1000
    for k in range(0, len(files), 4):
        cells = []
        for f in files[k:k + 4]:
            im = Image.open(f).convert("RGB"); r = cell_w / im.size[0]
            im = im.resize((cell_w, int(im.size[1] * r)))
            n = int(os.path.basename(f).split("-")[1].split(".")[0])
            d = ImageDraw.Draw(im); d.rectangle((0, 0, 70, 34), fill=(53, 86, 240)); d.text((8, 8), f"#{n}", fill="white")
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
