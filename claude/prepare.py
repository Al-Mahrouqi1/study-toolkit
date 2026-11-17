#!/usr/bin/env python3
"""One-shot preparation for the Claude edition of detailed-study-summary.

Usage: python work/tk/prepare.py FILE [FILE ...] [--out work]

For each PPTX/PDF/DOCX:
  work/<stem>/slides.txt      all text, slide by slide (tables as "a | b", notes)
  work/<stem>/blobs/          embedded pictures (PNG), pictures.json with positions (PPTX)
  work/<stem>/render/h-NN.png one image per slide (if LibreOffice/pdftoppm/PyMuPDF exist)
  work/<stem>/sheets/sheet_K.png  3x3 numbered contact sheets of the VISUAL slides only (≤1568 px)
  work/<stem>/zoom/sNN.png    1200 px single slides for close reading of a diagram
  work/<stem>/digest.json     per slide: words, pictures, tables, charts, diagram shapes, emphasis
Prints a short digest: which slides are visual and which sheet to view. View only those sheets.
"""
import json, os, re, shutil, subprocess, sys

def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

def pptx_info(path, out):
    from pptx import Presentation
    from pptx.util import Emu
    from PIL import Image
    import io
    prs = Presentation(path)
    W, H = prs.slide_width, prs.slide_height
    os.makedirs(os.path.join(out, "blobs"), exist_ok=True)
    lines, pics, info = [], [], []
    def walk(shapes, n, acc):
        for s in shapes:
            st = s.shape_type
            if st == 6:
                walk(s.shapes, n, acc); continue
            if getattr(s, "has_text_frame", False) and s.has_text_frame and s.text_frame.text.strip():
                acc["text"].append(s.text_frame.text.strip())
                for p in s.text_frame.paragraphs:
                    for r in p.runs:
                        try:
                            col = r.font.color.rgb if r.font.color and r.font.color.type is not None else None
                        except Exception:
                            col = None
                        if r.font.bold or r.font.underline or (col is not None and str(col) not in ("000000", "FFFFFF")):
                            if r.text.strip():
                                acc["emph"].append(r.text.strip())
            if getattr(s, "has_table", False) and s.has_table:
                acc["tables"] += 1
                for row in s.table.rows:
                    acc["text"].append(" | ".join(c.text.strip() for c in row.cells))
            if getattr(s, "has_chart", False) and s.has_chart:
                acc["charts"] += 1
            if st == 13:  # picture
                acc["pics"] += 1
                k = acc["pics"]
                name = f"s{n}_{k}.png"
                try:
                    im = Image.open(io.BytesIO(s.image.blob))
                    if im.mode in ("RGBA", "LA", "P"):
                        bg = Image.new("RGB", im.size, "white"); im = im.convert("RGBA"); bg.paste(im, mask=im.split()[-1]); im = bg
                    im.convert("RGB").save(os.path.join(out, "blobs", name)); f = name
                except Exception:
                    f = "unreadable"
                pics.append({"slide": n, "file": f, "x": round(s.left / W, 3) if s.left is not None else None,
                             "y": round(s.top / H, 3) if s.top is not None else None,
                             "w": round(s.width / W, 3) if s.width else None, "h": round(s.height / H, 3) if s.height else None})
            elif st in (1, 5, 9):    # autoshapes, freeforms, lines → parts of a drawn diagram
                acc["shapes"] += 1
    for n, slide in enumerate(prs.slides, 1):
        acc = {"text": [], "emph": [], "tables": 0, "charts": 0, "pics": 0, "shapes": 0}
        walk(slide.shapes, n, acc)
        lines.append(f"===== Slide {n} =====")
        lines += acc["text"]
        if slide.has_notes_slide:
            t = slide.notes_slide.notes_text_frame.text.strip()
            if t:
                lines.append("[notes] " + t.replace("\n", " / "))
        words = sum(len(t.split()) for t in acc["text"])
        info.append({"slide": n, "words": words, "pictures": acc["pics"], "tables": acc["tables"], "charts": acc["charts"],
                     "diagram_shapes": acc["shapes"], "emphasis": sorted(set(acc["emph"]))[:8]})
    open(os.path.join(out, "slides.txt"), "w", encoding="utf-8").write("\n".join(lines))
    json.dump(pics, open(os.path.join(out, "pictures.json"), "w"), indent=1)
    return info

