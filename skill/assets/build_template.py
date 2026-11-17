#!/usr/bin/env python3
"""Skeleton for one chapter. Copy it, fill the blocks from the slides, run it.

    python build_template.py            # writes ./out/summary.html

Image names refer to ./img/<name>.png (made with scripts/crop_tools.py).
"""
import os, sys
# Works in place, or after copying if SKILL_DIR points at the skill folder.
SKILL = os.environ.get("SKILL_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
from bilingual_lib import *

set_image_dir("img")

sec1 = section(1, "Topic title as in the slides", "عنوان الموضوع", "Slides 3–6", "الشرائح 3–6", [
    term("Exact definition wording from the slide.",
         "Easier explanation in English.",
         "شرح أبسط بالعربية."),
    bi("A plain explanatory paragraph in English.", f"فقرة شرح بالعربية مع مصطلح {L('Course Term')} بالإنجليزية."),
    # fig("c_s6", 6, "Caption as on slide", "التسمية بالعربية",
    #     "What the diagram shows, only what is visible or written.", "ما يظهر في المخطط بالعربية."),
    cards(card("Concept", "English explanation.", "الشرح بالعربية.",
               eg=("Slide example in English.", "مثال الشريحة بالعربية."))),
    warn("Note: something the slide leaves incomplete or unreadable. I do not guess it.",
         "ملاحظة: شيء تتركه الشريحة ناقصًا أو غير مقروء. لا أخمّنه."),
    review([("Definition X, rule Y.", "التعريف X والقاعدة Y.")]),
])

body = sec1 + practice(
    "No answers are given so you can try first.", "لا أضع الإجابات لتجرّب أولًا.",
    [("Question in English?", "السؤال بالعربية؟")]) + status(["1. Topic title as in the slides"])

n = write_page("out/summary.html", "Chapter N: Title", "ملخص الفصل: العنوان",
               "A summary built only from the provided slides, in English and Arabic.",
               "ملخص مبني فقط على الشرائح المقدّمة بالإنجليزية والعربية.",
               [("s1", "1. Topic"), ("practice", "Practice · التدريب")], body)
print(n // 1024, "KB", check_html("out/summary.html"))
