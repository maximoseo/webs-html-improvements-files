// N8N Code Node: Generate Product HTML Grid
// ==========================================
// This node takes product JSON array and generates WordPress-safe HTML product cards
//
// INPUT: items from "Extracts the Product Image Data" node
// OUTPUT: HTML string for product grid
//
// USAGE:
// 1. Add this node AFTER "Extracts the Product Image Data"
// 2. Connect "Extracts the Product Image Data" as input
// 3. This node outputs HTML strings to use in template
//
// IMPORTANT: Uses SOURCE SITE images directly (no Supabase needed)

/============================================
PRODUCT CARD HTML TEMPLATE
============================================
// This is the WordPress-safe, inline-CSS product card structure
// Key features:
// - Fixed 280px image container with flexbox centering
// - object-fit:contain (shows full image, no cropping)
// - min-height:380px on card (uniform height)
// - margin-top:auto on price (pushes to bottom)
// - hover effects with inline handlers
// - WordPress-safe inline CSS only

function generateProductCard(product, index) {
  // Extract product data with fallbacks
  const name = (product.title || product.name || '').trim();
  const url = (product.url || '#').trim();
  const image = (product.main_image || product.image || '').trim();
  const alt = name || 'תמונת מוצר';
  const price = (product.price || 'לצפייה בקטלוג').trim();
  
  // Skip if no image URL (mandatory field)
  if (!image) {
    return ''; // Skip products without images
  }
  
  // Validate URL
  if (!url || url === '#' || !url.startsWith('http')) {
    return ''; // Skip products without valid URL
  }
  
  // Generate unique ID for this card
  const cardId = 'product-card-' + index;
  
  // HTML card with proper WordPress-safe inline CSS
  return `<a href="${url}" style="display:flex;flex-direction:column;background:#fff;border:1px solid #e5e5e5;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.08);overflow:hidden;text-align:center;min-height:380px;text-decoration:none;color:inherit;" onmouseover="this.style.boxShadow='0 4px 16px rgba(0,0,0,0.12)';this.style.transform='translateY(-2px)'" onmouseout="this.style.boxShadow='0 2px 8px rgba(0,0,0,0.08)';this.style.transform='none'"><div style="height:280px;background:#f9f7f4;display:flex;align-items:center;justify-content:center;overflow:hidden;"><img src="${image}" alt="${alt}" style="width:100%;height:100%;object-fit:contain;padding:1rem;" loading="lazy"></div><h3 style="font-size:0.95rem;font-weight:600;padding:0.75rem 1rem 0.5rem;color:#2b2e34;font-family:'Assistant',Arial,sans-serif;margin:0;line-height:1.4;">${name}</h3><span style="font-size:0.9rem;color:#bc1f1f;font-weight:700;padding:0 1rem 1rem;display:block;margin-top:auto;">${price}</span></a>`;
}

function generateProductGrid(products, startIndex, count, gridClass) {
  // Slice the products array
  const gridProducts = products.slice(startIndex, startIndex + count);
  
  // Generate cards for valid products only
  const cards = [];
  for (let i = 0; i < gridProducts.length; i++) {
    const card = generateProductCard(gridProducts[i], startIndex + i);
    if (card) {
      cards.push(card);
    }
  }
  
  // If no valid cards, return empty
  if (cards.length === 0) {
    return '';
  }
  
  // Calculate actual columns (1, 2, or 3 based on valid cards)
  const cols = cards.length >= 3 ? 'repeat(3,1fr)' : (cards.length === 2 ? 'repeat(2,1fr)' : '1fr');
  
  // Return grid wrapper with cards
  return `<div style="display:grid;grid-template-columns:${cols};gap:1.5rem;margin:1.5rem 0;">${cards.join('')}</div>`;
}

// ============================================
// MAIN EXECUTION
// ============================================

// Get all products from input items
const allItems = $input.all();
const products = [];

// Extract valid products (must have url and main_image)
for (let i = 0; i < allItems.length; i++) {
  const item = allItems[i].json;
  if (item && item.url && item.main_image) {
    products.push(item);
  }
}

// If no products found, return empty response
if (products.length === 0) {
  return [
    {
      json: {
        top_grid: '',
        bottom_grid: '',
        top_grid_html: '',
        bottom_grid_html: '',
        top_products_count: 0,
        bottom_products_count: 0,
        total_products: 0,
        has_products: false
      }
    }
  ];
}

// Generate TOP grid (first 3 products)
const topGrid = generateProductGrid(products, 0, 3, 'top-grid');

// Generate BOTTOM grid (products 4-6, if available)
const bottomGrid = generateProductGrid(products, 3, 3, 'bottom-grid');

// Count valid products in each grid
const topCount = Math.min(products.length, 3);
const bottomStart = Math.min(products.length, 3);
const bottomCount = Math.max(0, Math.min(products.length - 3, 3));

// Return structured output
return [
  {
    json: {
      // HTML strings for direct injection into template
      top_grid: topGrid,
      bottom_grid: bottomGrid,
      
      // Also available as separate fields
      top_grid_html: topGrid,
      bottom_grid_html: bottomGrid,
      
      // Metadata for debugging
      top_products_count: topCount,
      bottom_products_count: bottomCount,
      total_products: products.length,
      has_products: products.length > 0,
      
      // Raw products array (for reference)
      products: products.slice(0, 6)
    }
  }
];

// ============================================
// NODE CONFIGURATION
// ============================================
/*
ADD THIS NODE TO YOUR N8N WORKFLOW:

1. Node Type: "Code"
2. Name: "Generate Product HTML"
3. Position: AFTER "Extracts the Product Image Data"

INPUT: Connect "Extracts the Product Image Data" node

OUTPUT: JSON with:
- top_grid: HTML string for top product grid (3 products)
- bottom_grid: HTML string for bottom product grid (products 4-6)
- top_products_count: Number of products in top grid
- bottom_products_count: Number of products in bottom grid
- total_products: Total valid products found
- has_products: Boolean indicating if any products exist

Then in your HTML template, replace:
- [PRODUCT_GRID_TOP] with {{ $json.top_grid }}
- [PRODUCT_GRID_BOTTOM] with {{ $json.bottom_grid }}
*/