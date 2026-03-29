const productList = document.getElementById("product-list");
const statusMessage = document.getElementById("status-message");

function createProductTile(product, index) {
  const article = document.createElement("article");
  article.className = "product-tile";
  article.style.animationDelay = `${index * 0.12}s`;

  article.innerHTML = `
    <div class="product-tile__badge">Product</div>
    <h2>${product.name}</h2>
    <p><strong>Brand:</strong> ${product.brand}</p>
    <p><strong>Price:</strong> Rs. ${product.price}</p>
    <p><strong>Quantity:</strong> ${product.quantity}</p>
    <p><strong>Category:</strong> ${product.category || "No Category"}</p>
  `;

  return article;
}

async function loadProducts() {
  try {
    statusMessage.textContent = "Fetching products from API...";

    const response = await fetch("http://127.0.0.1:8000/product-csr/products/");
    console.log("API response object:", response);

    const data = await response.json();
    console.log("Incoming product data:", data);

    productList.innerHTML = "";

    if (!data.products || data.products.length === 0) {
      statusMessage.textContent = "No products available right now.";
      productList.innerHTML = `
        <div class="empty-state">
          No products found in the API response.
        </div>
      `;
      return;
    }

    statusMessage.textContent = `Loaded ${data.products.length} product(s).`;

    data.products.forEach((product, index) => {
      const tile = createProductTile(product, index);
      productList.appendChild(tile);
    });
  } catch (error) {
    console.error("Failed to fetch products:", error);
    statusMessage.textContent = "Failed to load products.";
    productList.innerHTML = `
      <div class="error-state">
        Could not fetch product data. Please check backend server or CORS settings.
      </div>
    `;
  }
}

loadProducts();