def pdf_info(path, out):
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz
    doc = fitz.open(path); lines, info = [], []
    for n, page in enumerate(doc, 1):
        t = page.get_text().strip()
        lines += [f"===== Page {n} =====", t]
        info.append({"slide": n, "words": len(t.split()), "pictures": len(page.get_images()), "tables": 0, "charts": 0,
                     "diagram_shapes": len(page.get_drawings()) // 8, "emphasis": []})
    open(os.path.join(out, "slides.txt"), "w", encoding="utf-8").write("\n".join(lines))
    return info

def render(path, out):
    rd = os.path.join(out, "render"); os.makedirs(rd, exist_ok=True)
    pdf = path
    if not path.lower().endswith(".pdf"):
        exe = shutil.which("soffice") or shutil.which("libreoffice")
        if not exe:
            return []
        r = sh([exe, "--headless", "--convert-to", "pdf", "--outdir", rd, path], timeout=300)
        pdf = os.path.join(rd, os.path.splitext(os.path.basename(path))[0] + ".pdf")
        if not os.path.exists(pdf):
            return []
    if shutil.which("pdftoppm"):
        sh(["pdftoppm", "-r", "110", "-png", pdf, os.path.join(rd, "h")])
    else:
        try:
            import pymupdf as fitz
        except ImportError:
            try:
                import fitz
            except ImportError:
                return []
        for i, p in enumerate(fitz.open(pdf), 1):
            p.get_pixmap(dpi=110).save(os.path.join(rd, f"h-{i:02d}.png"))
    files = [f for f in os.listdir(rd) if re.match(r"h-\d+\.png$", f)]
    return sorted((int(re.findall(r"\d+", f)[0]), os.path.join(rd, f)) for f in files)

def sheets(pages, visual, out):
    from PIL import Image, ImageDraw
    sd, zd = os.path.join(out, "sheets"), os.path.join(out, "zoom")
    os.makedirs(sd, exist_ok=True); os.makedirs(zd, exist_ok=True)
    sel = [(n, f) for n, f in pages if n in visual]
    for n, f in sel:
        im = Image.open(f).convert("RGB"); r = 1200 / im.size[0]
        im.resize((1200, int(im.size[1] * r))).save(os.path.join(zd, f"s{n:02d}.png"))
    cw, made = 520, []
    for k in range(0, len(sel), 9):
        cells = []
        for n, f in sel[k:k + 9]:
            im = Image.open(f).convert("RGB"); r = cw / im.size[0]; im = im.resize((cw, int(im.size[1] * r)))
            d = ImageDraw.Draw(im); d.rectangle((0, 0, 58, 26), fill=(47, 91, 234)); d.text((6, 6), f"#{n}", fill="white")
            cells.append(im)
        ch = max(c.size[1] for c in cells); rows = (len(cells) + 2) // 3
        S = Image.new("RGB", (3 * cw, rows * ch), "white")
        for i, c in enumerate(cells): S.paste(c, ((i % 3) * cw, (i // 3) * ch))
        name = os.path.join(sd, f"sheet_{k // 9 + 1}.png"); S.save(name); made.append((name, [n for n, _ in sel[k:k + 9]]))
    return made

def main(files, root):
    for path in files:
        stem = re.sub(r"[^\w-]+", "_", os.path.splitext(os.path.basename(path))[0])[:40]
        out = os.path.join(root, stem); os.makedirs(out, exist_ok=True)
        ext = path.lower().rsplit(".", 1)[-1]
        if ext == "pptx":
            info = pptx_info(path, out)
        elif ext == "pdf":
            info = pdf_info(path, out)
        else:
            exe = shutil.which("soffice") or shutil.which("libreoffice")
            sh([exe, "--headless", "--convert-to", "pdf", "--outdir", out, path], timeout=300)
            path = os.path.join(out, stem + ".pdf"); info = pdf_info(path, out)
        visual = {d["slide"] for d in info if d["pictures"] or d["tables"] or d["charts"] or d["diagram_shapes"] >= 4 or d["words"] < 8}
        pages = render(path, out)
        made = sheets(pages, visual, out) if pages else []
        json.dump(info, open(os.path.join(out, "digest.json"), "w"), indent=1, ensure_ascii=False)
        words = sum(d["words"] for d in info)
        print(f"## {os.path.basename(path)} → {out}")
        print(f"slides: {len(info)} · words: {words} · target summary ≈ {max(150, words // 3)} words · rendered: {'yes' if pages else 'NO (use blobs/)'}")
        print("visual slides:", ", ".join(map(str, sorted(visual))) or "none")
        for name, ns in made:
            print(f"view {name}  (slides {', '.join(map(str, ns))})")
        emph = [f"{d['slide']}: {'; '.join(d['emphasis'][:4])}" for d in info if d["emphasis"]]
        if emph:
            print("emphasis (bold/colour/underline) → must-know candidates:")
            for e in emph[:25]:
                print("  " + e[:140])
        print(f"text: {out}/slides.txt · zoom a diagram: {out}/zoom/sNN.png")

if __name__ == "__main__":
    a = sys.argv[1:]
    root = a[a.index("--out") + 1] if "--out" in a else "work"
    fl = [x for x in a if x != "--out" and x != root]
    if not fl:
        sys.exit(__doc__)
    main(fl, root)
