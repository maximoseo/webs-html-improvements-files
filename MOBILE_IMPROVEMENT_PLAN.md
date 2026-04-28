# תוכנית שיפורי מובייל — HTML Redesign Dashboard
## v1.0 | 2026-04-26

---

## מצב נוכחי
- index.html ~21,844 שורות, CSS inline
- קיימות media queries ל־768px, 640px, 380px
- קיים hamburger menu + mobile drawer (מצד ימין)
- אין bottom navigation bar
- אין FAB (Floating Action Button)
- touch targets לא תמיד עומדים ב־WCAG 2.5.8 (44×44px)

---

## 🎯 מטרות
1. נוחות תפעול באגודל (thumb-friendly)
2. מינימום גלילה אנכית מיותרת
3. מבנה ויזואלי ברור ומקצועי
4. תגובתיות מיידית (feedback חזותי)
5. שמירה על הערכות הנוכחיות (dark theme, צבעים)

---

## שלב 1: Bottom Navigation Bar (בר ניווט תחתון)

### בעיה
ה־hamburger drawer מצד ימין דורש פתיחה → בחירה → סגירה. זה מסורבל לשימוש יומיומי.

### פתרון
הוספת `bottom-nav` קבוע עם 5 לשוניות עיקריות:
```
[Projects] [Fixer] [+] [Radar] [More]
```
- גובה: 64px + env(safe-area-inset-bottom)
- רקע: rgba(11,12,16,0.92) + backdrop-filter: blur(20px)
- אייקון + תווית מתחת
- מצב פעיל: צבע accent (#7170ff)
- מופיע רק מתחת ל־768px

### תיאורי הפעולה
- **Projects** — עמוד פרויקטים
- **Fixer** — כלי תיקון N8N
- **+ (FAB)** — פתיחת תפריט פעולות מהירות (sync, add, search)
- **Radar** — Skills Radar
- **More** — drawer עם שאר האפשרויות (KWR, Tasks, Analytics, Settings, Logout)

### CSS
```css
.bottom-nav {
  display: none;
  position: fixed;
  bottom: 0; left: 0; right: 0;
  height: 64px;
  padding-bottom: env(safe-area-inset-bottom);
  background: rgba(11,12,16,0.92);
  backdrop-filter: blur(20px) saturate(150%);
  border-top: 1px solid rgba(255,255,255,0.07);
  z-index: 900;
}
.bottom-nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  min-height: 48px;
  color: var(--muted);
  background: transparent;
  border: none;
  font-size: 10px;
  font-weight: 500;
  cursor: pointer;
}
.bottom-nav-item.active { color: #7170ff; }
.bottom-nav-item svg { width: 22px; height: 22px; }

@media(max-width:768px){
  .bottom-nav { display: flex; }
  .footer { padding-bottom: calc(80px + env(safe-area-inset-bottom)); }
  body { padding-bottom: calc(64px + env(safe-area-inset-bottom)); }
}
```

---

## שלב 2: FAB — Floating Action Button

### בעיה
פעולות נפוצות (Sync, Global Search) נמצאות ב header וקשות להגעה באגודל.

### פתרון
FAB מרכזי בתחתית המסך (מעל ה־bottom nav):
- גודל: 56×56px
- צבע: gradient accent (#7170ff → #5b5aee)
- סמל: + (או ⚡)
- לחיצה פותחת תפריט פעולות מהירות:
  - Sync
  - Global Search
  - Expand/Collapse All
  - Add New Project
- ripple effect בלחיצה
- shadow: 0 4px 20px rgba(113,112,255,0.35)

### CSS
```css
.fab-wrap {
  display: none;
  position: fixed;
  bottom: calc(80px + env(safe-area-inset-bottom));
  left: 50%;
  transform: translateX(-50%);
  z-index: 910;
}
.fab-btn {
  width: 56px; height: 56px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #7170ff, #5b5aee);
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 20px rgba(113,112,255,0.35);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.fab-btn:active { transform: translateX(-50%) scale(0.92); }
@media(max-width:768px){ .fab-wrap { display: block; } }
```

---

## שלב 3: Header מובייל מינימליסטי

### בעיה
ה־header מכיל יותר מדי איברים במובייל: search, sync, expand-all, overflow, hamburger, theme, logout.

### פתרון
- **למסכים עד 768px**: הצג רק לוגו + search icon + hamburger
- **הזזה ל drawer**:
  - Sync button
  - Expand/Collapse All
  - Theme toggle
  - Logout
  - Keyboard shortcuts
- **הסרת status-stack** מה־header במובייל (או קביעתו כ־chip קטן)
- **Search**: הפוך לאייקון שפותח modal חיפוש fullscreen

### CSS
```css
@media(max-width:768px){
  .header-actions .status-stack,
  .header-actions .hdr-expand-all-btn,
  .header-actions .hdr-sync-btn,
  .header-actions #logout-btn,
  .header-actions .theme-toggle-btn { display: none; }
  .header h1 span { display: none; } /* הצג רק "HTML" */
  .header-inner { gap: 8px; }
}
```

---

## שלב 4: Project Cards — מבנה מחודש למובייל

### בעיה
Cards רחבים מדי, פעולות קטנות, מידע מרובה דורש הרחבה.

### פתרון
- **רוחב מלא** (1 column)
- **Header card**: דומיין + סטטוס + תפריט ⋮ (overflow)
- **Stats bar**: 3 מספרים בשורה (files, size, date) בגודל קטן
- **Action bar**: כפתורים ברורים — Preview | Prompt Studio | Compare
  - גובה כפתור: 40px minimum
  - ריווח: 8px
- **Expandable section**: פרטים נוספים (file list, agents) מאחורי "Show more"
- **Swipe gesture**: swipe ימינה על card = פתיחת Quick Actions (כמו Gmail)

### CSS
```css
@media(max-width:640px){
  .project-card { 
    border-radius: 16px; 
    margin-bottom: 12px;
  }
  .card-header { padding: 14px 16px; }
  .card-actions { 
    display: grid; 
    grid-template-columns: repeat(3, 1fr); 
    gap: 8px; 
    padding: 0 16px 14px;
  }
  .card-actions .action-btn {
    justify-content: center;
    min-height: 40px;
    font-size: 13px;
  }
}
```

---

## שלב 5: Touch Targets & Accessibility

### בעיה
כפתורים קטנים מדי, חוסר feedback בלחיצה.

### פתרון
1. **כל כפתור/קישור**: min 44×44px (WCAG 2.5.8)
2. **Active state**: transform: scale(0.96) + opacity transition
3. **Tap highlight**: הסרת ברירת מחדל של iOS (-webkit-tap-highlight-color: transparent)
4. **Focus visible**: outline accent בולט
5. **Ripple effect** על כפתורים ראשיים

### CSS
```css
* { -webkit-tap-highlight-color: transparent; }
button, .action-btn, a, [role="button"] {
  min-height: 44px; min-width: 44px;
  touch-action: manipulation;
}
button:active, .action-btn:active {
  transform: scale(0.96);
  transition: transform 0.08s;
}
```

---

## שלב 6: iOS & Safari Fixes

### בעיות ידועות
1. **Input zoom**: iOS מזום כשפוקוס על input עם font-size < 16px
2. **Safe area**: notch, home indicator
3. **Overscroll**: bounce effect מפריע
4. **vh units**: 100vh כולל את ה־toolbar של Safari

### פתרונות
```css
/* iOS zoom prevention */
input, select, textarea { font-size: 16px !important; }

/* Safe area */
body {
  padding-top: env(safe-area-inset-top);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}

/* Dynamic viewport height */
.modal, .fullscreen {
  height: 100svh; /* small viewport height */
  max-height: 100dvh; /* dynamic viewport height */
}

/* Overscroll behavior */
body, .modal, .drawer {
  overscroll-behavior-y: contain;
}

/* Safari momentum scrolling */
.scrollable {
  -webkit-overflow-scrolling: touch;
}
```

---

## שלב 7: Pull-to-Refresh

### פתרון
הוספת pull-to-refresh לעמוד Projects:
- גרירה למטה → ריענון נתונים
- אנימציה: חץ מסתובב + "Pull to sync"
- מניעת אינטראקציה כפולה עם fullSync()

### JS
```javascript
let ptrStartY = 0, ptrPulling = false;
const ptrThreshold = 80;

function initPullToRefresh(){
  const el = document.getElementById('page-projects');
  if(!el || window.innerWidth > 768) return;
  
  el.addEventListener('touchstart', e => {
    if(el.scrollTop === 0) { ptrStartY = e.touches[0].clientY; ptrPulling = true; }
  }, {passive: true});
  
  el.addEventListener('touchmove', e => {
    if(!ptrPulling) return;
    const diff = e.touches[0].clientY - ptrStartY;
    if(diff > 0 && diff < ptrThreshold * 2) {
      showPullIndicator(diff);
    }
  }, {passive: true});
  
  el.addEventListener('touchend', () => {
    if(!ptrPulling) return;
    const diff = /* calculate */;
    if(diff > ptrThreshold) fullSync();
    hidePullIndicator();
    ptrPulling = false;
  });
}
```

---

## שלב 8: Typography & Spacing Scale

### בעיה
גדלי גופן לא עקביים, spacing לא מתאים למובייל.

### פתרון — Scale חדש למובייל:
```
Heading page:   24px / 600 / -0.5px
Heading card:   18px / 600 / -0.3px
Body:           15px / 400 / 0
Caption:        13px / 400 / 0.2px
Label:          11px / 600 / 0.5px uppercase
Button:         14px / 600 / 0
Stat number:    28px / 700 / -0.5px
Stat label:     12px / 500 / 0.3px uppercase
```

### Spacing:
```
Page padding:     16px horizontal
Card gap:         12px
Section gap:      24px
Inner padding:    16px
Action gap:       8px
```

---

## שלב 9: Skeleton Loading States

### בעיה
Cards מוצגים ריקים או עם "-" בזמן טעינה.

### פתרון
הוספת skeleton screens:
```css
.skeleton {
  background: linear-gradient(90deg, #1a1c24 25%, #252836 50%, #1a1c24 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
  border-radius: 6px;
}
@keyframes skeleton-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

---

## שלב 10: Login Page Polish

### שיפורים:
1. **Viewport**: viewport-fit=cover (כבר קיים ✓)
2. **Safe area padding**: env(safe-area-inset) על הכרטיסיה
3. **Input height**: 52px למובייל (נגישות + iOS)
4. **Button height**: 52px
5. **Logo**: גודל מותאם, לא מופרז
6. **Background**: gradient עדין (כבר קיים ✓)
7. **Animation**: fade-in + slight translateY

---

## סדר ביצוע (Priority)

| # | שלב | זמן משוער | חשיבות |
|---|-----|-----------|--------|
| 1 | Bottom Nav + FAB | 2h | 🔴 גבוהה |
| 2 | Header מינימליסטי | 1h | 🔴 גבוהה |
| 3 | Touch targets + iOS fixes | 1h | 🔴 גבוהה |
| 4 | Project cards מובייל | 2h | 🟡 בינונית |
| 5 | Pull-to-refresh | 1h | 🟡 בינונית |
| 6 | Typography + spacing | 1h | 🟡 בינונית |
| 7 | Skeleton loading | 1h | 🟢 נמוכה |
| 8 | Login page polish | 30m | 🟢 נמוכה |

**סה"כ משוער: ~9.5 שעות עבודה**

---

## QA Checklist (לפני deploy)

- [ ] בדיקה על iPhone 14 Pro (Safari)
- [ ] בדיקה על iPhone SE (Safari)
- [ ] בדיקה על Android Chrome
- [ ] בדיקה על iPad (portrait + landscape)
- [ ] וידוא touch targets ≥ 44px
- [ ] וידוא input zoom לא קורה ב־iOS
- [ ] וידוא safe area מתנהג נכון
- [ ] וידוא bottom nav לא מסתיר תוכן
- [ ] Lighthouse mobile score ≥ 90

---

## קבצים שיושפעו
1. `index.html` — CSS inline + HTML structure + JS
2. `login-page.html` — CSS inline (minor polish)
3. `server.py` — ללא שינוי (רק frontend)
