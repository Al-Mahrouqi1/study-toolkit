# Raw HTML markup (for tools that cannot run Python)

Use only when you cannot run the build script. Copy these blocks exactly; the toolkit's CSS and JS give
them their look and behaviour. Math markup: `<span class="mx" dir="ltr">` with `<sub>`, `<sup>` and
`<span class="fr"><span class="nu">a</span><span class="de">b</span></span>` for fractions.

## Page skeleton

```html
<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chapter N: Title · الفصل</title>
<meta name="chapter" content="Chapter N: Title">
<meta name="tk-quiz-lang" content="en">
<script type="application/json" id="tk-gloss">{"entity": "كيان"}</script>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;700&family=Manrope:wght@400;500;700;800&family=Instrument+Serif&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Al-Mahrouqi1/study-toolkit@main/style.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Al-Mahrouqi1/study-toolkit@main/toolkit.css">
</head>
<body>
<main>
<h1>Chapter N: Title<span class="ar" dir="rtl">عنوان الفصل</span></h1>
<div class="lede"><p class="e" dir="ltr">One line.</p><p class="a" dir="rtl">سطر.</p></div>
<!-- big picture, sections, quiz, cheat sheet go here -->
</main>
<footer class="tk-sig tk-x">Eyad Al-Mahrouqi · @q7r_9</footer>
<script src="https://cdn.jsdelivr.net/gh/Al-Mahrouqi1/study-toolkit@main/toolkit.js"></script>
</body>
</html>
```

## Section — `section(1, "Title", "العنوان", "Slides 3–6", "الشرائح 3–6", [blocks])`

```html
<section id="s1"><h2><span class="n">1</span><span class="t"><span class="te" dir="ltr">Title</span><span class="ta" dir="rtl">العنوان</span></span></h2><p class="slides"><span dir="ltr">Slides 3–6</span> · <span dir="rtl">الشرائح 3–6</span></p><!-- blocks --></section>
```

## Big picture — `bigpicture(...)`

```html
<section id="big" class="bigp"><div class="idea"><span class="lbl">The big idea · الفكرة الكبيرة</span><p class="e" dir="ltr">Main idea.</p><p class="a" dir="rtl">الفكرة.</p></div><div class="cmap" dir="ltr"><ul><li><div class="nd root">Topic</div><ul><li><span class="rel">has</span><div class="nd"><a href="#c-a">A</a></div><ul><li><div class="nd sm">x</div></li></ul></li></ul></li></ul></div></section>
```

## Lead — `lead(...)`

```html
<div class="lead"><div class="chain" dir="ltr"><span>Builds on <b>X</b></span><span class="ar">→</span><span>Leads to <b>Y</b></span></div><p dir="ltr">Why it matters.</p><p class="a" dir="rtl">لماذا.</p></div>
```

## Concept card — `concept(...)`

```html
<div class="concept" id="c-a"><div class="chd"><h4 dir="ltr">Concept A</h4><span class="src">Slide 4</span></div><div class="car" dir="rtl">سطر عربي.</div><div class="r def"><span class="cl">Definition</span><div class="cv"><q>Exact wording.</q></div></div><div class="r"><span class="cl">In plain words</span><div class="cv">Simple.</div></div><div class="r"><span class="cl">How it works</span><div class="cv"><ul><li>Rule 1.</li></ul></div></div><div class="r"><span class="cl">Example</span><div class="cv">Ex.</div></div><div class="r mis"><span class="cl">Common mistake</span><div class="cv">Confusion.</div></div><div class="r con"><span class="cl">Connects to</span><div class="cv"><ul><li><a href="#c-b">B</a> — relation</li></ul></div></div></div>
```

## Compare — `compare(...)`

```html
<div class="cmp"><div class="cmh">A vs B</div><table dir="ltr"><thead><tr><th></th><th>A</th><th>B</th></tr></thead><tbody><tr><td>Is</td><td>x</td><td>y</td></tr></tbody></table></div>
```

## Key points — `keypoints(...)`

```html
<div class="kp"><div class="kph">Key points · أهم النقاط</div><ol dir="ltr"><li class="core">Must know.</li><li class="">Point.</li></ol></div>
```

## Law — `law(...)`

