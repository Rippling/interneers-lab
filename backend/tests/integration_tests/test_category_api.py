import pytest
from rest_framework.test import APIClient
from bson import ObjectId

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestProductCategoryAPI:

    def test_create_category(self, api_client):
        response = api_client.post("/products/categories/", {
            "category_name": "Stationery",
            "description": "All office and school items",
            "is_active": True
        }, format='json')
        assert response.status_code == 201
        data = response.json()
        assert data["category_name"] == "Stationery"
        assert data["description"] == "All office and school items"

    def test_create_category_missing_fields(self, api_client):
        response = api_client.post("/products/categories/", {
            "description": "No name field",
            "is_active": True
        }, format='json')
        assert response.status_code == 400
        assert "category_name" in response.json()

    def test_get_all_categories(self, api_client):
        api_client.post("/products/categories/", {
            "category_name": "Books",
            "description": "All books",
            "is_active": True
        }, format='json')
        api_client.post("/products/categories/", {
            "category_name": "Games",
            "description": "All games",
            "is_active": True
        }, format='json')
        response = api_client.get("/products/categories/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2

    def test_get_category_by_valid_id(self, api_client):
        post_response = api_client.post("/products/categories/", {
            "category_name": "Music",
            "description": "Instruments and accessories",
            "is_active": True
        }, format='json')
        category_id = post_response.json()["id"]

        response = api_client.get(f"/products/categories/{category_id}/")
        assert response.status_code == 200
        assert response.json()["category_name"] == "Music"

    def test_get_category_by_invalid_id(self, api_client):
        response = api_client.get("/products/categories/invalid-id/")
        assert response.status_code == 400 or response.status_code == 404

    def test_get_category_by_nonexistent_id(self, api_client):
        fake_id = str(ObjectId())
        response = api_client.get(f"/products/categories/{fake_id}/")
        assert response.status_code == 404

    def test_update_category_success(self, api_client):
        post_response = api_client.post("/products/categories/", {
            "category_name": "Electronics",
            "description": "Gadgets and devices",
            "is_active": True
        }, format='json')
        category_id = post_response.json()["id"]

        update_response = api_client.put(f"/products/categories/{category_id}/", {
            "category_name": "Updated Electronics",
            "description": "Updated gadgets",
            "is_active": True
        }, format='json')
        assert update_response.status_code == 200
        updated_data = update_response.json()
        assert updated_data["category_name"] == "Updated Electronics"

    def test_update_category_with_invalid_id(self, api_client):
        response = api_client.put("/products/categories/invalid-id/", {
            "category_name": "Test",
            "description": "Test",
            "is_active": True
        }, format='json')
        assert response.status_code == 400 or response.status_code == 404

    def test_update_nonexistent_category(self, api_client):
        fake_id = str(ObjectId())
        response = api_client.put(f"/products/categories/{fake_id}/", {
            "category_name": "Ghost Category",
            "description": "Not real",
            "is_active": True
        }, format='json')
        assert response.status_code == 404

    def test_delete_category_success(self, api_client):
        post_response = api_client.post("/products/categories/", {
            "category_name": "To Be Deleted",
            "description": "Temporary",
            "is_active": True
        }, format='json')
        category_id = post_response.json()["id"]

        delete_response = api_client.delete(f"/products/categories/{category_id}/")
        assert delete_response.status_code == 204

        get_response = api_client.get(f"/products/categories/{category_id}/")
        assert get_response.status_code == 404

    def test_delete_category_invalid_id(self, api_client):
        response = api_client.delete("/products/categories/invalid-id/")
        assert response.status_code == 400 or response.status_code == 404

    def test_delete_nonexistent_category(self, api_client):
        fake_id = str(ObjectId())
        response = api_client.delete(f"/products/categories/{fake_id}/")
        assert response.status_code == 404
