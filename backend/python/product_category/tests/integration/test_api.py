from django.urls import reverse

def test_get_all_product_categories(client, seeded_categories):
    url = reverse("get_all_product_categories")
    response = client.get(url)

    assert response.status_code == 200

    data = response.json()
    product_category_data = data["product_category"]

    assert len(product_category_data) == 2

    names = [c["name"] for c in product_category_data]

    assert "Fruits" in names
    assert "Vegetables" in names

def test_get_all_product_categories_no_get(client):
    url = reverse("get_all_product_categories")
    response = client.post(url)
    assert response.status_code == 400    

def test_get_product_category_by_id(client, seeded_categories):
    category_id = seeded_categories[0]
    url = reverse("get_product_category_by_id", args=[category_id])
    response = client.get(url)
    assert response.status_code == 200
    product_category_data = response.json()
    assert product_category_data["id"] == str(category_id)
    assert product_category_data["name"] == "Fruits"  

def test_get_product_category_by_id_no_get(client, seeded_categories):
    category_id = seeded_categories[0]
    url = reverse("get_product_category_by_id", args=[category_id])
    response = client.post(url)
    assert response.status_code == 400

def test_create_product_category(client):
    url = reverse("create_product_category")
    data = {"name": "Dairy"}
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 200
    product_category_data = response.json()
    assert product_category_data["name"] == "Dairy"

def test_create_product_category_no_post(client):
    url = reverse("create_product_category")
    response = client.get(url)
    assert response.status_code == 400

def test_update_product_category(client, seeded_categories):
    category_id = seeded_categories[0]
    url = reverse("update_product_category", args=[category_id])
    data = {"name": "Fresh Fruits"}
    response = client.put(url, data, content_type="application/json")
    assert response.status_code == 200
    product_category_data = response.json()
    assert product_category_data["id"] == str(category_id)
    assert product_category_data["name"] == "Fresh Fruits"  

def test_update_product_category_not_found(client):
    category_id = "000000000000000000000000"
    url = reverse("update_product_category", args=[category_id])
    data = {"name": "Nonexistent"}
    response = client.put(url, data, content_type="application/json")
    assert response.status_code == 404

def test_update_product_category_no_put(client, seeded_categories):
    category_id = seeded_categories[0]
    url = reverse("update_product_category", args=[category_id])
    response = client.get(url)
    assert response.status_code == 400       

def test_delete_product_category(client, seeded_categories):
    category_id = seeded_categories[0]
    url = reverse("delete_product_category", args=[category_id])
    response = client.delete(url)
    
    assert response.status_code == 200
    # Verify the category is deleted
    get_url = reverse("get_product_category_by_id", args=[category_id])
    get_response = client.get(get_url)
    assert get_response.status_code == 404  

def test_delete_product_category_not_found(client): 
    # category id must be it must be a 12-byte input or a 24-character hex string
    category_id="000000000000000000000000"
    url = reverse("delete_product_category", args=[category_id])
    response = client.delete(url)
    assert response.status_code == 404

def test_delete_product_category_no_delete(client, seeded_categories):
    category_id = seeded_categories[0]
    url = reverse("delete_product_category", args=[category_id])
    response = client.get(url)
    assert response.status_code == 400

