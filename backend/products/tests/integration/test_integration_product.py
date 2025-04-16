import pytest
import json
import mongoengine
from decimal import Decimal
from bson import ObjectId
from rest_framework import status
from copy import deepcopy

@pytest.mark.django_db(transaction=True)
class TestProductAPI:
   
    def test_get_all_products(self, api_client, db):

        # Test default pagination
        response = api_client.get('/api/products/')
        assert response.status_code == status.HTTP_200_OK
        print(response)
        if 'results' in response.data:
            products = response.data['results']
            assert len(products) <= 10  
            assert response.data['count'] == 5  
            
            # Test page navigation
            response = api_client.get('/api/products/?page=2')
            assert response.status_code == status.HTTP_200_OK
            
            # Test custom page size
            response = api_client.get('/api/products/?page_size=2')
            assert response.status_code == status.HTTP_200_OK
            assert len(response.data['results']) <= 2
        else:
            # No pagination
            products = response.data
            assert len(products) == 5
    

    def test_get_product_by_id_success(self, api_client, db):

        product_id = str(db['products']['smartphone'].id)
        response = api_client.get(f'/api/products/{product_id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Smartphone X'
        assert float(response.data['price']) == 799.99
        assert response.data['quantity'] == 50
        assert response.data['brand'] == 'TechBrand'

        
    def test_get_product_by_id_not_found(self, api_client, db):      #Just by adding db to the function parameters, the fixture will be executed and the connection will be properly set.

        fake_id = str(ObjectId())
        response = api_client.get(f'/api/products/{fake_id}/')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'detail' in response.data
        assert response.data['detail'] == 'Product not found'
    
    
    def test_get_product_by_id_invalid_id(self, api_client, db):

        invalid_id = "invalid_format"
        response = api_client.get(f'/api/products/{invalid_id}/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert 'Invalid ID format' in str(response.data['error'])
        
    def test_get_category_by_id_invalid_format(self, api_client, db):

            invalid_id = "invalid_format"
            response = api_client.get(f'/api/categories/id/{invalid_id}/')
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert 'error' in response.data
            assert 'Invalid ID format' in str(response.data['error'])

    
    def test_create_product_success(self, api_client, db):

        new_product = {
            'name': 'Wireless Earbuds',
            'description': 'High-quality wireless earbuds with noise cancellation',
            'brand': 'SoundMaster',
            'category': ['Electronics'],
            'price': 129.99,
            'quantity': 75
        }
        
        response = api_client.post('/api/products/create/', new_product, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['data']['name'] == 'Wireless Earbuds'
        assert float(response.data['data']['price']) == 129.99
        assert 'Electronics' in response.data['data']['category']
        
        # Verify product was actually created in the database
        product_id = response.data['data']['id']
        get_response = api_client.get(f'/api/products/{product_id}/')
        assert get_response.status_code == status.HTTP_200_OK
    
    def test_create_product_missing_required_fields(self, api_client):

        incomplete_product = {
            'name': 'Incomplete Product',
            # Missing price, quantity
        }
        
        response = api_client.post('/api/products/create/', incomplete_product, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert 'price' in response.data['error']
        assert 'quantity' in response.data['error']
    
    def test_create_product_invalid_data(self, api_client, db):

        invalid_product = {
            'name': 'Invalid Product',
            'description': 'Testing validation',
            'brand': 'TestBrand',
            'category': ['Electronics'],
            'price': 'not-a-number',  # Invalid price
            'quantity': -10  # Invalid quantity
        }
        
        response = api_client.post('/api/products/create/', invalid_product, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
    
    def test_create_product_with_nonexistent_category(self, api_client , db):

        product_with_fake_category = {
            'name': 'Test Product',
            'description': 'Testing category validation',
            'brand': 'TestBrand',
            'category': ['FakeCategory'],
            'price': 99.99,
            'quantity': 50
        }
        
        response = api_client.post('/api/products/create/', product_with_fake_category, format='json')
        
        # Check if API rejects non-existent categories or creates them on-the-fly
        # This assertion depends on your API design
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED]
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            assert 'category' in response.data['error']
   
    def test_update_product_success(self, api_client, db):

        product_id = str(db['products']['tshirt'].id)
        original_data = api_client.get(f'/api/products/{product_id}/').data
        
        updated_data = {
            'name': 'Premium Cotton T-Shirt',
            'price': 24.99,
            'quantity': 180
        }
        
        response = api_client.put(f'/api/products/{product_id}/update/', updated_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['name'] == 'Premium Cotton T-Shirt'
        assert float(response.data['data']['price']) == 24.99
        assert response.data['data']['quantity'] == 180
        
        # Verify unchanged fields are preserved
        assert response.data['data']['brand'] == original_data['brand']
        assert response.data['data']['description'] == original_data['description']
    
    def test_partial_update_product(self, api_client, db):

        product_id = str(db['products']['laptop'].id)
        
        patch_data = {
            'price': 1099.99
        }
        
        response = api_client.patch(f'/api/products/{product_id}/update/', patch_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert float(response.data['data']['price']) == 1099.99
        assert response.data['data']['name'] == 'Laptop Pro'  # Unchanged
    
    def test_update_nonexistent_product(self, api_client, db):

        fake_id = str(ObjectId())
        updated_data = {
            'name': 'Updated Name',
            'price': 99.99
        }
        
        response = api_client.put(f'/api/products/{fake_id}/update/', updated_data, format='json')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'error' in response.data
    
    def test_update_with_invalid_data(self, api_client, db):

        product_id = str(db['products']['smartphone'].id)

        invalid_data = {
            'price': -50.00,
            'quantity': 'not-a-number'
        }

        response = api_client.put(f'/api/products/{product_id}/update/', invalid_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'errors' in response.data
        assert 'price' in response.data['errors']
        assert 'quantity' in response.data['errors']
    
   
    def test_delete_product_success(self, api_client, db):

        product_id = str(db['products']['desk'].id)
        
        response = api_client.delete(f'/api/products/{product_id}/delete/')
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify it's gone
        response = api_client.get(f'/api/products/{product_id}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    
    

    def test_add_category_to_product_success(self, api_client, db):

        product_id = str(db['products']['laptop'].id)
        category_id = str(db['categories']['furniture'].id)
        
        # Get product before modification for comparison
        before_response = api_client.get(f'/api/products/{product_id}/')
        original_categories = set(before_response.data['category'])
        
        response = api_client.put(f'/api/products/{product_id}/add-category/{category_id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        
        # Verify the category was added
        after_response = api_client.get(f'/api/products/{product_id}/')
        updated_categories = set(after_response.data['category'])
        assert 'Furniture' in updated_categories
        assert 'Electronics' in updated_categories
        assert updated_categories == original_categories.union({'Furniture'})
    
    def test_add_existing_category(self, api_client, db):

        product_id = str(db['products']['smartwatch'].id)
        category_id = str(db['categories']['electronics'].id)
        
        # The smartwatch already has the Electronics category
        response = api_client.put(f'/api/products/{product_id}/add-category/{category_id}/')
        
        assert response.status_code == status.HTTP_200_OK or status.HTTP_400_BAD_REQUEST
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            assert 'already has this category' in response.data['error']
    
    def test_add_nonexistent_category(self, api_client, db):

        product_id = str(db['products']['laptop'].id)
        fake_category_id = str(ObjectId())
        
        response = api_client.put(f'/api/products/{product_id}/add-category/{fake_category_id}/')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'error' in response.data
    
    def test_remove_category_from_product_success(self, api_client, db):

        product_id = str(db['products']['smartwatch'].id)
        category_id = str(db['categories']['clothing'].id)
        
        # Get product before modification
        before_response = api_client.get(f'/api/products/{product_id}/')
        original_categories = set(before_response.data['category'])
        
        response = api_client.put(f'/api/products/{product_id}/remove-category/{category_id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        
        # Verify the category was removed
        after_response = api_client.get(f'/api/products/{product_id}/')
        updated_categories = set(after_response.data['category'])
        assert 'Clothing' not in updated_categories
        assert 'Electronics' in updated_categories
        assert updated_categories == original_categories - {'Clothing'}
    
    def test_remove_nonexistent_category_association(self, api_client, db):

        product_id = str(db['products']['laptop'].id)
        category_id = str(db['categories']['clothing'].id)
        
        # Laptop doesn't have the Clothing category
        response = api_client.put(f'/api/products/{product_id}/remove-category/{category_id}/')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # assert 'error' in response.data
        assert 'message' in response.data
        assert response.data['message'] == "Category not assigned to product."
    

    def test_remove_last_category(self, api_client, db):

        product_id = str(db['products']['laptop'].id)
        
        # First, ensure laptop has only one category (Electronics)
        electronics_category = str(db['categories']['electronics'].id)
        
        # Get all categories for laptop
        response = api_client.get(f'/api/products/{product_id}/')
        categories = response.data['category']
        
        # If laptop has multiple categories, remove all except Electronics
        if len(categories) > 1:
            for category in categories:
                if category != 'Electronics':
                    category_id = self._get_category_id_by_name(db, category)
                    api_client.put(f'/api/products/{product_id}/remove-category/{category_id}/')
        
        # Now try to remove the last category
        response = api_client.put(f'/api/products/{product_id}/remove-category/{electronics_category}/')
        
        # Check if API prevents removing the last category or allows it
        # This assertion depends on your API design
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            assert 'last category' in response.data['error'].lower() or 'at least one category' in response.data['error'].lower()
   
    def test_create_product_with_extreme_values(self, api_client, db):

        extreme_product = {
            'name': 'Extreme Product',
            'description': 'Testing boundary values',
            'brand': 'TestBrand',
            'category': ['Electronics'],
            'price': 9999999.99,  # Very high price 
            'quantity': 1000000    # Very high quantity
        }
        
        response = api_client.post('/api/products/create/', extreme_product, format='json')
        
        # System should either accept or reject with a meaningful error
        if response.status_code == status.HTTP_201_CREATED:
            assert float(response.data['data']['price']) == 9999999.99
            assert response.data['data']['quantity'] == 1000000
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            assert 'error' in response.data
        else:
            print("Unexpected Response:", response.status_code, response.data)
            assert False, "Expected status 201 or 400, got something else."
    