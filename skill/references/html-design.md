# Page design, bilingual rules and pitfalls

## Look
Light, modern, large type. The CSS in `assets/style.css` already does this; use it as is.
- Root font 20px, body 1.08rem, headings 800 weight; `Manrope` for Latin and `IBM Plex Sans Arabic`
  for Arabic (Google Fonts with system fallbacks, so the file still works offline).
- Cool near-white page (#F6F8FC), white cards with hairline borders, one blue accent (#3556F0),
  soft blue explanation panels, amber `warn` notes, a blue left rule on every "For review" box.
- Single column, max width ~62rem; two-column grids only for cards and paired definitions.
- No dark mode, no animations, no decorative effects. Readability first.

## Bilingual rules
- The page is `dir="ltr"`. Each explanatory unit is English first, Arabic directly below (`bi()`).
  Arabic blocks carry `dir="rtl"`; English terms inside Arabic text go through `L("...")`.
- Course definitions stay in the slide's language (`term()`); the simple explanation is in both.
- Headings are bilingual (English title, smaller Arabic subtitle).
- Use "ي" and "ك" Arabic forms and plain Arabic punctuation (، ؛ ؟). Translate meaning, keep course
  terms in English in parentheses or via `L()`.
- If the user asks for Arabic only or English only, drop the other half in each helper (or call
  `bi()` with the unwanted side as an empty string and hide `.e` / `.a` in CSS).

## Images
- Render with `scripts/render_slides.py`, **view every contact sheet**, then crop each diagram.
- Crop boxes: start from `pictures.json` positions (fractions of the slide); pad a little.
- Prefer the original picture file (`blobs/`) when it exists and is readable: it is sharper and has
  none of the neighbouring slide text. Use a render crop when the picture is WMF/EMF (Pillow cannot
  open them) or when the diagram is drawn with shapes rather than as a picture.
- A slide that renders distorted (rotated or grouped pictures) is a rendering artefact: use the
  picture file instead and mention it in the explanation.
- When text overlaps a picture on the slide (the slide's own layout flaw), crop around it and note
  that part of the slide text is hidden behind the picture.
- Stack rows (`crop_tools.py stack`) when bullets sit between picture rows.
- Always `montage` the crops and look at them; fix stray text at the edges. Decorative icons that
  carry no study content are skipped, and the skip is stated at the end of the page.
- Images are embedded as base64 JPEG (max ~1100px wide, smaller for small diagrams) so the HTML is a
  single file. Typical result: 0.6 to 1 MB.

## Pitfalls seen in practice
- `sh.image.ext` raises on WEBP; read the blob through the slide relationship (done in extract_pptx.py).
- f-strings: `{Name}` is evaluated as a variable. Double the braces or wrap in `L("{Name}")`.
- `mkdir -p a/{b,c}` fails in `/bin/sh`; list directories explicitly.
- Cardinality/crow's-foot symbols and small connectors are often unreadable at slide size. Zoom a
  2x crop before describing them; if still unclear, give only the labels the slide itself prints.
- Placeholder bullets sometimes export as odd glyphs (□); ignore the glyph, keep the text.
- Slide text with typos ("underlying" for "underlining", "may he optional"): quote definitions
  verbatim but add a note when the typo changes meaning.
- Validate with `check_html()` (tag balance, image count) before presenting. A real browser check is
  not available in the sandbox, so tell the user it was not opened in a browser.
