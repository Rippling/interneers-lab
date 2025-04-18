async function loadProducts() {
    const productList = document.getElementById("product-list");

    try {
        const response = await fetch("http://localhost:8000/api/products/");
        if (!response.ok) {
            throw new Error("Failed to fetch products.");
        }

        const data = await response.json();
        const products = data.results; // Extract the products array

        if (products.length === 0) {
            productList.innerHTML = "<p>No products available</p>";
            return;
        }

        products.forEach(product => {
            const productCard = document.createElement("div");
            productCard.className = "product-card";

            // Use product.image if available, else a placeholder image
            const productImageUrl = product.image || "https://images.unsplash.com/photo-1591337676887-a217a6970a8a?q=80&w=2080&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D";

            productCard.innerHTML = `
                <a href="product.html?id=${product.id}">
                    <h3>${product.name}</h3>
                    <img src="${productImageUrl}" alt="${product.name}" style="max-width:200px;">
                </a>
            `;

            productList.appendChild(productCard);
        });
    }
    catch (err) {
        productList.innerHTML = `<p>Error loading the products: ${err.message}</p>`;
    }
}

window.addEventListener("DOMContentLoaded", loadProducts);