```html
<div class="law" data-syms="{&quot;Y&quot;: [&quot;meaning&quot;, &quot;المعنى&quot;, &quot;unit&quot;]}"><div class="lh"><span dir="ltr">Law · Name</span><span dir="rtl">القانون · الاسم</span></div><div class="lf"><span class="mx" dir="ltr">Y = <span class="fr"><span class="nu">a</span><span class="de">b</span></span></span></div><table class="lv" dir="ltr"><thead><tr><th>Symbol</th><th>Meaning · المعنى</th><th>Unit</th></tr></thead><tbody><tr><td><span class="mx" dir="ltr">Y</span></td><td><span dir="ltr">meaning</span><span class="a" dir="rtl">المعنى</span></td><td dir="ltr">unit</td></tr></tbody></table><div class="bi lw"><p class="e" dir="ltr"><b>When to use:</b> When.</p><p class="a" dir="rtl"><b>متى نستخدمه:</b> متى.</p></div><div class="bi lw"><p class="e" dir="ltr"><b>Watch out:</b> Trap.</p><p class="a" dir="rtl"><b>انتبه:</b> انتبه.</p></div></div>
```

## Worked solution — `steps(...)`

```html
<ol class="steps"><li><div class="sx"><span class="mx" dir="ltr">Y = <span class="fr"><span class="nu">a</span><span class="de">b</span></span></span></div><div class="sn" dir="ltr">Law</div></li><li><div class="sx"><span class="mx" dir="ltr">= <span class="fr"><span class="nu">6</span><span class="de">2</span></span></span></div><div class="sn" dir="ltr">Substitute</div></li><li><div class="sx"><span class="mx" dir="ltr">= 3</span></div><div class="sn" dir="ltr">Divide</div></li></ol><div class="ans"><span class="lb">Answer · الإجابة</span><span class="mx" dir="ltr">Y = 3</span></div>
```

## Warning / gap — `warn(...)`

```html
<div class="warn"><p class="e" dir="ltr">Not covered in the provided chapters.</p><p class="a" dir="rtl">غير موجود في الفصول المقدّمة.</p></div>
```

## Quiz — `quiz(...) with mcq / tf / essay`

```html
<section id="quiz" class="quiz" data-mode="instant"><h2><span class="t"><span class="te" dir="ltr">Test</span><span class="ta" dir="rtl">اختبار</span></span></h2><div class="q" data-type="mcq" data-answer="1" data-src="Slide 4" data-ref="s1"><div class="qt"><span class="qn">1</span><div class="bi"><span class="kind">Multiple choice</span><p class="e" dir="ltr">Q?</p><p class="a" dir="rtl">س؟</p></div></div><ol class="opts"><li><span class="e" dir="ltr">A</span></li><li><span class="e" dir="ltr">B</span></li></ol><div class="why"><b>Explanation</b><div class="bi"><p class="e" dir="ltr">Why.</p></div></div></div><div class="q" data-type="tf" data-answer="true"><div class="qt"><span class="qn">2</span><div class="bi"><span class="kind">True or False</span><p class="e" dir="ltr">Statement.</p><p class="a" dir="rtl"></p></div></div></div><div class="q" data-type="essay"><div class="qt"><span class="qn">3</span><div class="bi"><span class="kind">Written answer</span><p class="e" dir="ltr">Explain.</p><p class="a" dir="rtl"></p></div></div><div class="model"><b>Model answer</b><div class="bi"><p class="e" dir="ltr">Model answer.</p></div></div></div></section>
```

## Cheat sheet — `cheatsheet(...)`

```html
<section id="cheat" class="cheat"><h2><span class="t"><span class="te" dir="ltr">Quick review sheet</span><span class="ta" dir="rtl">ورقة المراجعة السريعة</span></span></h2><div class="cg" dir="ltr"><div class="cb"><h5>Definitions</h5><dl><dt>A</dt><dd>meaning</dd></dl></div><div class="cb"><h5>Formulas</h5><ul class="fm"><li><span class="fl">Name</span><span class="mx" dir="ltr">Y = <span class="fr"><span class="nu">a</span><span class="de">b</span></span></span></li></ul></div><div class="cb"><h5>Don't confuse</h5><ul><li><b>A</b> vs <b>B</b>: diff</li></ul></div><div class="cb trap"><h5>Exam traps</h5><ul><li>Trap.</li></ul></div></div></section>
```
