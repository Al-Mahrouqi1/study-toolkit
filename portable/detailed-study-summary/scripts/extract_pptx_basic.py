#!/usr/bin/env python3
"""Fallback PPTX extractor with NO third-party packages (use when python-pptx cannot be installed).

Usage: python extract_pptx_basic.py deck.pptx OUTDIR

Writes OUTDIR/slides.txt (text of every slide in order, tables as "a | b", speaker notes) and
OUTDIR/blobs/ (every embedded picture file, named s<slide>_<n>.<ext>) plus OUTDIR/pictures.json
(slide -> picture files; no positions). Less precise than extract_pptx.py but never fails to import.
"""
import json, os, re, sys, zipfile
from xml.etree import ElementTree as ET

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

def slide_order(z):
    rels = ET.fromstring(z.read("ppt/_rels/presentation.xml.rels"))
    target = {r.get("Id"): r.get("Target") for r in rels}
    pres = ET.fromstring(z.read("ppt/presentation.xml"))
    ids = [s.get(R + "id") for s in pres.iter() if s.tag.endswith("}sldId")]
    return ["ppt/" + target[i].lstrip("/").replace("ppt/", "") for i in ids if i in target]

def paras(xml):
    """Text in document order: each paragraph on its own line, each table row as 'a | b'."""
    out = []
    def walk(el):
        for ch in el:
            if ch.tag == A + "tbl":
                for tr in ch.iter(A + "tr"):
                    out.append(" | ".join("".join(t.text or "" for t in tc.iter(A + "t")).strip() for tc in tr.iter(A + "tc")))
            elif ch.tag == A + "p":
                t = "".join(x.text or "" for x in ch.iter(A + "t")).strip()
                if t:
                    out.append(t)
            else:
                walk(ch)
    walk(ET.fromstring(xml))
    return out

def main(path, out):
    os.makedirs(os.path.join(out, "blobs"), exist_ok=True)
    z = zipfile.ZipFile(path)
    lines, pics = [], {}
    for n, sp in enumerate(slide_order(z), 1):
        lines.append(f"===== Slide {n} =====")
        lines += paras(z.read(sp))
        relp = os.path.join(os.path.dirname(sp), "_rels", os.path.basename(sp) + ".rels")
        if relp in z.namelist():
            rels = ET.fromstring(z.read(relp))
            k = 0
            for r in rels:
                tgt, typ = r.get("Target"), r.get("Type", "")
                full = os.path.normpath(os.path.join(os.path.dirname(sp), tgt)).replace("\\", "/")
                if typ.endswith("/image") and full in z.namelist():
                    k += 1
                    name = f"s{n}_{k}{os.path.splitext(full)[1].lower()}"
                    open(os.path.join(out, "blobs", name), "wb").write(z.read(full))
                    pics.setdefault(n, []).append(name)
                if typ.endswith("/notesSlide") and full in z.namelist():
                    notes = [t for t in paras(z.read(full)) if not re.fullmatch(r"\d+", t)]
                    if notes:
                        lines.append("[notes] " + " / ".join(notes))
    open(os.path.join(out, "slides.txt"), "w", encoding="utf-8").write("\n".join(lines))
    json.dump(pics, open(os.path.join(out, "pictures.json"), "w"), indent=1)
    print(f"{n} slides, {sum(len(v) for v in pics.values())} pictures -> {out}")

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
