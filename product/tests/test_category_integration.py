import pytest
from django.urls import reverse
from product.models.CategoryModel import ProductCategory
from bson import ObjectId

class TestCategoryAPI:

    def generate_fake_id(self):
        return str(ObjectId())

    def test_list_categories(self,api_client, test_data):
        url = reverse('category-list')
        response = api_client.get(url)
        assert response.status_code == 200
        titles = [c['title'] for c in response.json()]
        assert "Electronics" in titles
        assert "Clothing" in titles
        assert "Books" in titles

    def test_create_category(self,api_client):
        url = reverse('category-list')
        new_category = {
            "title": "Home Goods",
            "description": "Items for the home"
        }
        response=api_client.post(url,new_category,format='json')
        assert response.status_code == 201
        data=response.json()
        assert data['title'] == new_category['title']
        assert data['description'] == new_category['description']
        assert ProductCategory.objects.get(title="Home Goods")

    def test_create_category_missing_fields(self, api_client):
        url=reverse('category-list')
        response=api_client.post(url, {"description": "Missing title"}, format='json')
        assert response.status_code==400

    def test_get_category_by_id(self, api_client, test_data):
        categ = test_data['categories'][0]
        url = reverse('category-detail', kwargs={'category_id': str(categ.id)})
        response=api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data['title'] == categ.title
        assert data['description'] == categ.description

    def test_get_category_invalid_id(self, api_client):
        url=reverse('category-detail', kwargs={'category_id': self.generate_fake_id()})
        response=api_client.get(url)
        assert response.status_code == 404

    def test_search_category_by_title(self, api_client):
        ProductCategory.objects.create(title="Electronics", description="electronic gadgets")
        url=reverse('category-search', kwargs={'title': "Elec"})
        response=api_client.get(url)
        assert response.status_code == 200
        titles=[cat['title'] for cat in response.json()]
        assert "Electronics" in titles

    def test_search_category_no_match(self, api_client):
        url=reverse('category-search', kwargs={'title': 'InvalidCategory'})
        response=api_client.get(url)
        assert response.status_code == 200
        assert response.json() == []

    def test_update_category(self, api_client, test_data):
        categ=test_data['categories'][1]
        url=reverse('category-detail', kwargs={'category_id': str(categ.id)})
        update={
            "title": "Apparel",
            "description": "Updated description for clothing"
        }
        response = api_client.put(url,update,format='json')
        assert response.status_code == 200
        data = response.json()
        assert data['title'] == update['title']
        assert data['description'] == update['description']
        updated_category = ProductCategory.objects.get(id=categ.id)
        assert updated_category.title == update['title']

    def test_update_category_invalid(self,api_client,test_data):
        categ=test_data['categories'][1]
        url=reverse('category-detail', kwargs={'category_id': str(categ.id)})
        invalid_update = {
            "title": "",
            "description": "Missing title"
        }
        response = api_client.put(url,invalid_update,format='json')
        assert response.status_code == 400

    def test_delete_category(self,api_client,test_data):
        categ=test_data['categories'][2]
        url=reverse('category-detail', kwargs={'category_id': str(categ.id)})
        response=api_client.delete(url)
        assert response.status_code == 204
        with pytest.raises(ProductCategory.DoesNotExist):
            ProductCategory.objects.get(id=categ.id)

    def test_delete_nonexistent_category(self,api_client):
        url=reverse('category-detail', kwargs={'category_id': self.generate_fake_id()})
        response=api_client.delete(url)
        assert response.status_code == 404

    def test_get_products_in_category(self,api_client,test_data):
        categ = next(c for c in test_data['categories'] if c.title == "Electronics")
        url=reverse('category-products', kwargs={'category_id': str(categ.id)})
        response=api_client.get(url)
        assert response.status_code == 200
        names=[p['name'] for p in response.json()]
        assert "Smartphone" in names
        assert "Laptop" in names
