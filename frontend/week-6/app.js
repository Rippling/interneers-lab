getprods = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8001/api/product/');
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            const container = document.getElementById("product-list");

            container.innerHTML = "";

            data.forEach(product => {
                const card = document.createElement("div");
                card.className = "prodcard";

                card.innerHTML = `
                    <h2 class="title">${product.name}</h2>
                    <p class="desc">${product.description}</p>
                    <h4 class="brand">${product.brand}</h4>
                `;

                container.appendChild(card);
            });

        }
        else {
            throw new Error("Failed to fetch!")

        }
    } catch (error) {
        console.error('Error: ', error)
    }

}

getprods()