#!/usr/bin/env python3
"""Crop diagrams out of rendered slides and check them before embedding.

  python crop_tools.py crop h-06.png L T R B out.png   # box as fractions 0-1 of the slide
  python crop_tools.py blob picture.png out.png        # flatten transparency onto white
  python crop_tools.py stack out.png a.png b.png ...   # stack crops vertically (avoids text between rows)
  python crop_tools.py montage out.png a.png b.png ... # contact sheet to VIEW and verify the crops

Picture positions in pictures.json are fractions of the slide, so use them as the starting box
and pad slightly. After every batch of crops run `montage` and look at it: stray text from
neighbouring bullets at the edges is the usual defect; tighten the box until it is gone.
"""
import sys
from PIL import Image

def crop(src, box, out):
    im = Image.open(src).convert("RGB"); W, H = im.size
    a, b, c, d = box; im.crop((int(a * W), int(b * H), int(c * W), int(d * H))).save(out)

def blob(src, out):
    im = Image.open(src)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA"); bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[3]); im = bg
    im.convert("RGB").save(out)

def stack(files, out, gap=20):
    ims = [Image.open(f).convert("RGB") for f in files]
    w = max(i.size[0] for i in ims); h = sum(i.size[1] for i in ims) + gap * (len(ims) - 1)
    S = Image.new("RGB", (w, h), "white"); y = 0
    for i in ims: S.paste(i, ((w - i.size[0]) // 2, y)); y += i.size[1] + gap
    S.save(out)

def montage(files, out, tw=520):
    ims = [Image.open(f).convert("RGB") for f in files]
    th = [int(i.size[1] * tw / i.size[0]) for i in ims]; rows = (len(ims) + 1) // 2
    rh = [max(th[2 * r:2 * r + 2]) for r in range(rows)]
    M = Image.new("RGB", (2 * tw, sum(rh)), "white"); y = 0
    for r in range(rows):
        for c in range(2):
            k = 2 * r + c
            if k < len(ims): M.paste(ims[k].resize((tw, th[k])), (c * tw, y))
        y += rh[r]
    M.save(out)

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == "crop": crop(a[1], tuple(map(float, a[2:6])), a[6])
    elif a[0] == "blob": blob(a[1], a[2])
    elif a[0] == "stack": stack(a[2:], a[1])
    elif a[0] == "montage": montage(a[2:], a[1])
    else: sys.exit(__doc__)
