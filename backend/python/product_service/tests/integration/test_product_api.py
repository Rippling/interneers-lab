from django.urls import reverse
import json

def test_list_products(client, seeded_products):
    url = reverse("list_products")
    response = client.get(url)

    assert response.status_code == 200

    products_data = response.json()

    assert len(products_data) == 2

    names = [p["name"] for p in products_data]

    assert "Apple" in names
    assert "Carrot" in names

def test_get_product_by_id(client, seeded_products):
    product_id = seeded_products[0]
    url = reverse("get_product", args=[product_id])
    response = client.get(url)
    assert response.status_code == 200
    product_data = response.json()
    assert product_data["id"] == str(product_id)
    assert product_data["name"] == "Apple"    

def test_create_product(client, seeded_categories):
    url = reverse("create_product")
    data = {
        "name": "Banana",
        "price": 12,
        "category": str(seeded_categories[0]),
        "brand": "Fruit Brand",
        "quantity": 30
    }
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 200
    get_url=reverse("get_product", args=[response.json()["id"]])
    get_response = client.get(get_url)
    product_data = get_response.json()
    assert product_data["name"] == "Banana" 

def test_create_product_invalid_price(client, seeded_categories):
    url = reverse("create_product")
    data = {
        "name": "Banana",
        "price": -5,
        "category": str(seeded_categories[0]),
        "brand": "Fruit Brand",
        "quantity": 30
    }
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 400
    assert response.json()["error"] == "Given Price is not valid"      

import json

def test_create_product_not_by_post(client, seeded_categories):
    url = reverse("create_product")

    data = {
        "name": "Banana",
        "price": 12,
        "category": str(seeded_categories[0]),
        "brand": "Fruit Brand",
        "quantity": 30
    }

    response = client.put(
        url,
        data=json.dumps(data),
        content_type="application/json"
    )

    assert response.status_code == 400    

def test_delete_product(client, seeded_products):
    product_id = seeded_products[0]
    url = reverse("delete_product", args=[product_id])
    response = client.delete(url)
    
    assert response.status_code == 200
    # Verify the product is deleted
    get_url = reverse("get_product", args=[product_id])
    get_response = client.get(get_url)
    assert get_response.status_code == 404   

def test_list_products_by_category_id(client, seeded_categories, seeded_products):
    category_id = seeded_categories[0]
    url = reverse("list_products_by_category_id", args=[category_id])
    response = client.get(url)
    assert response.status_code == 200
    products_data = response.json()
    assert len(products_data) == 1
    assert products_data[0]["name"] == "Apple" 

def test_list_products_by_category_not_by_get(client, seeded_categories):    
    category_id = seeded_categories[0]
    url = reverse("list_products_by_category_id", args=[category_id])
    response = client.post(url)
    assert response.status_code == 400

def test_remove_category_from_product(client, seeded_products):
    product_id = seeded_products[0]
    url = reverse("remove_category_from_product", args=[product_id])
    response = client.patch(url)
    assert response.status_code == 200
    get_url = reverse("get_product", args=[product_id])
    get_response = client.get(get_url)
    product_data = get_response.json()
    assert product_data["category"] is None

def test_remove_category_from_product_not_found(client):
    product_id = "000000000000000000000000"
    url = reverse("remove_category_from_product", args=[product_id])
    response = client.patch(url)
    assert response.status_code == 404
    

def test_remove_category_from_product_not_by_patch(client, seeded_products):
    product_id = seeded_products[0]
    url = reverse("remove_category_from_product", args=[product_id])
    response = client.post(url)
    assert response.status_code == 400        

def test_add_category_to_product(client, seeded_products, seeded_categories):
    product_id = seeded_products[0]
    category_id = seeded_categories[1]
    url = reverse("add_category_to_product", args=[product_id, category_id])
    response = client.patch(url)
    assert response.status_code == 200
    get_url = reverse("get_product", args=[product_id])
    get_response = client.get(get_url)
    product_data = get_response.json()
    assert product_data["category"] == str(category_id)

def test_add_category_to_product_not_found(client, seeded_categories):
    product_id = "000000000000000000000000"
    category_id = seeded_categories[0]
    url = reverse("add_category_to_product", args=[product_id, category_id])
    response = client.patch(url)
    assert response.status_code == 404

def test_add_category_to_product_not_by_patch(client, seeded_products, seeded_categories):
    product_id = seeded_products[0]
    category_id = seeded_categories[1]

    url = reverse("add_category_to_product", args=[product_id, category_id])

    response = client.post(url)
    
    print(response.status_code)
    print(response.json())

    assert response.status_code == 400
    assert response.json()["error"] == "PATCH method not used"