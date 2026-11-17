#!/usr/bin/env python3
"""Dump everything useful from a .pptx so nothing in the slides is missed.

Usage: python extract_pptx.py deck.pptx OUTDIR

Writes:
  OUTDIR/slides.txt     text of every slide (placeholders, groups, tables, notes)
  OUTDIR/pictures.json  every picture: slide, name, position as fractions of the slide,
                        and the saved file if Pillow can open it ("unreadable" for WMF/EMF)
  OUTDIR/blobs/         picture files Pillow could open (converted to PNG, white background)
Prints slides that have no text at all (picture-only slides: look at them visually).
"""
import io, json, os, sys
from pptx import Presentation
from PIL import Image

def walk_text(shapes, out):
    for sh in shapes:
        if sh.shape_type == 6:                       # group
            walk_text(sh.shapes, out)
        if sh.has_text_frame and sh.text_frame.text.strip():
            out.append(sh.text_frame.text.strip())
        if getattr(sh, "has_table", False) and sh.has_table:
            for r in sh.table.rows:
                out.append(" | ".join(c.text for c in r.cells))

def walk_pics(shapes, slide, n, W, H, rows, blobdir):
    for sh in shapes:
        if sh.shape_type == 6:
            walk_pics(sh.shapes, slide, n, W, H, rows, blobdir); continue
        if sh.shape_type != 13:
            continue
        info = dict(slide=n, name=sh.name, left=round(sh.left / W, 3), top=round(sh.top / H, 3),
                    width=round(sh.width / W, 3), height=round(sh.height / H, 3), file="unreadable")
        try:   # avoid sh.image.ext: it raises on WEBP; go through the relationship instead
            blob = slide.part.related_part(sh._element.blipFill.blip.rEmbed).blob
            im = Image.open(io.BytesIO(blob))
            if im.mode in ("RGBA", "LA", "P"):
                im = im.convert("RGBA"); bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[3]); im = bg
            else:
                im = im.convert("RGB")
            path = os.path.join(blobdir, f"s{n}_{sh.shape_id}.png"); im.save(path)
            info["file"] = path; info["size"] = list(im.size)
        except Exception:
            pass
        rows.append(info)

def main(pptx, out):
    os.makedirs(os.path.join(out, "blobs"), exist_ok=True)
    p = Presentation(pptx); W, H = p.slide_width, p.slide_height
    lines, pics, empty = [], [], []
    for n, s in enumerate(p.slides, 1):
        t = []; walk_text(s.shapes, t)
        lines.append(f"--- Slide {n}"); lines += t
        if s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip():
            lines.append("NOTES: " + s.notes_slide.notes_text_frame.text.strip())
        if not t: empty.append(n)
        walk_pics(s.shapes, s, n, W, H, pics, os.path.join(out, "blobs"))
    open(os.path.join(out, "slides.txt"), "w", encoding="utf-8").write("\n".join(lines))
    json.dump(pics, open(os.path.join(out, "pictures.json"), "w"), indent=1)
    print(f"{len(p.slides)} slides, {len(pics)} pictures. Slides with no text: {empty}")

if __name__ == "__main__":
    if len(sys.argv) != 3: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
