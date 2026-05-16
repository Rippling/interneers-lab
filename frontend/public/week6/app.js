/**
 * app.js — Inventory Management Frontend
 *
 * Week 6: Vanilla JavaScript consuming the Django REST API.
 *
 * What this file demonstrates:
 *   - fetch() API calls to the backend
 *   - DOM manipulation to render dynamic HTML
 *   - Event listeners (click, input, keydown)
 *   - console.log for API response inspection (open DevTools!)
 *   - Error handling and UI state management
 *   - Pagination state
 */

// ── Config ──────────────────────────────────────────────────────────
const API_BASE = 'http://localhost:8000';
const PAGE_SIZE = 9;  // number of products per grid page

// ── State ───────────────────────────────────────────────────────────
let currentPage = 1;
let totalPages   = 1;
let currentFilters = {};

// ── DOM refs ─────────────────────────────────────────────────────────
const apiStatus      = document.getElementById('api-status');
const fetchBtn       = document.getElementById('fetch-btn');
const searchInput    = document.getElementById('search-input');
const minPriceInput  = document.getElementById('filter-min-price');
const maxPriceInput  = document.getElementById('filter-max-price');
const categorySelect = document.getElementById('filter-category');
const productGrid    = document.getElementById('product-grid');
const gridSection    = document.getElementById('grid-section');
const featuredSection= document.getElementById('featured-section');
const statsBar       = document.getElementById('stats-bar');
const emptyState     = document.getElementById('empty-state');
const prevBtn        = document.getElementById('prev-btn');
const nextBtn        = document.getElementById('next-btn');

// ── Helpers ──────────────────────────────────────────────────────────

/**
 * Formats a price number as a dollar string.
 * e.g. 999.9 → "$999.90"
 */
function formatPrice(price) {
  if (price == null) return '—';
  return '$' + parseFloat(price).toFixed(2);
}

/**
 * Truncates text to a given length with an ellipsis.
 */
function truncate(str, max = 80) {
  if (!str) return '—';
  return str.length > max ? str.slice(0, max) + '…' : str;
}

/**
 * Returns a stock status class based on quantity.
 */
function stockClass(qty) {
  return qty <= 5 ? 'low' : '';
}

/**
 * Sets the API status indicator in the header.
 */
function setApiStatus(state, text) {
  apiStatus.textContent = '● ' + text;
  apiStatus.className = 'nav-status ' + state;
}

/**
 * Builds the query string from current filters and page state.
 */
function buildQueryString(page = 1) {
  const params = new URLSearchParams();
  params.set('page', page);
  params.set('page_size', PAGE_SIZE);

  if (currentFilters.search)    params.set('search', currentFilters.search);
  if (currentFilters.minPrice)  params.set('min_price', currentFilters.minPrice);
  if (currentFilters.maxPrice)  params.set('max_price', currentFilters.maxPrice);
  if (currentFilters.categoryId) params.set('category_ids', currentFilters.categoryId);

  return params.toString();
}

// ── Category loader ──────────────────────────────────────────────────

/**
 * Fetches all categories from the API and populates the filter dropdown.
 * Logs raw API response to console so you can inspect it in DevTools.
 */
async function loadCategories() {
  try {
    const response = await fetch(`${API_BASE}/categories/?page_size=50`);
    const data = await response.json();

    // ▸ Open browser DevTools Console to see this
    console.group('📂 Categories API response');
    console.log('Status:', response.status);
    console.log('Data:', data);
    console.groupEnd();

    if (data.categories && data.categories.length > 0) {
      data.categories.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat.id;
        option.textContent = cat.title;
        categorySelect.appendChild(option);
      });
    }
  } catch (err) {
    console.warn('Could not load categories:', err.message);
  }
}

// ── Featured tile updater ─────────────────────────────────────────────

/**
 * Updates the featured product tile with data from a product object.
 * This shows how to manipulate the DOM with JavaScript.
 */
