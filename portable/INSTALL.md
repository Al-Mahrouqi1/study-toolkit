# تثبيت مهارة «التلخيص المفصل» في أدوات الذكاء الاصطناعي

المهارة مبنية على المعيار المفتوح **Agent Skills** (ملف `SKILL.md`)، وتعمل في كل أداة تدعمه وتسمح بتشغيل Python.
المجلد المطلوب هو `detailed-study-summary` كاملًا (لا تنقل ملف `SKILL.md` وحده).

## التنزيل

```bash
git clone https://github.com/Al-Mahrouqi1/study-toolkit
cd study-toolkit/portable
```
أو نزّل `detailed-study-summary.zip` من نفس المجلد في GitHub.

## مكان المهارة في كل أداة

| الأداة | لكل المشاريع (عام) | لمشروع واحد |
|---|---|---|
| Claude (الموقع / التطبيق) | ارفع `detailed-study-summary.zip` من إعدادات المهارات (Skills) | — |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| OpenAI Codex | `~/.agents/skills/` (والإصدارات الأقدم: `~/.codex/skills/`) | `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` أو `.agents/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` أو `.agents/skills/` |
| GitHub Copilot (VS Code / CLI) | `~/.copilot/skills/` | `.github/skills/` |
| Windsurf | — | `.windsurf/skills/` |
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` |
| أدوات أخرى تدعم المعيار | `~/.agents/skills/` | `.agents/skills/` |

مثال (Codex أو أي أداة تقرأ المجلد العام):
```bash
mkdir -p ~/.agents/skills && cp -r detailed-study-summary ~/.agents/skills/
```

## ChatGPT وأي محادثة فيها تشغيل كود بدون دعم المهارات
ارفع `detailed-study-summary.zip` مع ملف الشرائح، واكتب:
> فك ضغط الملف واقرأ `detailed-study-summary/SKILL.md` ونفّذ تعليماتها حرفيًا على الشرائح المرفقة.

## نموذج بدون تشغيل كود
أرسل له محتوى `SKILL.md` و`references/markup.md` مع نص الشرائح. سيكتب صفحة HTML تحمّل أدوات القالب من الإنترنت.
النتيجة أقل دقة من الأدوات التي تشغّل Python (لا قص صور ولا حساب بالكود).

## المتطلبات على جهازك (للأدوات المحلية فقط)
- **ضروري:** Python 3.9 أو أحدث.
- **اختياري للأفضل:** LibreOffice (لعرض الشرائح كصور) و poppler (`pdftoppm`).
- الحزم (python-pptx و Pillow و PyMuPDF) تثبّتها المهارة بنفسها إن أمكن، ولها بدائل إن لم يمكن.

## الاستخدام
أرفق الشرائح أو ملف PDF واكتب مثلًا: «لخّص هذا الفصل» أو «اعمل اختبار للفصل».
أول ما تفعله المهارة هو تشغيل `scripts/setup_env.py` لتعرف ما المتاح في الأداة وأين تحفظ الملف.
