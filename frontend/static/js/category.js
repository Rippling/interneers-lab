document.addEventListener('DOMContentLoaded', function () { 
    const path = window.location.pathname;
    console.log(path);

    if (path === '/categories/page/') {
        fetch('/api/categories/all')
            .then(response => response.json())
            .then(data => {
                console.log(data);
                const container = document.getElementById('product-container');
                data.results.forEach(category => {
                    const div = document.createElement('div');
                    div.classList.add('product-card');
                    div.setAttribute('data-id', category.id);
                    div.dataset.category = JSON.stringify(category);

                    div.innerHTML = `
                        <h3>${category.title}</h3>
                        <p>Description: ${category.description}</p>
                        <hr/>
                   `;

                    div.addEventListener('click', function () {
                        const clickedCategory = JSON.parse(this.dataset.category); 
                        console.log(clickedCategory.title); 
                        window.location.href = `/categories/title/${clickedCategory.title}`; 
                    });

                    container.appendChild(div); 
                });

            })
            .catch(error => console.error('Error fetching categories:', error));
    } 

    else if (path.includes('/categories/title/')) {
        console.log("Dfdf");
        const pathParts = path.split('/');
        const categoryTitle = decodeURIComponent(pathParts[pathParts.length - 1]);

        fetch(`/api/categories/title/${categoryTitle}/`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                const container = document.getElementById('product-container');
                container.innerHTML = "";  

                if (data.length === 0) {
                    container.innerHTML = '<p>No products found for this category.</p>'; 
                    return;
                }

                data.forEach(product => {
                    const div = document.createElement('div');
                    div.classList.add('product-card');
                    div.setAttribute('data-id', product.id);

                    div.innerHTML = `
                        <h3>${product.name}</h3>
                        <p>Brand: ${product.brand}</p>
                        <p>Price: ₹${product.price}</p>
                    `;

                    div.addEventListener('click', function () {
                        const productId = this.getAttribute('data-id');
                        console.log(productId);  
                        window.location.href = `/products/${productId}/`; 
                    });

                    container.appendChild(div);
                });

            })
            .catch(error => {
                console.error('Error fetching products:', error);
                document.getElementById('product-container').innerHTML = '<p>Failed to load products.</p>'; 
            });
    }
});