function updateFeaturedTile(product) {
  const name     = document.getElementById('feat-name');
  const desc     = document.getElementById('feat-desc');
  const price    = document.getElementById('feat-price');
  const brand    = document.getElementById('feat-brand');
  const qty      = document.getElementById('feat-qty');
  const qtyDot   = document.getElementById('feat-qty-dot');
  const category = document.getElementById('feat-category');
  const id       = document.getElementById('feat-id');

  // Update text content — this is how DOM manipulation works
  name.textContent     = product.name;
  desc.textContent     = product.description;
  price.textContent    = formatPrice(product.price);
  brand.textContent    = product.brand?.toUpperCase() || '—';
  qty.textContent      = product.quantity;
  category.textContent = product.category?.title?.toUpperCase() || 'UNCATEGORIZED';
  id.textContent       = 'ID: ' + product.id;

  // Add low-stock class to the dot indicator
  qtyDot.className = 'qty-dot ' + stockClass(product.quantity);

  console.group('⭐ Featured product');
  console.log('Product:', product);
  console.log('DOM element updated:', document.getElementById('featured-tile'));
  console.groupEnd();
}

// ── Product card builder ──────────────────────────────────────────────

/**
 * Creates a product card DOM element from a product object.
 * Returns the element — caller decides where to insert it.
 *
 * This is the core DOM creation pattern:
 *   createElement → set properties → append children
 */
function buildProductCard(product) {
  const card = document.createElement('div');
  card.className = 'product-card';
  card.dataset.productId = product.id;

  card.innerHTML = `
    <div class="card-category">${product.category?.title || 'Uncategorized'}</div>
    <div class="card-name">${product.name}</div>
    <div class="card-desc">${truncate(product.description)}</div>
    <div class="card-footer">
      <span class="card-price">${formatPrice(product.price)}</span>
      <span class="card-stock">
        <span class="qty-dot ${stockClass(product.quantity)}"></span>
        ${product.quantity} in stock
      </span>
    </div>
  `;

  // Click to highlight and update the featured tile
  card.addEventListener('click', () => {
    // Remove highlight from all cards
    document.querySelectorAll('.product-card').forEach(c => c.classList.remove('highlighted'));
    // Highlight clicked card
    card.classList.add('highlighted');
    // Update the featured tile with this product's data
    updateFeaturedTile(product);
    // Scroll to featured tile
    featuredSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    console.log('🖱️ Card clicked — product:', product);
  });

  return card;
}

// ── Main fetch function ───────────────────────────────────────────────

/**
 * Fetches products from the API and renders the grid.
 *
 * This demonstrates:
 *   - async/await with fetch()
 *   - Building query strings for filtering
 *   - Updating multiple DOM elements based on API response
 *   - Error handling with try/catch
 *   - console.log for DevTools inspection
 */
