from django.test import SimpleTestCase

from product_csr.models import Product, ProductCategory
from product_csr.repositories.category_repository import MongoCategoryRepository
from product_csr.repositories.product_repository import MongoProductRepository
from product_csr.services.category_service import CategoryService
from product_csr.services.product_service import ProductService


class OwnershipServiceTests(SimpleTestCase):
    def setUp(self):
        Product.objects.delete()
        ProductCategory.objects.delete()

        self.category_repo = MongoCategoryRepository()
        self.product_repo = MongoProductRepository(category_repo=self.category_repo)
        self.category_service = CategoryService(self.category_repo)
        self.product_service = ProductService(self.product_repo, self.category_repo)

    def tearDown(self):
        Product.objects.delete()
        ProductCategory.objects.delete()

    def test_product_create_assigns_owner_id(self):
        result = self.product_service.create_product(
            {
                "name": "Hoodie",
                "brand": "Zara",
                "price": 49.99,
                "quantity": 8,
            },
            owner_id="1",
        )

        saved_product = Product.objects(id=result["id"]).first()

        self.assertEqual(result["owner_id"], "1")
        self.assertIsNotNone(saved_product)
        self.assertEqual(saved_product.owner_id, "1")

    def test_product_update_rejects_other_owner(self):
        product = self.product_service.create_product(
            {
                "name": "Hoodie",
                "brand": "Zara",
                "price": 49.99,
                "quantity": 8,
            },
            owner_id="1",
        )

        with self.assertRaisesMessage(
            ValueError,
            "You are not allowed to update this product",
        ):
            self.product_service.update_product(
                product["id"],
                {"name": "Updated Hoodie"},
                owner_id="2",
            )

    def test_product_delete_rejects_other_owner(self):
        product = self.product_service.create_product(
            {
                "name": "Hoodie",
                "brand": "Zara",
                "price": 49.99,
                "quantity": 8,
            },
            owner_id="1",
        )

        with self.assertRaisesMessage(
            ValueError,
            "You are not allowed to delete this product",
        ):
            self.product_service.delete_product(
                product["id"],
                owner_id="2",
            )

    def test_category_create_assigns_owner_id(self):
        result = self.category_service.create_category(
            {
                "title": "Fashion",
                "description": "Clothing",
            },
            owner_id="1",
        )

        saved_category = ProductCategory.objects(id=result["id"]).first()

        self.assertEqual(result["owner_id"], "1")
        self.assertIsNotNone(saved_category)
        self.assertEqual(saved_category.owner_id, "1")

    def test_category_lookup_uses_owner_id(self):
        category = self.category_service.create_category(
            {
                "title": "Fashion",
                "description": "Clothing",
            },
            owner_id="1",
        )

        result = self.category_service.get_category(
            category["id"],
            owner_id="1",
        )

        self.assertEqual(result["owner_id"], "1")
        self.assertEqual(result["title"], "Fashion")

    def test_category_lookup_rejects_other_owner(self):
        category = self.category_service.create_category(
            {
                "title": "Fashion",
                "description": "Clothing",
            },
            owner_id="1",
        )

        with self.assertRaisesMessage(ValueError, "category not found"):
            self.category_service.get_category(
                category["id"],
                owner_id="2",
            )

