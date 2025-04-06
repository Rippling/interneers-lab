from django.urls import reverse
from product.models.ProductModel import Product
from bson import ObjectId

class TestProductCategoryIntegration:

    def test_add_product_to_category(self, api_client, test_data):
        prod = next((p for p in test_data['products'] if p.name == "T-shirt"), None)
        new_categ = next((c for c in test_data['categories'] if c.title == "Electronics"), None)
        assert prod and new_categ

        original_category_id = prod.category.id
        url = reverse('category-product-management')
        payload = {
            "product_id": str(prod.id),
            "category_id": str(new_categ.id)
        }

        res = api_client.post(url, payload, format='json')
        assert res.status_code == 200, f"Expected 200 OK, got {res.status_code}: {res.content}"
        data = res.json()
        assert any(key in data for key in ("success", "message"))

        updated_prod = Product.objects.get(id=prod.id)
        assert updated_prod.category.id == new_categ.id
        assert updated_prod.category.id != original_category_id

    def test_remove_product_from_category(self, api_client, test_data):
        prod = next((p for p in test_data['products'] if p.name == "Laptop"), None)
        assert prod

        url = reverse('category-product-management')
        payload = {
            "product_id": str(prod.id)
        }

        res = api_client.delete(url, payload, format='json')
        assert res.status_code == 200, f"Expected 200 OK, got {res.status_code}: {res.content}"
        data = res.json()
        assert any(key in data for key in ("success", "message"))

        updated_prod = Product.objects.get(id=prod.id)
        assert updated_prod.category is None

    def test_get_method_not_allowed(self, api_client):
        url = reverse('category-product-management')
        res = api_client.get(url)
        assert res.status_code == 405, f"Expected 405 Method Not Allowed, got {res.status_code}"

    def test_add_product_to_nonexistent_category(self, api_client, test_data):
        prod = next((p for p in test_data['products'] if p.name == "T-shirt"), None)
        assert prod

        invalid_categ_id = str(ObjectId())
        url = reverse('category-product-management')
        payload = {
            "product_id": str(prod.id),
            "category_id": invalid_categ_id
        }

        res = api_client.post(url, payload, format='json')
        assert res.status_code == 404, f"Expected 404 Not Found, got {res.status_code}"

    def test_add_nonexistent_product(self, api_client, test_data):
        categ = next((c for c in test_data['categories']), None)
        assert categ

        invalid_prod_id = str(ObjectId())
        url = reverse('category-product-management')
        payload = {
            "product_id": invalid_prod_id,
            "category_id": str(categ.id)
        }

        res = api_client.post(url, payload, format='json')
        assert res.status_code == 404, f"Expected 404 Not Found, got {res.status_code}"

    def test_missing_fields_in_payload(self, api_client):
        url = reverse('category-product-management')

        payload = {
            "product_id": "some-id"
        }
        res = api_client.post(url, payload, format='json')
        assert res.status_code == 400, f"Expected 400 Bad Request, got {res.status_code}"

        payload = {
            "category_id": "some-id"
        }
        res = api_client.post(url, payload, format='json')
        assert res.status_code == 400, f"Expected 400 Bad Request, got {res.status_code}"

    def test_end_to_end_category_product_flow(self, api_client):
        #step 1 - create a new category
        categ_url = reverse('category-list')
        new_categ = {
            "title": "Gaming",
            "description": "Video games and gaming accessories"
        }

        categ_res = api_client.post(categ_url, new_categ, format='json')
        assert categ_res.status_code == 201, f"Expected 201 Created, got {categ_res.status_code}"
        categ_id = categ_res.json()['id']

        #step 2 - add product to that category
        prod_url = reverse('product-list')
        new_product = {
            "name": "Gaming Console",
            "description": "Next-gen gaming console",
            "category": categ_id,
            "price": 49999.99,
            "brand": "GameTech",
            "quantity": 20
        }

        prod_res = api_client.post(prod_url, new_product, format='json')
        assert prod_res.status_code == 201, f"Expected 201 Created, got {prod_res.status_code}"
        product_id = prod_res.json()['id']

        #step 3 - create another categ.
        another_categ = {
            "title": "Entertainment",
            "description": "Entertainment devices"
        }
        another_categ_res = api_client.post(categ_url, another_categ, format='json')
        assert another_categ_res.status_code == 201
        another_category_id = another_categ_res.json()['id']

        #step 4 - move prod to new categ.
        management_url = reverse('category-product-management')
        move_payload = {
            "product_id": product_id,
            "category_id": another_category_id
        }

        move_res = api_client.post(management_url, move_payload, format='json')
        assert move_res.status_code == 200
        assert any(key in move_res.json() for key in ("success", "message"))

        #step 5 - verify prod belongs to new categ.
        prod_detail_url = reverse('product-detail', kwargs={'prod_id': product_id})
        updated_prod_res = api_client.get(prod_detail_url)
        assert updated_prod_res.status_code == 200
        updated_product_data = updated_prod_res.json()
        assert updated_product_data['category'] == another_category_id

        #step 6 - check prod. appears in new categ. products list
        categ_prod_url = reverse('category-products', kwargs={'category_id': another_category_id})
        categ_prod_res = api_client.get(categ_prod_url)
        assert categ_prod_res.status_code == 200
        category_products = categ_prod_res.json()
        assert any(p['id'] == product_id for p in category_products)

        #step 7 - remove prod. from categ.
        remove_payload = {
            "product_id": product_id
        }
        remove_res = api_client.delete(management_url, remove_payload, format='json')
        assert remove_res.status_code == 200
        assert any(key in remove_res.json() for key in ("success", "message"))

        #step 8 - verify categ. is now None
        final_prod_res = api_client.get(prod_detail_url)
        assert final_prod_res.status_code == 200
        final_product_data = final_prod_res.json()
        assert final_product_data['category'] is None
