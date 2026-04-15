from django.test import SimpleTestCase

from product_csr.models import Product, ProductCategory
from product_csr.repositories.category_repository import MongoCategoryRepository
from product_csr.repositories.product_repository import MongoProductRepository
from product_csr.services.category_service import CategoryService
from product_csr.services.product_service import ProductService


class ProductServiceTests(SimpleTestCase):
    def setUp(self):
        Product.objects.delete()
        ProductCategory.objects.delete()

        self.category_repo = MongoCategoryRepository()
        self.product_repo = MongoProductRepository(category_repo=self.category_repo)
        self.category_service = CategoryService(self.category_repo)
        self.service = ProductService(self.product_repo, self.category_repo)
        self.owner_id = "test-user-1"

    def tearDown(self):
        Product.objects.delete()
        ProductCategory.objects.delete()

    def create_category(self, title="Fashion", owner_id=None):
        return self.category_service.create_category(
            {
                "title": title,
                "description": f"{title} category",
            },
            owner_id=owner_id or self.owner_id,
        )

    def create_product(self, name="Hoodie", owner_id=None, category_id=None):
        data = {
            "name": name,
            "brand": "Zara",
            "price": 1499,
            "quantity": 5,
            "description": "Comfortable fashion product",
        }

        if category_id:
            data["categoryId"] = category_id

        return self.service.create_product(
            data,
            owner_id=owner_id or self.owner_id,
        )

    def test_create_product_success(self):
        result = self.create_product()

        self.assertEqual(result["name"], "Hoodie")
        self.assertEqual(result["brand"], "Zara")
        self.assertEqual(result["price"], 1499)
        self.assertEqual(result["quantity"], 5)
        self.assertEqual(result["description"], "Comfortable fashion product")
        self.assertEqual(result["owner_id"], self.owner_id)
        self.assertIsNotNone(Product.objects(name="Hoodie").first())

    def test_create_product_with_category_success(self):
        category = self.create_category()

        result = self.create_product(category_id=category["id"])

        self.assertEqual(result["category"], category["id"])

    def test_create_product_raises_when_name_missing(self):
        with self.assertRaisesMessage(ValueError, "name is required"):
            self.service.create_product(
                {
                    "brand": "Zara",
                    "price": 1499,
                    "quantity": 5,
                },
                owner_id=self.owner_id,
            )

    def test_create_product_raises_when_brand_missing(self):
        with self.assertRaisesMessage(ValueError, "brand is required"):
            self.service.create_product(
                {
                    "name": "Hoodie",
                    "price": 1499,
                    "quantity": 5,
                },
                owner_id=self.owner_id,
            )

    def test_create_product_raises_when_price_missing(self):
        with self.assertRaisesMessage(ValueError, "price is required"):
            self.service.create_product(
                {
                    "name": "Hoodie",
                    "brand": "Zara",
                    "quantity": 5,
                },
                owner_id=self.owner_id,
            )

    def test_create_product_raises_when_quantity_missing(self):
        with self.assertRaisesMessage(ValueError, "quantity is required"):
            self.service.create_product(
                {
                    "name": "Hoodie",
                    "brand": "Zara",
                    "price": 1499,
                },
                owner_id=self.owner_id,
            )

    def test_create_product_raises_when_price_is_zero(self):
        with self.assertRaisesMessage(ValueError, "Price must be positive"):
            self.service.create_product(
                {
                    "name": "Hoodie",
                    "brand": "Zara",
                    "price": 0,
                    "quantity": 5,
                },
                owner_id=self.owner_id,
            )

    def test_create_product_raises_when_quantity_is_negative(self):
        with self.assertRaisesMessage(ValueError, "Quantity cannot be negative"):
            self.service.create_product(
                {
                    "name": "Hoodie",
                    "brand": "Zara",
                    "price": 1499,
                    "quantity": -1,
                },
                owner_id=self.owner_id,
            )

    def test_create_product_raises_when_category_not_found(self):
        with self.assertRaisesMessage(ValueError, "Category not found"):
            self.service.create_product(
                {
                    "name": "Hoodie",
                    "brand": "Zara",
                    "price": 1499,
                    "quantity": 5,
                    "categoryId": "507f1f77bcf86cd799439011",
                },
                owner_id=self.owner_id,
            )

    def test_get_all_products_returns_only_owner_products(self):
        self.create_product(name="Hoodie", owner_id="user-1")
        self.create_product(name="Sneakers", owner_id="user-2")

        result = self.service.get_all_products(owner_id="user-1")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Hoodie")
        self.assertEqual(result[0]["owner_id"], "user-1")

    def test_get_all_products_with_brand_filter(self):
        self.create_product(name="Hoodie", owner_id=self.owner_id)

        self.service.create_product(
            {
                "name": "T-Shirt",
                "brand": "H&M",
                "price": 799,
                "quantity": 10,
            },
            owner_id=self.owner_id,
        )

        result = self.service.get_all_products(
            owner_id=self.owner_id,
            filters={"brand": "H&M"},
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "T-Shirt")
        self.assertEqual(result[0]["brand"], "H&M")

    def test_get_products_by_category_success(self):
        category = self.create_category()
        self.create_product(category_id=category["id"])

        result = self.service.get_products_by_category(
            category["id"],
            owner_id=self.owner_id,
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Hoodie")
        self.assertEqual(result[0]["category"], category["id"])

    def test_get_products_by_category_raises_when_category_not_found(self):
        with self.assertRaisesMessage(ValueError, "Category not found"):
            self.service.get_products_by_category(
                "507f1f77bcf86cd799439011",
                owner_id=self.owner_id,
            )

    def test_update_product_success(self):
        product = self.create_product()

        result = self.service.update_product(
            product["id"],
            {
                "name": "Updated Hoodie",
                "brand": "Zara",
                "price": 1799,
                "quantity": 8,
            },
            owner_id=self.owner_id,
        )

        self.assertEqual(result["name"], "Updated Hoodie")
        self.assertEqual(result["price"], 1799)
        self.assertEqual(result["quantity"], 8)

    def test_update_product_rejects_other_owner(self):
        product = self.create_product(owner_id="user-1")

        with self.assertRaisesMessage(
            ValueError,
            "You are not allowed to update this product",
        ):
            self.service.update_product(
                product["id"],
                {"name": "Updated Hoodie"},
                owner_id="user-2",
            )

    def test_update_product_raises_when_brand_is_empty(self):
        product = self.create_product()

        with self.assertRaisesMessage(ValueError, "Brand cannot be empty"):
            self.service.update_product(
                product["id"],
                {"brand": ""},
                owner_id=self.owner_id,
            )

    def test_update_product_raises_when_price_not_positive(self):
        product = self.create_product()

        with self.assertRaisesMessage(ValueError, "Price must be positive"):
            self.service.update_product(
                product["id"],
                {"price": 0},
                owner_id=self.owner_id,
            )

    def test_update_product_raises_when_quantity_is_negative(self):
        product = self.create_product()

        with self.assertRaisesMessage(ValueError, "Quantity cannot be negative"):
            self.service.update_product(
                product["id"],
                {"quantity": -1},
                owner_id=self.owner_id,
            )

    def test_update_product_can_change_category(self):
        product = self.create_product()
        category = self.create_category(title="Electronics")

        result = self.service.update_product(
            product["id"],
            {"categoryId": category["id"]},
            owner_id=self.owner_id,
        )

        self.assertEqual(result["category"], category["id"])

    def test_add_product_to_category_success(self):
        product = self.create_product()
        category = self.create_category()

        result = self.service.add_product_to_category(
            product["id"],
            category["id"],
            owner_id=self.owner_id,
        )

        updated_product = Product.objects(id=product["id"]).first()

        self.assertEqual(result, {"message": "Product added to category"})
        self.assertEqual(str(updated_product.category.id), category["id"])

    def test_add_product_to_category_rejects_other_owner_product(self):
        product = self.create_product(owner_id="user-1")
        category = self.create_category(owner_id="user-2")

        with self.assertRaisesMessage(
            ValueError,
            "You are not allowed to move this product",
        ):
            self.service.add_product_to_category(
                product["id"],
                category["id"],
                owner_id="user-2",
            )

    def test_remove_product_from_category_success(self):
        category = self.create_category()
        product = self.create_product(category_id=category["id"])

        result = self.service.remove_product_from_category(
            product["id"],
            owner_id=self.owner_id,
        )

        updated_product = Product.objects(id=product["id"]).first()

        self.assertEqual(result, {"message": "Product removed from category"})
        self.assertIsNone(updated_product.category)

    def test_remove_product_from_category_rejects_other_owner_product(self):
        product = self.create_product(owner_id="user-1")

        with self.assertRaisesMessage(
            ValueError,
            "You are not allowed to modify this product",
        ):
            self.service.remove_product_from_category(
                product["id"],
                owner_id="user-2",
            )

    def test_delete_product_success(self):
        product = self.create_product()

        result = self.service.delete_product(product["id"], owner_id=self.owner_id)

        self.assertEqual(result, {"message": "Product deleted successfully"})
        self.assertIsNone(Product.objects(id=product["id"]).first())

    def test_delete_product_rejects_other_owner(self):
        product = self.create_product(owner_id="user-1")

        with self.assertRaisesMessage(
            ValueError,
            "You are not allowed to delete this product",
        ):
            self.service.delete_product(product["id"], owner_id="user-2")
