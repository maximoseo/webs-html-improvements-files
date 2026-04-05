# N8N - תיקון תצוגת מוצרים ב-WordPress

## הבעיה

המוצרים לא מוצגים נכון באתר WordPress כי:

1. **תמונות Supabase** - ה-N8N מנסה להעלות ל-Supabase ולהשתמש בקישורים משם, אבל זה לא תמיד עובד
2. **מבנה HTML** - הגריד (grid) לא מוגדר נכון לכל גודל מסך
3. **חסר קוד JavaScript** - אין קוד שמייצר את ה-HTML של כרטיסי המוצרים

---

## פתרון: קוד JavaScript לייצור כרטיסי מוצרים

### קוד ל-Node "Generate Product HTML" (חדש)

הוסף Node חדש מסוג "Code" אחרי "Extracts the Product Image Data":

```javascript
// N8N Code Node: Generate Product HTML Grid
// Input: items from product extraction
// Output: HTML string for product grid

function generateProductCard(product) {
  const name = product.title || product.name || '';
  const url = product.url || '#';
  const image = product.main_image || product.image || '';
  const alt = product.title || name;
  const price = product.price || 'לצפייה בקטלוג';

  // Skip if no image
  if (!image) return '';

  return `<a href="${url}" style="text-decoration:none;color:inherit;display:flex;flex-direction:column;background:#fff;border:1px solid #e5e5e5;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.08);overflow:hidden;text-align:center;min-height:380px;" onmouseover="this.style.boxShadow='0 4px 16px rgba(0,0,0,0.12)';this.style.transform='translateY(-2px)'" onmouseout="this.style.boxShadow='0 2px 8px rgba(0,0,0,0.08)';this.style.transform='none'"><div style="height:280px;background:#f9f7f4;display:flex;align-items:center;justify-content:center;overflow:hidden;"><img src="${image}" alt="${alt}" style="width:100%;height:100%;object-fit:contain;padding:1rem;" loading="lazy"></div><h3 style="font-size:0.95rem;padding:0.5rem 1rem 0.5rem;color:#2b2e34;font-family:'Assistant',Arial,sans-serif;margin:0;">${name}</h3><span style="font-size:0.9rem;color:#bc1f1f;font-weight:700;padding:0 1rem 1rem;display:block;margin-top:auto;">${price}</span></a>`;
}

function generateProductGrid(products, startIndex, count) {
  const gridProducts = products.slice(startIndex, startIndex + count);
  const cards = gridProducts.map(generateProductCard).filter(Boolean);
  
  if (cards.length === 0) return '';
  
  return `<div style="display:grid;grid-template-columns:repeat(${Math.min(cards.length, 3)},1fr);gap:1.5rem;margin:1.5rem 0;">${cards.join('')}</div>`;
}

// Get products from input
const allProducts = $input.all().map(item => item.json);
const products = allProducts.filter(p => p.main_image || p.image);

// Generate TOP grid (first 3 products)
const topGrid = generateProductGrid(products, 0, 3);

// Generate BOTTOM grid (next 3 products, if available)
const bottomGrid = generateProductGrid(products, 3, 3);

return [
  {
    json: {
      top_grid: topGrid,
      bottom_grid: bottomGrid,
      top_products: products.slice(0, 3),
      bottom_products: products.slice(3, 6),
      total_products: products.length
    }
  }
];
```

---

## קוד ל-JavaScript Node המתוקן - "Collect Images URLS" (קיים)

ודא שהקוד הזה מעביר את נתוני המוצרים נכון:

```javascript
// Current node: Collect Images URLS
// Make sure it also passes products data

const items = $items();
const urls = items.map(i => i.json["Image URL"]).filter(Boolean);

// ADD THIS: Get product data from previous nodes
const productItems = $items("Extracts the Product Image Data") || [];
const products = productItems.map(p => p.json).filter(prod => prod.main_image);

const images = {
  hero: urls[0] || null,
  section_1: urls[1] || null,
  section_2: urls[2] || null,
  section_3: urls[3] || null,
  section_4: urls[4] || null,
  // ADD products array
  products: products.slice(0, 6)  // Max 6 products for 2 grids
};

return [{ json: { images } }];
```

---

## עדכון Node "Preparing Image Data"

הוסף לוגיקה לטיפול במוצרים:

```javascript
// In "Preparing Image Data" node, add at the end:

// Handle products
const rawImages = $node["Collect images URLS"].json.images;
const products = rawImages.products || [];

// Generate product HTML
const topGrid = generateProductGrid(products, 0, 3);
const bottomGrid = generateProductGrid(products, 3, 3);

return [
  {
    json: {
      // ... existing fields ...
      top_product_grid: topGrid,
      bottom_product_grid: bottomGrid
    }
  }
];
```

---

## שינוי ב-N8N Prompt - חלק HTML Generation

### החלף את החלק של [PRODUCT_GRID_TOP] ו-[PRODUCT_GRID_BOTTOM]

במקום:
```
[PRODUCT_GRID_TOP]
[PRODUCT_GRID_BOTTOM]
```

השתמש ב-placeholder:
```
{{ $json.top_product_grid }}
{{ $json.bottom_product_grid }}
```

---

## מבנה נתונים צפוי מ-"Extracts the Product Image Data"

```json
[
  {
    "url": "https://www.dtapet.com/product/product-slug/",
    "title": "שם המוצר",
    "main_image": "https://www.dtapet.com/wp-content/uploads/2025/08/image.jpg",
    "price": "250 ₪"
  },
  {
    "url": "https://www.dtapet.com/product/product-slug-2/",
    "title": "שם מוצר שני",
    "main_image": "https://www.dtapet.com/wp-content/uploads/2024/01/image.jpg",
    "price": ""
  }
]
```

---

## רשימת בדיקה לפני הרצה

- [ ] Node "Extracts the Product Image Data" מחזיר נתוני מוצרים עם `main_image`
- [ ] Node "Collect Images URLS" מעביר את מערך המוצרים
- [ ] Node "Generate Product HTML" (חדש) מייצר HTML תקין
- [ ] ה-HTML משתמש ב-`object-fit:contain` לתמונות
- [ ] יש `min-height:380px` על כל כרטיס
- [ ] הגריד מוגדר כ-`repeat(3,1fr)` ל-3 עמודות

---

## אם Supabase לא עובד - פתרון חלופי

אם התמונות מ-Supabase לא נטענות, השתמש ישירות בתמונות מהאתר:

```javascript
// In "Extracts the Product Image Data" node
// Use source site images instead of Supabase

function extractImages(md) {
  // Existing code...
  const wp = urls.filter(u => u.includes("/wp-content/uploads/"));
  const main = wp[0] || urls[0] || "";
  return { main_image: main, gallery_images: gallery };
}
```

אין צורך ב-Supabase אם התמונות כבר על השרת שלך!

---

## קובץ HTML לדוגמה - להעלאה ישירה ל-WordPress

ראה קובץ נפרד: `PRODUCT_CARD_HTML_Reference.html`

זה מכיל דוגמה עובדת של תצוגת מוצרים שאפשר להעתיק ישירות ל-WordPress.
