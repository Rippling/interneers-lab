import pytest
from unittest.mock import patch, MagicMock
from django.http import Http404
from bson import ObjectId
from products.services.ProductService import ProductService
from rest_framework.exceptions import ErrorDetail

@pytest.mark.django_db
class TestProductService:

    @patch("products.repositories.ProductRepository.ProductRepository.createProd")
    @patch("products.serializers.ProductSerializer.is_valid")
    @patch("products.serializers.ProductSerializer", autospec=True)  
    def test_create_product_success(self, mock_serializer_class, mock_is_valid, mock_create_prod):
        # Create a mock instance of the ProductSerializer
        mock_serializer_instance = mock_serializer_class.return_value
        mock_serializer_instance.is_valid.return_value = True  # Simulate that the serializer is valid
        mock_serializer_instance.data = {"id": "12345", "name": "Test Product", "price": 100}  # Return actual dictionary directly

        mock_product = MagicMock()
        mock_product.id = "12345"
        mock_product.name = "Test Product"
        mock_product.price = 100
        mock_create_prod.return_value = mock_product
        
        product_data = {
            "name": "Test Product",
            "price": 100,
            "brand": "Test Brand",
            "category": [],
            "quantity": 10
        }
      
        result = ProductService.createProd(product_data)

        assert result["success"] is True
        assert result["data"]["name"] == "Test Product"  
        assert result["data"]["id"] == "12345"
        assert result["data"]["price"] == 100

    @patch("products.repositories.ProductRepository.ProductRepository.getProdById")
    def test_get_product_by_id_found(self, mock_get):
        
        mock_product = MagicMock()
        mock_product.id = ObjectId()
        
        # print(mock_product)
        mock_get.return_value = mock_product 

        result = ProductService.getProdById(mock_product.id)
        # print(result)
        assert result == mock_product


    @patch("products.repositories.ProductRepository.ProductRepository.getProdById")
    def test_get_product_by_id_not_found(self, mock_get):

        mock_get.return_value = None

        with pytest.raises(Http404, match="Product not found"):
            ProductService.getProdById(ObjectId())


    @patch("products.repositories.ProductRepository.ProductRepository.getAllProd")
    def test_get_all_products(self, mock_get_all):

        mock_get_all.return_value = [{"name": "Product 1"}, {"name": "Product 2"}]

        result = ProductService.getAllProds()
        # print(result)
        mock_get_all.assert_called_once()

        assert isinstance(result, list)
        assert len(result) == 2
        
    @patch("products.repositories.ProductRepository.ProductRepository.getAllProd")
    def test_get_all_products_empty(self, mock_get_all):

        mock_get_all.return_value = []

        result = ProductService.getAllProds()

        mock_get_all.assert_called_once()

        assert isinstance(result, list)
        assert len(result) == 0

    @patch("products.repositories.ProductRepository.ProductRepository.deleteProd")
    def test_delete_product_success(self, mock_delete):

        mock_delete.return_value = True

        result = ProductService.deleteProd(ObjectId())
        # print(result)
        assert result["success"] is True
        assert result["message"] == "Product deleted successfully"


    @patch("products.repositories.ProductRepository.ProductRepository.deleteProd")
    def test_delete_product_not_found(self, mock_delete):

        mock_delete.return_value = False

        with pytest.raises(Http404, match="Product not found"):
            ProductService.deleteProd(ObjectId())


    @patch("products.repositories.ProductRepository.ProductRepository.getProdById")
    @patch("products.serializers.ProductSerializer.save")
    def test_update_product_success(self, mock_save, mock_get_product):
       
        mock_product = MagicMock()
        mock_product.id = ObjectId()

        mock_get_product.return_value = mock_product  
        
       
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True  # Validation succeeds
        mock_save.return_value = mock_product

        with patch("products.serializers.ProductSerializer", return_value=mock_serializer):
            updated_data = {"name": "Updated Product Name", "price": 200}
            result = ProductService.updateProd(mock_product.id, updated_data)

            assert result == mock_product  
         


    @patch("products.repositories.ProductRepository.ProductRepository.getProdById")
    def test_update_product_not_found(self, mock_get_product):
        
        mock_get_product.return_value = None  
        
        updated_data = {"name": "Updated Product"}
        result = ProductService.updateProd(ObjectId(), updated_data)

        assert result is None 

    @patch("products.repositories.ProductRepository.ProductRepository.getProdById")
    def test_update_product_serializer_error(self, mock_get_product):

        mock_product = MagicMock()
        mock_product.id = ObjectId()

        mock_get_product.return_value = mock_product  # Simulate product found

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = False  # Validation fails
        mock_serializer.errors = {"price": [ErrorDetail(string='Price must be greater than zero.', code='invalid')]}

        with patch("products.serializers.ProductSerializer", return_value=mock_serializer):
            updated_data = {"price": -100}  # Invalid price
            # Now, match the error detail in the exception message
            with pytest.raises(Exception, match=r"{'price': \[ErrorDetail\(string='Price must be greater than zero.', code='invalid'\)\]}"):
                ProductService.updateProd(mock_product.id, updated_data)

    @patch("products.repositories.ProductRepository.ProductRepository.getProdById")
    @patch("products.repositories.Category.CategoryRepository.getCategoryById")
    @patch("products.repositories.ProductRepository.ProductRepository.update_product_categories")
    def test_remove_category_from_product_success(self, mock_update_categories, mock_get_category, mock_get_product):
        # Set up mocks
        mock_product = MagicMock()
        mock_category = MagicMock()
        mock_product.id = ObjectId()
        mock_category.id = ObjectId()
        mock_product.category = [mock_category]
        
        mock_get_product.return_value = mock_product
        mock_get_category.return_value = mock_category

        # Call the function under test
        result = ProductService.remove_category_from_product(mock_product.id, mock_category.id)
        
        # Assertions
        assert result == {"message": "Category removed from product successfully.", "status": 200}
        mock_update_categories.assert_called_once()


    @patch("products.repositories.ProductRepository.ProductRepository.getProdById")
    @patch("products.repositories.Category.CategoryRepository.getCategoryById")
    def test_remove_category_from_product_product_not_found(self, mock_get_category, mock_get_product):
     
        mock_get_product.return_value = None  # Simulate product not found
        
        with pytest.raises(Http404, match="Product not found"):
            ProductService.remove_category_from_product(ObjectId(), ObjectId())


    @patch("products.repositories.ProductRepository.ProductRepository.getProdById")
    @patch("products.repositories.Category.CategoryRepository.getCategoryById")
    def test_remove_category_from_product_category_not_found(self, mock_get_category, mock_get_product):
       
        mock_product = MagicMock()
        mock_product.id = ObjectId()

        mock_get_product.return_value = mock_product
        mock_get_category.return_value = None  # Simulate category not found

        with pytest.raises(Http404, match="Category not found"):
            ProductService.remove_category_from_product(mock_product.id, ObjectId())


    @patch("products.repositories.ProductRepository.ProductRepository.getProdById")
    @patch("products.repositories.Category.CategoryRepository.getCategoryById")
    def test_remove_category_from_product_category_not_assigned(self, mock_get_category, mock_get_product):
       
        mock_product = MagicMock()
        mock_category = MagicMock()
        mock_product.id = ObjectId()
        mock_category.id = ObjectId()
        mock_product.category = [mock_category]  # Product has a different category
        
        mock_get_product.return_value = mock_product
        mock_get_category.return_value = mock_category

        result = ProductService.remove_category_from_product(mock_product.id, ObjectId())  # Using a different category id
        
        assert result == {"message": "Category not assigned to product.", "status": 400}


    @patch("products.repositories.ProductRepository.ProductRepository.getProdById")
    @patch("products.repositories.Category.CategoryRepository.getCategoryById")
    def test_add_category_to_product_success(self, mock_get_category, mock_get_product):
       
        mock_product = MagicMock()
        mock_category = MagicMock()
        mock_product.id = ObjectId()
        mock_category.id = ObjectId()
        mock_product.category = []

        mock_get_product.return_value = mock_product
        mock_get_category.return_value = mock_category

        result = ProductService.add_category_to_product(mock_product.id, mock_category.id)
        
        assert result == {"message": "Category added to product successfully.", "status": 200}
        mock_product.save.assert_called_once()  


    @patch("products.repositories.ProductRepository.ProductRepository.getProdById")
    @patch("products.repositories.Category.CategoryRepository.getCategoryById")
    def test_add_category_to_product_category_already_assigned(self, mock_get_category, mock_get_product):
        
        mock_product = MagicMock()
        mock_category = MagicMock()
        mock_product.id = ObjectId()
        mock_category.id = ObjectId()
        mock_product.category = [mock_category]

        mock_get_product.return_value = mock_product
        mock_get_category.return_value = mock_category

        result = ProductService.add_category_to_product(mock_product.id, mock_category.id)  # Category is already assigned
        
        assert result == {"message": "Category already assigned to product.", "status": 400}
