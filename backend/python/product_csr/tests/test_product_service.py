from django.test import SimpleTestCase
from unittest.mock import MagicMock

from product_csr.services.product_service import ProductService



class ProductServiceTests(SimpleTestCase):
    def setUp(self):
        self.service = ProductService()
        self.service.repo = MagicMock()
        self.service.category_repo = MagicMock()

    def test_get_products_by_category_returns_serialized_products(self):
        category = MagicMock()
        product1 = MagicMock()
        product2 = MagicMock()

        product1.to_dict.return_value = {"id": "1", "name": "Phone"}
        product2.to_dict.return_value = {"id": "2", "name": "Laptop"}

        self.service.category_repo.get_by_id.return_value = category
        self.service.repo.get_by_category.return_value = [product1, product2]

        result = self.service.get_products_by_category("cat1")

        self.service.category_repo.get_by_id.assert_called_once_with("cat1")
        self.service.repo.get_by_category.assert_called_once_with(category)
        self.assertEqual(result, [
            {"id": "1", "name": "Phone"},
            {"id": "2", "name": "Laptop"},
        ])

    def test_get_products_by_category_raises_when_category_not_found(self):
        self.service.category_repo.get_by_id.return_value = None

        with self.assertRaisesMessage(ValueError, "Category not found"):
            self.service.get_products_by_category("cat1")

    def test_add_product_to_category_raises_when_product_not_found(self):
        self.service.repo.get_by_id.return_value = None
        self.service.category_repo.get_by_id.return_value = MagicMock()

        with self.assertRaisesMessage(ValueError, "Product not found"):
            self.service.add_product_to_category("prod1", "cat1")

    def test_add_product_to_category_raises_when_category_not_found(self):
        self.service.repo.get_by_id.return_value = MagicMock()
        self.service.category_repo.get_by_id.return_value = None

        with self.assertRaisesMessage(ValueError, "Category not found"):
            self.service.add_product_to_category("prod1", "cat1")

    def test_add_product_to_category_success(self):
        product = MagicMock()
        category = MagicMock()

        self.service.repo.get_by_id.return_value = product
        self.service.category_repo.get_by_id.return_value = category

        result = self.service.add_product_to_category("prod1", "cat1")

        self.assertEqual(product.category, category)
        product.save.assert_called_once()
        self.assertEqual(result, {"message": "Product added to category"})

    def test_remove_product_from_category_raises_when_product_not_found(self):
        self.service.repo.get_by_id.return_value = None

        with self.assertRaisesMessage(ValueError, "Product not found"):
            self.service.remove_product_from_category("prod1")

    def test_remove_product_from_category_success(self):
        product = MagicMock()
        self.service.repo.get_by_id.return_value = product

        result = self.service.remove_product_from_category("prod1")

        self.assertIsNone(product.category)
        product.save.assert_called_once()
        self.assertEqual(result, {"message": "Product removed from category"})

    def test_create_product_raises_when_name_missing(self):
        data = {
            "price": 100,
            "brand": "Apple",
            "quantity": 5,
        }

        with self.assertRaisesMessage(ValueError, "name is required"):
            self.service.create_product(data)

    def test_create_product_raises_when_price_missing(self):
        data = {
            "name": "Phone",
            "brand": "Apple",
            "quantity": 5,
        }

        with self.assertRaisesMessage(ValueError, "price is required"):
            self.service.create_product(data)

    def test_create_product_raises_when_brand_missing(self):
        data = {
            "name": "Phone",
            "price": 100,
            "quantity": 5,
        }

        with self.assertRaisesMessage(ValueError, "brand is required"):
            self.service.create_product(data)

    def test_create_product_raises_when_quantity_missing(self):
        data = {
            "name": "Phone",
            "price": 100,
            "brand": "Apple",
        }

        with self.assertRaisesMessage(ValueError, "quantity is required"):
            self.service.create_product(data)

    def test_create_product_raises_when_price_is_required_for_zero_value(self):
        data = {
            "name": "Phone",
            "price": 0,
            "brand": "Apple",
            "quantity": 5,
          }

        with self.assertRaisesMessage(ValueError, "price is required"):
           self.service.create_product(data)


    def test_create_product_success(self):
        data = {
            "name": "Phone",
            "price": 1000,
            "brand": "Apple",
            "quantity": 5,
        }
        created_product = MagicMock()
        created_product.to_dict.return_value = {
            "id": "1",
            "name": "Phone",
            "price": 1000,
            "brand": "Apple",
            "quantity": 5,
        }

        self.service.repo.create.return_value = created_product

        result = self.service.create_product(data)

        self.service.repo.create.assert_called_once_with(data)
        self.assertEqual(result, {
            "id": "1",
            "name": "Phone",
            "price": 1000,
            "brand": "Apple",
            "quantity": 5,
        })

    def test_get_all_products_without_filters_uses_get_all(self):
        product1 = MagicMock()
        product2 = MagicMock()

        product1.to_dict.return_value = {"id": "1", "name": "Phone"}
        product2.to_dict.return_value = {"id": "2", "name": "Laptop"}

        self.service.repo.get_all.return_value = [product1, product2]

        result = self.service.get_all_products()

        self.service.repo.get_all.assert_called_once()
        self.service.repo.filter_products.assert_not_called()
        self.assertEqual(result, [
            {"id": "1", "name": "Phone"},
            {"id": "2", "name": "Laptop"},
        ])

    def test_get_all_products_with_empty_filters_uses_get_all(self):
        product = MagicMock()
        product.to_dict.return_value = {"id": "1", "name": "Phone"}

        self.service.repo.get_all.return_value = [product]

        result = self.service.get_all_products({})

        self.service.repo.get_all.assert_called_once()
        self.service.repo.filter_products.assert_not_called()
        self.assertEqual(result, [{"id": "1", "name": "Phone"}])

    def test_get_all_products_with_filters_uses_filter_products(self):
        filters = {"brand": "Apple"}
        product = MagicMock()
        product.to_dict.return_value = {"id": "1", "name": "Phone", "brand": "Apple"}

        self.service.repo.filter_products.return_value = [product]

        result = self.service.get_all_products(filters)

        self.service.repo.filter_products.assert_called_once_with(filters)
        self.service.repo.get_all.assert_not_called()
        self.assertEqual(result, [{"id": "1", "name": "Phone", "brand": "Apple"}])

    def test_update_product_raises_when_product_not_found(self):
        self.service.repo.get_by_id.return_value = None

        with self.assertRaisesMessage(ValueError, "Product not found"):
            self.service.update_product("prod1", {"name": "Updated"})

    def test_update_product_raises_when_brand_is_empty(self):
        self.service.repo.get_by_id.return_value = MagicMock()

        with self.assertRaisesMessage(ValueError, "Brand cannot be empty"):
            self.service.update_product("prod1", {"brand": ""})

    def test_update_product_raises_when_price_not_positive(self):
        self.service.repo.get_by_id.return_value = MagicMock()

        with self.assertRaisesMessage(ValueError, "Price must be positive"):
            self.service.update_product("prod1", {"price": 0})

    def test_update_product_success(self):
        product = MagicMock()
        updated_product = MagicMock()
        updated_product.to_dict.return_value = {
            "id": "1",
            "name": "Updated Phone",
            "brand": "Apple",
            "price": 1500,
            "quantity": 10,
        }

        self.service.repo.get_by_id.return_value = product
        self.service.repo.update.return_value = updated_product

        data = {
            "name": "Updated Phone",
            "price": 1500,
            "brand": "Apple",
            "quantity": 10,
        }

        result = self.service.update_product("prod1", data)

        self.service.repo.get_by_id.assert_called_once_with("prod1")
        self.service.repo.update.assert_called_once_with(product, data)
        self.assertEqual(result, {
            "id": "1",
            "name": "Updated Phone",
            "brand": "Apple",
            "price": 1500,
            "quantity": 10,
        })

    def test_delete_product_raises_when_product_not_found(self):
        self.service.repo.get_by_id.return_value = None

        with self.assertRaisesMessage(ValueError, "Product not found"):
            self.service.delete_product("prod1")

    def test_delete_product_success(self):
        product = MagicMock()
        self.service.repo.get_by_id.return_value = product

        result = self.service.delete_product("prod1")

        self.service.repo.delete.assert_called_once_with(product)
        self.assertEqual(result, {"message": "Product deleted successfully"})


