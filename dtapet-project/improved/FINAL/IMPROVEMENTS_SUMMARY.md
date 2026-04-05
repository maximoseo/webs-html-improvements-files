# שיפורים - DTAPET Project V2.0
## Tim Claw Max | 2026-04-05

---

## 📁 קבצים משופרים

### 1. N8N Prompt V2 (n8n_prompt_v2.txt / N8N_Prompt_v2.md)
**46KB** - Prompts משופרים ליצירת כתבות

### 2. HTML Template V2 (HTML_Template_V2_Sample.html)
**11KB** - תבנית HTML לדוגמה עם כל השיפורים

### 3. Workflow JSON - בהכנה (n8n_workflow_v2.json)
**קובץ JSON משופר ל-N8N**

---

## ✅ שיפורים מרכזיים

### Anti-AI Detection (Section 0 - NEW)
- VOICE AUTHENTICITY - כתיבה כמו יועץ פנים אמיתי
- HUMAN WRITING PATTERNS - וריאציה באורך משפטים
- FORBIDDEN AI MARKERS - 12 ביטויים אסורים
- NATURAL WRITING TRIGGERS - תבניות כתיבה הומניות

### Local SEO Israel (Section 3 - NEW)
- מיקוד בשוק הישראלי
- מחירים ב-₪ (NIS)
- כתובת פתח תקווה
- סכמות: Article + LocalBusiness + FAQPage + Product + Review

### Performance Optimization (Section 8 - NEW)
- loading="lazy" decoding="async" לכל התמונות
- Alt text בעברית
- קונטרסט WCAG 2.1 AA
- ARIA labels

### Accordion Arrow Fix (Section 9 - CRITICAL)
```
 Arrow: position:absolute; LEFT:18px; top:50%;
 Summary: padding-right:50px; display:block (NOT flex)
 !important flags on ALL RTL properties
```

### Hover Effects (Section 10)
- TOC per-item hover
- FAQ per-item hover  
- CTA button hover
- Product card hover
- Floating buttons hover
- Social buttons: neutral → Facebook/Instagram colors

### Output Checklist (Section 13)
50+ פריטים לבדיקה לפני יצירת הכתבה

---

## 🎨 מבנה הכתבה (בסדר מדויק)

1. **A0. Trust Banner** - יתרונות המותג
2. **A. Hero Image + Intro** - פסקה פותחת עם HOOK
3. **B. Summary Box** - "במאמר זה" עם 4-6 נקודות
4. **C. Table of Contents** - סגור כברירת מחדל
5. **D. Top Product Grid** - 3 מוצרים מ-[PRODUCTS_JSON]
6. **E. Body Content** - מינימום 5 H2 עם תמונות
7. **E1. Content Elements** - טבלאות, כרטיסיות, CTA
8. **E2. Bottom Product Grid** - 3 מוצרים נוספים
9. **E3. Reviews** - רק אם יש ביקורות
10. **F. FAQ Section** - 5-8 שאלות
11. **G. Closing** - 2-3 משפטי סיום
12. **H. CTA Button** - כפתור יצירת קשר
13. **I. Author Bio** - כרטיס פרימיום
14. **J. Floating Buttons** - שמאל בלבד
15. **K. JSON-LD Schemas** - Article + LocalBusiness + FAQ

---

## 🔧 משתנים להחלפה ב-N8N

```
[ARTICLE_TOPIC] - נושא הכתבה
[HERO_IMAGE] - תמונת Hero
[SECTION_IMAGE_1-4] - תמונות מקטעים
[PRODUCTS_JSON] - מוצרים מ-Supabase
[REVIEWS_JSON] - ביקורות מאומתות
[SOCIAL_JSON] - פרופילים חברתיים
```

---

## 📋 כללי Output

- RAW HTML בלבד
- Minified (שורה אחת או מעט)
- Inline CSS בלבד (ללא `<style>`)
- ללא classes
- RTL: `<article lang="he" dir="rtl">`
- צבעים: HEX בלבד (#rrggbb)
- גופן: 'Assistant', Arial, sans-serif
- ללא emoji
- ללא קישורים למתחרים

---

## 🚫 אסורים

- `<style>` blocks
- CSS classes
- `<h1>` tags
- display:flex on `<summary>`
- Em-dashes (—) בעברית
- "חשוב לציין", "ללא ספק", "ראשית...שנית"
- תמונות מקור חיצוני (רק Supabase)
- category pages כמוצרים
- object-fit:cover (חייב contain)
