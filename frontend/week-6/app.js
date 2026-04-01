getprods = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8001/api/product/');
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            product = data[12];


            document.getElementById("title").innerText = product.name;
            document.getElementById("desc").innerText = product.description;
            document.getElementById("brand").innerText = product.brand;
        }
        else {
            throw new Error("Failed to fetch!")

        }
    } catch (error) {
        console.error('Error: ', error)
    }

}

getprods()