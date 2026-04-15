from django.test import SimpleTestCase

from product_csr.models import ProductCategory
from product_csr.repositories.category_repository import MongoCategoryRepository
from product_csr.services.category_service import CategoryService


class CategoryServiceTests(SimpleTestCase):
    def setUp(self):
        ProductCategory.objects.delete()
        self.repo = MongoCategoryRepository()
        self.service = CategoryService(self.repo)
        self.owner_id = "test-user-1"

    def tearDown(self):
        ProductCategory.objects.delete()

    def test_create_category_success(self):
        result = self.service.create_category(
            {
                "title": "Fashion",
                "description": "Clothing products",
            },
            owner_id=self.owner_id,
        )

        self.assertEqual(result["title"], "Fashion")
        self.assertEqual(result["description"], "Clothing products")
        self.assertEqual(result["owner_id"], self.owner_id)
        self.assertIsNotNone(ProductCategory.objects(title="Fashion").first())

    def test_create_category_raises_when_title_missing(self):
        with self.assertRaisesMessage(ValueError, "Title is required"):
            self.service.create_category(
                {"description": "Missing title"},
                owner_id=self.owner_id,
            )

    def test_get_all_categories_returns_only_owner_categories(self):
        self.service.create_category(
            {"title": "Fashion", "description": "Clothing"},
            owner_id="user-1",
        )
        self.service.create_category(
            {"title": "Electronics", "description": "Devices"},
            owner_id="user-2",
        )

        result = self.service.get_all_categories(owner_id="user-1")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Fashion")
        self.assertEqual(result[0]["owner_id"], "user-1")

    def test_get_category_returns_category_for_correct_owner(self):
        created = self.service.create_category(
            {"title": "Fashion", "description": "Clothing"},
            owner_id=self.owner_id,
        )

        result = self.service.get_category(created["id"], owner_id=self.owner_id)

        self.assertEqual(result["id"], created["id"])
        self.assertEqual(result["title"], "Fashion")
        self.assertEqual(result["owner_id"], self.owner_id)

    def test_get_category_rejects_other_owner_category(self):
        created = self.service.create_category(
            {"title": "Fashion", "description": "Clothing"},
            owner_id="user-1",
        )

        with self.assertRaisesMessage(ValueError, "category not found"):
            self.service.get_category(created["id"], owner_id="user-2")

    def test_duplicate_category_title_fails_for_same_owner(self):
        self.service.create_category(
            {"title": "Fashion", "description": "Clothing"},
            owner_id="user-1",
        )

        with self.assertRaisesMessage(ValueError, "Category title already exists"):
            self.service.create_category(
                {"title": "Fashion", "description": "Duplicate"},
                owner_id="user-1",
            )

    def test_same_category_title_allowed_for_different_owners(self):
        first = self.service.create_category(
            {"title": "Fashion", "description": "User 1 category"},
            owner_id="user-1",
        )

        second = self.service.create_category(
            {"title": "Fashion", "description": "User 2 category"},
            owner_id="user-2",
        )

        self.assertEqual(first["title"], "Fashion")
        self.assertEqual(second["title"], "Fashion")
        self.assertNotEqual(first["owner_id"], second["owner_id"])

    def test_update_category_success(self):
        created = self.service.create_category(
            {"title": "Fashion", "description": "Clothing"},
            owner_id=self.owner_id,
        )

        updated = self.service.update_category(
            created["id"],
            {"title": "Updated Fashion", "description": "Updated clothing"},
            owner_id=self.owner_id,
        )

        self.assertEqual(updated["title"], "Updated Fashion")
        self.assertEqual(updated["description"], "Updated clothing")
        self.assertEqual(updated["owner_id"], self.owner_id)

    def test_update_category_raises_when_category_not_found(self):
        with self.assertRaisesMessage(ValueError, "category not found"):
            self.service.update_category(
                "507f1f77bcf86cd799439011",
                {"title": "Updated Fashion"},
                owner_id=self.owner_id,
            )

    def test_update_category_rejects_duplicate_title_for_same_owner(self):
        self.service.create_category(
            {"title": "Fashion", "description": "Clothing"},
            owner_id=self.owner_id,
        )

        second = self.service.create_category(
            {"title": "Electronics", "description": "Devices"},
            owner_id=self.owner_id,
        )

        with self.assertRaisesMessage(ValueError, "Category title already exists"):
            self.service.update_category(
                second["id"],
                {"title": "Fashion"},
                owner_id=self.owner_id,
            )

    def test_delete_category_success(self):
        created = self.service.create_category(
            {"title": "Fashion", "description": "Clothing"},
            owner_id=self.owner_id,
        )

        result = self.service.delete_category(created["id"], owner_id=self.owner_id)

        self.assertEqual(result, {"message": "category deleted successfully"})

        with self.assertRaisesMessage(ValueError, "category not found"):
            self.service.get_category(created["id"], owner_id=self.owner_id)

    def test_delete_category_rejects_other_owner_category(self):
        created = self.service.create_category(
            {"title": "Fashion", "description": "Clothing"},
            owner_id="user-1",
        )

        with self.assertRaisesMessage(ValueError, "category not found"):
            self.service.delete_category(created["id"], owner_id="user-2")

    def test_create_category_if_not_exists_returns_existing_category(self):
        created = self.service.create_category(
            {"title": "Fashion", "description": "Clothing"},
            owner_id=self.owner_id,
        )

        result = self.service.create_category_if_not_exists(
            "Fashion",
            owner_id=self.owner_id,
        )

        self.assertEqual(str(result.id), created["id"])
        self.assertEqual(result.title, "Fashion")

    def test_create_category_if_not_exists_creates_new_category(self):
        result = self.service.create_category_if_not_exists(
            "Books",
            owner_id=self.owner_id,
        )

        self.assertEqual(result.title, "Books")
        self.assertEqual(result.description, "")
        self.assertEqual(result.owner_id, self.owner_id)

