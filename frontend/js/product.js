async function loadProduct() {
    const params = new URLSearchParams(window.location.search);
    const productId = params.get("id");
    console.log("Product ID:", productId);

    const productTile = document.getElementById("product-tile");


    if (!productTile) {
        console.error("Element with id 'product-tile' not found!");
        return;
    }

    if (!productId) {
        productTile.innerHTML = "<p>Product ID not provided.</p>";
        return;
    }

    try {
        const response = await fetch(`http://localhost:8000/api/products/${productId}/`);
        if (!response.ok) throw new Error("Product not found");

        const product = await response.json();
        const sampleImage = product.image || "https://images.unsplash.com/photo-1591337676887-a217a6970a8a?q=80&w=2080&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D";

        productTile.innerHTML = `
            <h2>${product.name}</h2>
            <img src="${sampleImage}" alt="${product.name}" style="max-width: 400px;"/>
            <p><strong>Brand:</strong> ${product.brand}</p>
            <p><strong>Description:</strong> ${product.description}</p>
            <p><strong>Price:</strong> ₹${product.price}</p>
            <p><strong>Quantity:</strong> ${product.quantity}</p>
        `;
    } catch (err) {
        productTile.innerHTML = `<p>Error loading product: ${err.message}</p>`;
    }
}

window.addEventListener("DOMContentLoaded", loadProduct);
