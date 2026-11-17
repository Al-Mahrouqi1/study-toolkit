# Formulas and math

## Writing math: `m(expr)`
`x_i`, `x_{avg}` subscript · `x^2`, `10^{-9}` power · `[[a || b]]` fraction (nestable) · `*` → ×.
Example: `m("CPU time = [[IC × CPI || f]]")`. Put numbers inside sentences through `m()` too
(f-strings: `f"runs {m('2 × 10^9')} instructions"`).

## A law: `law(name_en, name_ar, expr, variables, when_en, when_ar, note_en, note_ar)`
Coloured boxed card: formula, a table of symbols `[(symbol, meaning_en, meaning_ar, unit), …]`,
when to use it, and the common mistake. Every symbol listed here becomes hoverable/tappable wherever it
appears in `m()` math. Symbols used outside a law box: `add_toolkit(..., symbols={"V": ("Voltage", "الجهد", "V")})`.
Use the same spelling of a symbol everywhere (`R_th` in the law and in the steps).

## Worked example: `solved(title_en, title_ar, problem_en, problem_ar, given=[…], find="…", items=[…], answer=(…), check=(…), src=…)`
`items` = steps `[(math, why_en, why_ar), …]`, **one operation per line**: law → substitute with units →
each arithmetic step → result. `answer=("CPU time = 1 s", "words")` is boxed; `check=` re-derives it.
`steps(items, answer, check)` alone is the model answer for test questions.

## Accuracy (strict)
- Compute every number in Python; paste exact results. Never mental arithmetic.
- Keep units in every step; convert units in their own step before substituting.
- Round only the final answer (3 significant figures unless the course says otherwise), and say so.
- Use the course's exact formula and symbols; if the slides show two forms, show both and how they connect.
- Re-derive each answer a second way (other formula, units check, plugging back). If they disagree, fix first.
