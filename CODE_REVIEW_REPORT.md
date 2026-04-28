# Code Review – Dashboard (Stability / Speed / UX)
תאריך: 2026-04-21 · קבצים: `index.html`, `dashboard-rebuilt.html`, `server.py`, `kwr_backend.py`

הפרויקט בנוי טוב בסך הכל, אבל יש כמה נקודות כאב שמרגישות בייצור. מסומן P0 = לתקן עכשיו, P1 = השבוע, P2 = שיפור.

---

## 🔴 P0 – קריטי (יציבות / אבטחה)

### 1. כתיבת JSON לא-אטומית → קבצים פגומים בקריסה
`kwr_backend.py:51-52, 69-70` כותב `job.json`/`meta.json` ישירות. אם השרת נופל באמצע כתיבה (Render OOM), הקובץ נשאר חלקי וכל הריצה אבודה.
**תיקון:** כתיבה ל־`*.tmp` ואז `os.replace()`:
```python
tmp = path + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(job_copy, f, ensure_ascii=False, indent=2, default=str)
os.replace(tmp, path)
```

### 2. Header לא חוקי מפיל העלאת Excel ל-Supabase
`kwr_backend.py:1881`: `'Cache-Control': '3600'` – חסר `max-age=`. Supabase מחזיר 400 לעיתים.
**תיקון:** `'Cache-Control': 'max-age=3600'`

### 3. גישות ל-`_state` מחוץ ל-`RLock` (race condition)
מהסריקה הקודמת: 64/109 גישות לא מוגנות. מתבטא כ-stale reads בעת ריצות מקבילות (KWR + status polling) – המשתמש רואה stage שלא מתעדכן או "stuck at 99%".
**תיקון:** wrapper:
```python
def _state_get(rid): 
    with _state_lock: return _state.get(rid)
def _state_update(rid, **kw):
    with _state_lock:
        if rid in _state: _state[rid].update(kw); _state[rid]['updated_at']=time.time()
```
ולעבור על כל `_state[...]=` להשתמש בו.

### 4. XSS פוטנציאלי ב-33 מקומות `innerHTML` עם interpolation
`index.html` משתמש ב־`elem.innerHTML = \`...${userInput}...\`` עם נתונים מהשרת/clipboard/comments. שם המשתמש בקומנטים, URLs מ-radar, prompts – כולם זורמים לתוך DOM ללא escaping.
**תיקון מהיר:** helper `esc(s)`:
```js
const esc = s => String(s??'').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
```
ולעטוף כל `${...}` שמגיע מ-user/network. עדיף לעבור ל-`textContent` היכן שאפשר.

---

## 🟠 P1 – חשוב (השבוע)

### 5. Poller בלי backoff על שגיאות
`dashboard-rebuilt.html:10114`: `setInterval(kwrPoll, 2500)` רץ גם כשה-API נופל → 24 בקשות/דקה לשרת מת. גם לא נעצר כש-tab לא פעיל.
**תיקון:**
- `setTimeout` רקורסיבי + הגדלת אינטרוול בכישלון (2.5s → 5 → 10 → 20).
- `document.addEventListener('visibilitychange', ...)` לעצירה כש-tab מוסתר.

### 6. Polling יורה שתי לולאות במקביל
שני קבצי dashboard (`index.html` + `dashboard-rebuilt.html`) שניהם מגדירים `_kwrPoller`, `radarPollTimer` באותו namespace. אם שניהם נטענים → poll כפול.
**תיקון:** לוודא שרק קובץ אחד נטען בהפעלה, או להוסיף `if (window._kwrPoller) return;`

### 7. localStorage גדל ללא הגבלה
`radar_seen_urls` נשמר עם `slice(-5000)` ✓ אבל `dashboard_cache`, `kwr_*` לא מוגבלים. בדפדפן עם מכסה 5MB → quota exceeded ושום `setItem` לא יעבוד.
**תיקון:** wrapper `safeSetItem` שתופס `QuotaExceededError` ומריץ cleanup של מפתחות ישנים.

### 8. `urlopen` חוסם thread של HTTP server
`kwr_backend.py` קורא ל-LLMs/scraping עם `urlopen(timeout=30)` בתוך handler של ה-API. ב-`ThreadingHTTPServer` כל בקשה תופסת thread – 10 בקשות במקביל = 10 threads תקועים בקריאת רשת.
**תיקון:** להעביר את כל הקריאות הארוכות ל-`worker_thread` שמופעל ע"י `/api/kwr/start`, ו-`/api/kwr/status` רק קורא state.

### 9. `print(...)` בכל מקום במקום logging
קשה לדבג ב-Render (אין רמות, אין timestamps). 
**תיקון:** `logger = logging.getLogger('kwr')` ולהחליף.

---

## 🟡 P2 – שיפורי UX/ביצועים

### 10. `index.html` 13K+ שורות בקובץ אחד
- זמן parse ראשוני איטי במובייל.
- **המלצה:** לפצל ל-`app.css`, `app.js`, ו-modules (kwr.js, radar.js, comments.js) עם `<script type="module">`. אפילו cache-busted concat יעזור.

### 11. אין debounce על חיפוש/פילטרים
חיפוש בטבלאות של 200+ rows מריץ re-render בכל keystroke.
**תיקון:** `debounce(fn, 200)` סטנדרטי.

### 12. אין skeleton/empty-state
מסכי loading מראים רק spinner. מומלץ skeleton rows לטבלאות KWR/radar.

### 13. אין retry אוטומטי ל-`/api/kwr/start`
כישלון רשת אקראי = המשתמש צריך ללחוץ שוב. fetch wrapper עם retry-3 על network error בלבד.

### 14. CSP חסר
`server.py` לא שולח `Content-Security-Policy`. הוספת `default-src 'self'; script-src 'self' 'unsafe-inline'` מצמצמת משמעותית את חשיפת ה-XSS.

### 15. ניווט מקלדת
טבלאות KWR/Radar לא ניתנות לניווט עם חצים/Tab. הוספת `tabindex` ו-`role="row"` ישפרו נגישות וזמן עבודה.

---

## סדר ביצוע מומלץ
1. **עכשיו (15 דק'):** #2 (Cache-Control), #1 (atomic write), #5 (poller backoff).
2. **היום (1-2 שעות):** #3 (state lock wrapper), #4 (XSS esc helper על השדות הרגישים).
3. **השבוע:** #6, #7, #8, #14.
4. **רפקטור:** #10 (פיצול index.html) – פרויקט בפני עצמו.

רוצה שאפתח PR עם תיקוני P0 (#1, #2, #5) עכשיו? זה ~30 שורות שינוי, נמוך-סיכון, גיבוי לפני.
