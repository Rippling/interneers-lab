const productList = document.getElementById("product-list");

function createProductTile(product) {
  const article = document.createElement("article");
  article.className = "product-tile";

  article.innerHTML = `
    <h2>${product.name}</h2>
    <p><strong>Brand:</strong> ${product.brand}</p>
    <p><strong>Price:</strong> ${product.price}</p>
    <p><strong>Quantity:</strong> ${product.quantity}</p>
    <p><strong>Category:</strong> ${product.category || "No Category"}</p>
  `;

  return article;
}

async function loadProducts() {
  try {
    const response = await fetch("http://127.0.0.1:8000/product-csr/products/");
    const data = await response.json();

    console.log("API response:", response);
    console.log("Incoming data:", data);

    productList.innerHTML = "";

    if (!data.products || data.products.length === 0) {
      productList.innerHTML = "<p>No products found.</p>";
      return;
    }

    data.products.forEach((product) => {
      const tile = createProductTile(product);
      productList.appendChild(tile);
    });
  } catch (error) {
    console.error("Failed to fetch products:", error);
    productList.innerHTML = "<p>Failed to load products.</p>";
  }
}

loadProducts();
