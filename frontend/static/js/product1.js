document.addEventListener('DOMContentLoaded', function () {
   
    console.log("DOM fully loaded and parsed"); 
    let currentPage = 1;  // Initialize to the first page
    const productsPerPage = 4;  
    const container = document.getElementById('product-container');
    const paginationButtons = document.getElementById('pagination-buttons');

    function fetchProducts(page) {
        fetch(`/api/products/?page=${page}`)
        .then(response => response.json())
            .then(data => {
                console.log("Cvc" )
                console.log("Cvc" )
                    console.log("Cvc" )
                console.log("Cvc" , data);  
           
                container.innerHTML = '';
                paginationButtons.innerHTML = '';

                // Render products
                if (data.results.length === 0) {
                    container.innerHTML = '<p>No products found.</p>';
                } else {
                    data.results.forEach(product => {
                        const div = document.createElement('div');
                        div.classList.add('product-card');
                        div.setAttribute('data-id', product.id);

                        div.innerHTML = `
                            <div>
                                <h3>${product.name}</h3>
                                <p>Brand: ${product.brand}</p>
                                <p class="category">Category: ${product.category.join(', ')}</p>
                                <p class="price">Price: ₹${product.price}</p>
                                <hr/>
                            </div>
                        `;

                        div.addEventListener('click', function () {
                            const productId = this.getAttribute('data-id');
                            window.location.href = `/products/${productId}/`;
                        });


                        container.appendChild(div);
                    });
                }

                console.log("Rendering pagination buttons...");

// Render pagination buttons if needed
if (data.previous || data.next) {
    console.log('Pagination Info:', data.previous, data.next);  
    const totalPages = Math.ceil(data.count / productsPerPage);
    
    // Previous button
    if (data.previous) {
        const prevButton = document.createElement('button');
        prevButton.textContent = 'Previous';
        prevButton.addEventListener('click', function () {
            currentPage--;
            fetchProducts(currentPage);
        });
        paginationButtons.appendChild(prevButton);
    }

    // Page number buttons
    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement('button');
        button.textContent = i;
        button.addEventListener('click', function () {
            currentPage = i;
            fetchProducts(currentPage);
        });
        paginationButtons.appendChild(button);
    }

    // Next button
    if (data.next) {
        const nextButton = document.createElement('button');
        nextButton.textContent = 'Next';
        nextButton.addEventListener('click', function () {
            currentPage++;
            fetchProducts(currentPage);
        });
        paginationButtons.appendChild(nextButton);
    }
} else {
    paginationButtons.innerHTML = '<p>No more pages.</p>';
}

            })
            .catch(error => console.error('Error fetching products:', error));
    }

    fetchProducts(currentPage);
});        