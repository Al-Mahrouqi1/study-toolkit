# Tests and practice questions

Build each part with `quiz(title_en, title_ar, [questions], sid="partA", mode="instant"|"exam")` and finish
the page with `add_toolkit(..., quiz_lang="en")` (English labels, Arabic hidden behind "Show Arabic").
Fill the Arabic arguments anyway.

Question helpers (all take `src="Section 3 · Slides 14–19", ref="s3"` so the student can jump to the source):
- `mcq(q_en, q_ar, [(opt_en, opt_ar), …], answer_index, why_en, why_ar)`
- `tf(q_en, q_ar, True/False, why_en, why_ar)`
- `essay(q_en, q_ar, model_en, model_ar)` — written answers; model answer may be `steps(...)`.

## Size and parts
Many questions of all types: A Multiple choice · B True/False · C Fill in the blank (`essay`, short answer)
· D Calculations (if the chapter has formulas) · E Understanding. Roughly 50–70 questions for a normal
chapter, covering every section, including every exercise and question-bank item in the slides.

## Understanding, not only memory
At most about a third are recall. The rest mix: why/explain · apply to a short new scenario
("my scenario") · compare two close concepts · find the error · predict what changes if a condition changes.
MCQ distractors are plausible misconceptions. New scenarios may only use concepts from the material.

## Calculation problems
For each law: direct · inverse (solve for another variable) · unit traps (GHz→Hz, ms→s, %) · multi-step
(chain two laws) · compare two cases · find the error in a wrong solution. Clean, realistic numbers.
Distractors come from real mistakes (forgot to convert, inverted a ratio, wrong variable, early rounding).
Model answers use `steps()` (see math.md). Compute every number in Python first.
