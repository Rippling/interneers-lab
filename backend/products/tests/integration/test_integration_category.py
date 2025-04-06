import pytest
import json
import mongoengine
from decimal import Decimal
from bson import ObjectId
from rest_framework import status
from django.urls import reverse

class TestCategoryAPI:

    # GET ALL CATEGORIES
    @pytest.mark.django_db
    def test_get_all_categories_success(self, api_client, db):
     
        response = api_client.get('/api/categories/all')
        assert response.status_code == status.HTTP_200_OK
        
        if 'results' in response.data:
            # Paginated response
            categories = response.data['results']
            assert len(categories) > 0
            assert response.data['count'] == 3
            assert 'next' in response.data
            assert 'previous' in response.data
            
            # Test category structure
            first_category = categories[0]
            assert 'id' in first_category
            assert 'title' in first_category
            assert 'description' in first_category
            assert first_category['title'] == 'Electronics'
        else:
            # Non-paginated response
            categories = response.data
            assert len(categories) == 3


    # GET CATEGORY BY ID
    @pytest.mark.django_db
    def test_get_category_by_id_success(self, api_client, db):
       
        category_id = str(db['categories']['electronics'].id)
        response = api_client.get(f'/api/categories/id/{category_id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Electronics'
        assert response.data['description'] == 'Electronic devices and accessories'
        assert '_id' in response.data or 'id' in response.data

    @pytest.mark.django_db
    def test_get_category_by_id_invalid_format(self, api_client, db):
       
        invalid_id = "invalid_format"
        response = api_client.get(f'/api/categories/id/{invalid_id}/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert 'Invalid ID format' in str(response.data['error'])

    @pytest.mark.django_db
    def test_get_category_by_id_not_found(self, api_client, db):

        non_existent_id = str(ObjectId())
        response = api_client.get(f'/api/categories/id/{non_existent_id}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'detail' in response.data
        assert response.data['detail'] == "Category not found"
    
    # GET CATEGORY BY TITLE
    @pytest.mark.django_db
    def test_get_category_by_title_success(self, api_client, db):

        response = api_client.get('/api/categories/title/Electronics/')
        
        print("RESPONSE DATA:", response.data)  

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) > 0
        for product in response.data:
            assert 'category' in product
            assert 'Electronics' in product['category']

    @pytest.mark.django_db
    def test_get_category_by_title_case_insensitive(self, api_client, db):

        response = api_client.get('/api/categories/title/electronics/')
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) > 0
        for product in response.data:
            assert 'category' in product
            assert 'Electronics' in product['category']


    @pytest.mark.django_db
    def test_get_category_by_title_not_found(self, api_client, db):

        response = api_client.get('/api/categories/title/NonExistentCategory/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'error' in response.data

    @pytest.mark.django_db
    def test_get_category_by_title_with_special_chars(self, api_client, db):

        response = api_client.get('/api/categories/title/Special@Category!/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    # CREATE CATEGORY
    @pytest.mark.django_db
    def test_create_category_success(self, api_client, db):

        new_category = {
            'title': 'Books',
            'description': 'Fiction and non-fiction books'
        }
        
        response = api_client.post('/api/categories/', new_category, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['category']['title'] == 'Books'
        assert 'message' in response.data
        assert response.data['message'] == 'Category created successfully'
        
        # Verify the category was added
        response = api_client.get('/api/categories/title/Books/')
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_create_category_duplicate_title(self, api_client, db):

        new_category = {
            'title': 'Unique',
            'description': 'Original category'
        }
        
        # Create first category
        api_client.post('/api/categories/', new_category, format='json')
        
        # Try to create duplicate
        response = api_client.post('/api/categories/', new_category, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    @pytest.mark.django_db
    def test_create_category_missing_title(self, api_client, db):

        invalid_category = {
            'description': 'Missing title field'
        }
        response = api_client.post('/api/categories/', invalid_category, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'title' in response.data
        assert response.data['title'][0] == 'This field is required.'

    @pytest.mark.django_db
    def test_create_category_empty_title(self, api_client, db):

        invalid_category = {
            'title': '',
            'description': 'Empty title'
        }
        response = api_client.post('/api/categories/', invalid_category, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'][0] == 'This field may not be blank.'

  
    
    # UPDATE CATEGORY
    @pytest.mark.django_db
    def test_update_category_success(self, api_client, db):

        new_category = {
            'title': 'TestUpdate',
            'description': 'Will be updated'
        }
        
        create_response = api_client.post('/api/categories/', new_category, format='json')
        assert create_response.status_code == status.HTTP_201_CREATED

        updated_data = {
            'title': 'TestUpdate',
            'description': 'Updated description'
        }

        #  Corrected update URL
        response = api_client.put('/api/categories/TestUpdate/update', updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Category updated successfully'
        assert response.data['category']['description'] == 'Updated description'

        #  Confirm it's updated
        response = api_client.get('/api/categories/title/TestUpdate/')
        assert response.status_code == status.HTTP_200_OK
        for product in response.data:
            assert 'Updated description' in product['description']

    @pytest.mark.django_db
    def test_update_category_not_found(self, api_client, db):
        """Test updating a non-existent category fails"""
        updated_data = {
            'title': 'NonExistent',
            'description': 'Updated description'
        }
        
        response = api_client.put('/api/categories/title/NonExistent/', updated_data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'error' in response.data

    @pytest.mark.django_db
    def test_update_category_missing_fields(self, api_client, db):

        # First create a test category
        new_category = {
            'title': 'TestPartial',
            'description': 'Will test partial update'
        }
        
        api_client.post('/api/categories/', new_category, format='json')
        
        # Test partial update (missing fields)
        partial_data = {'description': 'Partial update'}
        response = api_client.put('/api/categories/title/TestPartial/', partial_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'title' in response.data
        assert response.data['title'][0] == 'This field is required.'

    # DELETE CATEGORY
    @pytest.mark.django_db
    def test_delete_category_success(self, api_client, db):

        # First create a temporary category
        new_category = {
            'title': 'Temporary',
            'description': 'Will be deleted'
        }
        
        create_response = api_client.post('/api/categories/', new_category, format='json')
        assert create_response.status_code == status.HTTP_201_CREATED
        
        # Now delete it
        response = api_client.delete('/api/categories/title/Temporary/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Category deleted successfully'
        
        # Verify it's gone
        response = api_client.get('/api/categories/title/Temporary/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_delete_category_not_found(self, api_client, db):

        response = api_client.delete('/api/categories/title/NonExistent/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'error' in response.data

    @pytest.mark.django_db
    def test_delete_category_with_products(self, api_client, db):

        # Test deleting category with products (assuming this should be prevented)
        response = api_client.delete('/api/categories/title/Electronics/')
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            # Expected response if deletion is prevented due to existing products
            assert 'error' in response.data
            assert 'cannot delete' in response.data['error'].lower() or 'has products' in response.data['error'].lower()
    
    # GET PRODUCTS BY CATEGORY
    @pytest.mark.django_db
    def test_get_products_by_category_success(self, api_client, db):

        response = api_client.get('/api/categories/title/Electronics/')
        
        assert response.status_code == status.HTTP_200_OK
        products = response.data
        
        # Should return 3 electronics products
        assert len(products) == 3
        product_names = [product['name'] for product in products]
        assert 'Smartphone X' in product_names
        assert 'Laptop Pro' in product_names
        assert 'Smart Watch' in product_names
        
        # Test each product has required fields
        for product in products:
            assert 'id' in product or '_id' in product
            assert 'name' in product
            assert 'price' in product
            assert 'description' in product


    @pytest.mark.django_db
    def test_get_products_by_category_not_found(self, api_client, db):

        response = api_client.get('/api/categories/title/NonExistent/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'error' in response.data
    