async function fetchProducts(page = 1) {
  currentPage = page;

  // UI: loading state
  fetchBtn.classList.add('loading');
  fetchBtn.querySelector('.btn-text').textContent = 'Loading…';
  productGrid.innerHTML = '';

  // Build URL with query params
  const qs  = buildQueryString(page);
  const url = `${API_BASE}/products/?${qs}`;

  console.group(`🔄 Fetching products — page ${page}`);
  console.log('URL:', url);
  console.log('Filters:', currentFilters);

  try {
    const response = await fetch(url);

    // ▸ VIEW THIS IN DEVTOOLS — Network tab or Console
    console.log('Response status:', response.status, response.statusText);
    console.log('Response headers:', Object.fromEntries(response.headers.entries()));

    const data = await response.json();

    // ▸ This is the raw API response — expand it in DevTools to explore
    console.log('Raw API response:', data);
    console.groupEnd();

    if (!response.ok) {
      throw new Error(data.error || 'API returned an error');
    }

    // ── Render ────────────────────────────────────────────────────
    const products = data.products || [];

    // Update stats bar
    totalPages = data.total_pages || 1;
    document.getElementById('stat-total').textContent = data.total_products ?? '—';
    document.getElementById('stat-page').textContent  = data.page ?? '—';
    document.getElementById('stat-pages').textContent = totalPages;
    statsBar.style.display = 'flex';

    // Update pagination buttons
    prevBtn.disabled = page <= 1;
    nextBtn.disabled = page >= totalPages;

    if (products.length === 0) {
      // Empty state
      gridSection.style.display = 'none';
      emptyState.style.display  = 'block';
      document.getElementById('empty-title').textContent = 'No products found';
      document.getElementById('empty-sub').textContent   =
        Object.keys(currentFilters).length > 0
          ? 'Try adjusting your filters'
          : 'No products exist yet — create some via the API';
      setApiStatus('connected', 'Connected — 0 results');
      return;
    }

    emptyState.style.display  = 'none';
    gridSection.style.display = 'block';

    // Build and append cards
    // This loop shows how to dynamically create and insert DOM elements
    products.forEach(product => {
      const card = buildProductCard(product);
      productGrid.appendChild(card);
    });

    // Update featured tile with first product
    updateFeaturedTile(products[0]);

    setApiStatus('connected', `Connected — ${data.total_products} products`);

    // Log DOM tree summary for DevTools exploration
    console.group('🏗️ DOM update summary');
    console.log('Cards rendered:', products.length);
    console.log('Grid element:', productGrid);
    console.log('First card:', productGrid.firstElementChild);
    console.groupEnd();

  } catch (err) {
    console.error('❌ Fetch failed:', err);
    console.groupEnd();

    setApiStatus('error', 'Connection failed');
    emptyState.style.display  = 'block';
    gridSection.style.display = 'none';
    document.getElementById('empty-title').textContent = 'Could not reach API';
    document.getElementById('empty-sub').textContent   =
      'Make sure your Django server is running on localhost:8000';

  } finally {
    // Always restore button state
    fetchBtn.classList.remove('loading');
    fetchBtn.querySelector('.btn-text').textContent = 'Load Products';
  }
}

// ── Event listeners ───────────────────────────────────────────────────

/**
 * Collect current filter values into the state object.
 * Called before every fetch.
 */
function collectFilters() {
  currentFilters = {};
  const search   = searchInput.value.trim();
  const minPrice = minPriceInput.value.trim();
  const maxPrice = maxPriceInput.value.trim();
  const catId    = categorySelect.value;

  if (search)   currentFilters.search    = search;
  if (minPrice) currentFilters.minPrice  = minPrice;
  if (maxPrice) currentFilters.maxPrice  = maxPrice;
  if (catId)    currentFilters.categoryId = catId;

  // Log to console — useful for DevTools inspection
  console.log('📋 Active filters:', currentFilters);
}

// Fetch button
fetchBtn.addEventListener('click', () => {
  collectFilters();
  fetchProducts(1);
});

// Enter key in search also triggers fetch
searchInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    collectFilters();
    fetchProducts(1);
  }
});

// Pagination
prevBtn.addEventListener('click', () => {
  if (currentPage > 1) fetchProducts(currentPage - 1);
});

nextBtn.addEventListener('click', () => {
  if (currentPage < totalPages) fetchProducts(currentPage + 1);
});

// ── Initialise ────────────────────────────────────────────────────────

/**
 * Runs when the page loads.
 * Loads categories for the dropdown, then fetches the first page of products.
 */
async function init() {
  console.group('🚀 Inventory app initialised');
  console.log('API base:', API_BASE);
  console.log('Page size:', PAGE_SIZE);
  console.log('Tip: Expand the objects below to explore the API response structure!');
  console.groupEnd();

  setApiStatus('', 'Connecting…');

  await loadCategories();
  await fetchProducts(1);
}

// Kick off when DOM is ready
document.addEventListener('DOMContentLoaded', init);