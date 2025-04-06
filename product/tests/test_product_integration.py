from django.urls import reverse
from product.models.ProductModel import Product, ProductHistory
from bson import ObjectId

class TestProductAPI:

    def test_list_products(self,api_client,test_data):
        url=reverse('product-list')
        response=api_client.get(url)
        assert response.status_code == 200, "Expected 200 OK for product list"
        data=response.json()
        names=[p['name'] for p in data]
        for name in ["Smartphone", "T-shirt", "Python Programming", "Laptop"]:
            assert name in names, f"Product '{name}' should be in the list"

    def test_create_product(self,api_client,test_data):
        categ_id=str(next(cat for cat in test_data['categories'] if cat.title == "Electronics").id)
        url=reverse('product-list')
        new_product = {
            "name": "Headphones",
            "description": "Wireless headphones",
            "category": categ_id,
            "price": 11699.99,
            "brand": "AudioTech",
            "quantity": 75
        }
        response=api_client.post(url,new_product,format='json')
        assert response.status_code == 201, "Product creation should return 201"
        data=response.json()
        assert data['name'] == new_product['name'], "Name mismatch after creation"
        assert data['brand'] == new_product['brand'], "Brand mismatch after creation"

    def test_create_product_with_missing_field(self,api_client):
        url=reverse('product-list')
        response=api_client.post(url, {
            "name": "Missing Field Product"
        }, format='json')
        assert response.status_code == 400, "Missing required fields should return 400"
        data=response.json()
        expected_fields=["price", "brand", "quantity"]
        for field in expected_fields:
            assert field in data, f"{field} should be in the error response"
            assert data[field], f"{field} should have error message"

    def test_create_product_with_invalid_category(self, api_client):
        url=reverse('product-list')
        invalid_categ_id=str(ObjectId())  
        response=api_client.post(url, {
            "name": "Invalid Category Product",
            "description": "Invalid category",
            "category": invalid_categ_id,
            "price": 100,
            "brand": "FakeBrand",
            "quantity": 10
        }, format='json')
        assert response.status_code == 400
        assert "category" in response.data
        assert "Invalid" in response.data["category"][0] or "does not exist" in response.data["category"][0]

    def test_get_product_by_invalid_id(self,api_client):
        url=reverse('product-detail',kwargs={'prod_id':'invalidoid'})
        response=api_client.get(url)
        assert response.status_code == 404 or response.status_code == 400, "Invalid product ID should return 404 or 400"

    def test_get_product_by_id(self, api_client,test_data):
        prod=test_data['products'][0]
        url=reverse('product-detail',kwargs={'prod_id':str(prod.id)})
        response=api_client.get(url)
        assert response.status_code == 200, "Should return 200 for valid product"
        data=response.json()
        assert data['name'] == prod.name, "Product name mismatch"
        assert float(data['price']) == float(prod.price), "Product price mismatch"

    def test_update_product_no_change(self,api_client,test_data):
        prod=test_data['products'][0]
        prod_id=str(prod.id)
        original_data={
            "name": prod.name,
            "description": prod.description,
            "category": str(prod.category.id),
            "price": float(prod.price),
            "brand": prod.brand,
            "quantity": prod.quantity
        }
        url=reverse('product-detail',kwargs={'prod_id':prod_id})
        response=api_client.put(url,original_data,format='json')
        assert response.status_code == 200, "Update with no change should still return 200"
        assert response.json()['name'] == prod.name,"Name should remain unchanged"

    def test_update_product(self, api_client, test_data):
        prod=test_data['products'][0]
        prod_id=str(prod.id)
        updated_data={
            "name": "Smartphone Pro",
            "description": "Updated description",
            "category": str(prod.category.id),
            "price": 199999.99,
            "brand": "ProBrand",
            "quantity": 10
        }
        url=reverse('product-detail', kwargs={'prod_id':prod_id})
        response=api_client.put(url,updated_data,format='json')
        assert response.status_code == 200, "Product update should return 200"
        assert response.json()['name'] == "Smartphone Pro","Updated name mismatch"
        history=ProductHistory.objects(product_id=prod_id)
        assert len(history) >= 1, "Product history should exist after update"

    def test_delete_product(self,api_client,test_data):
        prod=test_data['products'][3]
        prod_id=str(prod.id)
        url=reverse('product-detail', kwargs={'prod_id': prod_id})
        response=api_client.delete(url)
        assert response.status_code == 204, "Product deletion should return 204"
        assert Product.objects.filter(id=prod_id).first() is None, "Product should no longer exist after deletion"

    def test_delete_non_existent_product(self,api_client):
        url=reverse('product-detail', kwargs={'prod_id': str(ObjectId())})
        response=api_client.delete(url)
        assert response.status_code == 404, "Deleting a non-existent product should return 404"

    def test_product_history(self,api_client,test_data):
        prod=test_data['products'][1]
        prod_id=str(prod.id)
        api_client.put(reverse('product-detail', kwargs={'prod_id': prod_id}), {
            "name": prod.name,
            "description": prod.description,
            "category": str(prod.category.id),
            "price": float(prod.price) + 10,
            "brand": prod.brand,
            "quantity": prod.quantity - 1
        }, format='json')
        url=reverse('product-history', kwargs={'prod_id': prod_id})
        response=api_client.get(url)
        assert response.status_code == 200, "History fetch should return 200"
        data=response.json()
        assert float(data[0]['price']) == float(prod.price), "Original price should be recorded in history"

    def test_recent_updated_products(self, api_client, test_data):
        prod=test_data['products'][2]
        prod_id=str(prod.id)
        update_data={
            "name": prod.name,
            "description": "New description",
            "category": str(prod.category.id),
            "price": float(prod.price),
            "brand": prod.brand,
            "quantity": prod.quantity
        }
        api_client.put(reverse('product-detail', kwargs={'prod_id': prod_id}), update_data, format='json')
        url=reverse('recent-updates')
        response=api_client.get(url)
        assert response.status_code == 200, "Fetching recent updates should return 200"
        data=response.json()
        updated_prod=[p for p in data if p['id'] == prod_id]
        assert updated_prod, "Updated product should appear in recent updates"
        assert updated_prod[0]['description'] == update_data['description'], "Description should match update"
