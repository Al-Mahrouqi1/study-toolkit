# Summary method

A summary is not the slides in order. Rebuild the chapter around its concepts and how they connect.

1. **List the concepts** from `slides.txt` (terms, laws, processes, components). Merge slides that repeat
   or continue the same idea. For each concept note what it depends on and what it leads to.
2. **Order by dependency** (what must be understood first); keep the chapter's order when it already works.
   Group the concepts into 3–7 sections.
3. **Open with `bigpicture(idea_en, idea_ar, center, branches)`**: the chapter's main idea in 1–2 sentences
   and a concept map. `branches = [((label, concept_id), [children], "verb on the link"), ...]`.
4. **Each section** (`section(n, title_en, title_ar, "Slides 3–6", "الشرائح 3–6", blocks)`):
   - `lead(why_en, builds_on="…", leads_to="…", why_ar="…")` — why it matters and how it links.
   - one `concept(cid, name, definition=, plain=, how=[…], example=, mistake=, connects=[(id, relation, label)],
     ar=, src="Slide 4", extra=fig(...) or law(...))` per concept. Skip empty rows, never pad.
   - `compare(title, ["", "A", "B"], rows)` for any concepts students mix up.
   - `keypoints([("must-know point", True), "point", …])` — max 5, most important first.
   - `warn(en, ar)` for gaps; `dtable(head, rows)` for tables copied from the slides.
5. **Card rows**: Definition (verbatim) → In plain words (one sentence) → How it works (2–4 bullets) →
   Example (slides, or "my example") → Common mistake → Connects to.
6. **Bullets**: one idea, ≤ 15 words, start with the key term, parallel grammar, ≤ 5 per list, no filler.
7. **End with `cheatsheet(definitions, formulas, differences, traps)`**, then `practice(...)` (questions
   without answers, including the slides' own exercises) and `status([...])` (all "Not yet tested").
8. **Figures**: every exam-relevant slide picture is embedded with `fig(name, slide, cap_en, cap_ar, en, ar)`
   and explained (only what is visible). Your own simple SVG diagrams are welcome where a picture makes
   an idea easier; label them "My diagram (from the slide content)".
9. **Emphasis** on the slides (red, bold, repeated) becomes must-know `keypoints` and goes in the cheatsheet.
