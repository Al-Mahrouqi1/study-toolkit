#!/usr/bin/env python3
"""Claude edition skeleton. Write work/build.py from this (one file), fill it from the slides, run it.

    python work/build.py && python work/tk/qa.py "$OUT" --slides work/<stem>/slides.txt
"""
import os, sys
sys.path.insert(0, "work/tk")            # bilingual_lib, study_tools, crop_tools (bootstrap step)
from bilingual_lib import *
from study_tools import *

OUT = "/mnt/user-data/outputs/chapterN_summary.html"
set_image_dir("work/img")                # crops: work/img/c_s<slide>.png · or set_image_dir("work/<stem>/blobs") and fig("s5_1", ...)

big = bigpicture("The chapter's main idea in one or two sentences.", "الفكرة الرئيسية في سطر.",
                 "Chapter topic", [(("Concept A", "a"), ["detail"], "has"), ("Concept B", [], "uses")],
                 src="Slides 1–20")

s1 = section(1, "First group of concepts", "المجموعة الأولى", "Slides 3–6", "الشرائح 3–6", [
    lead("Why this matters in one sentence.", builds_on="previous idea", leads_to="next idea",
         why_ar="لماذا يهم، في سطر."),
    concept("a", "Concept A", definition="Exact course wording.", plain="One simple sentence.",
            how=["Part or rule 1.", "Part or rule 2."], example="Example from the slides.",
            mistake="The usual confusion.", connects=[],
            ar="المفهوم أ: معناه في سطر.", src="Slide 4"),
    # extra=fig("c_s5", 5, "Caption", "التسمية", "What it shows.", "ماذا يظهر.")
    # extra=law("Name", "الاسم", "Y = [[a || b]]", [("Y", "meaning", "المعنى", "unit")])
    keypoints([("Most important point.", True), "Second point."]),
])

body = big + s1 + cheatsheet(definitions=[("Concept A", "one-line meaning")], traps=["Common exam trap."]) \
     + practice("Try these before checking your notes.", "حاول قبل الرجوع للملخص.",
                [("Why does A need B?", "لماذا يحتاج أ إلى ب؟")]) \
     + status(["1. First group of concepts"])

os.makedirs(os.path.dirname(OUT), exist_ok=True)
write_page(OUT, "Chapter N: Title", "الفصل N: العنوان", "One-line description of the chapter.",
           "وصف الفصل في سطر.", [("big", "Big picture"), ("s1", "1. First group"), ("cheat", "Review sheet")], body)
add_toolkit(OUT, chapter="Chapter N: Title", gloss={"concept a": "المفهوم أ"})
print(OUT, check_html(OUT))
