"""
Unit tests for ProductService and ProductCategoryService.

Week 5 requirement: unit tests mock the repository layer so no real
MongoDB connection is needed. Every test runs in pure Python — fast,
isolated, and runnable without Docker.

Run with:
    python manage.py test Product.test_services

Structure:
  - FakeCategory / FakeProduct   — in-memory stand-ins for MongoEngine documents
  - FakeCategoryRepository       — fake repository for ProductCategory
  - FakeProductRepository        — fake repository for Product
  - TestProductCategoryService   — tests for all category service methods
  - TestProductService           — tests for all product service methods
"""

from unittest import TestCase
from unittest.mock import MagicMock
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Fake domain objects
# These mimic the interface of MongoEngine Documents without hitting MongoDB.
# ---------------------------------------------------------------------------

class FakeCategory:
    """Mimics a ProductCategory MongoEngine Document."""

    def __init__(self, title, description, id=None):
        self.id = id or "cat_" + title.lower().replace(" ", "_")
        self.title = title
        self.description = description
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class FakeProduct:
    """Mimics a Product MongoEngine Document."""

    def __init__(self, name, description, price, brand, quantity,
                 category=None, id=None):
        self.id = id or "prod_" + name.lower().replace(" ", "_")
        self.name = name
        self.description = description
        self.price = price
        self.brand = brand
        self.quantity = quantity
        self.category = category
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self):
        category_data = None
        if self.category:
            category_data = {"id": str(self.category.id), "title": self.category.title}
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "category": category_data,
            "price": self.price,
            "brand": self.brand,
            "quantity": self.quantity,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


# ---------------------------------------------------------------------------
# Fake repositories
# Store data in plain Python dicts. Same interface as the real repositories.
# ---------------------------------------------------------------------------

class FakeCategoryRepository:
    def __init__(self):
        self._store = {}

    def create(self, data):
        cat = FakeCategory(title=data["title"], description=data["description"])
        self._store[cat.id] = cat
        return cat

    def get_by_id(self, category_id):
        return self._store.get(category_id)

    def get_all(self):
        return list(self._store.values())

    def count(self, filters=None):
        # filters accepted but not applied — unit tests don't need DB-side filtering
        return len(self._store)

    def get_paginated(self, skip, limit, filters=None):
        # filters accepted but not applied — unit tests don't need DB-side filtering
        items = list(self._store.values())
        return items[skip:skip + limit]

    def update(self, category, data):
        if "title" in data:
            category.title = data["title"]
        if "description" in data:
            category.description = data["description"]
        category.updated_at = datetime.now(timezone.utc)
        return category

    def delete(self, category):
        self._store.pop(category.id, None)


class FakeProductRepository:
    def __init__(self):
        self._store = {}

    def create(self, data, category=None):
        product = FakeProduct(
            name=data["name"],
            description=data["description"],
            price=float(data["price"]),
            brand=data["brand"],
            quantity=int(data["quantity"]),
            category=category,
        )
        self._store[product.id] = product
        return product

    def get_by_id(self, product_id):
        return self._store.get(product_id)

    def count(self, filters=None):
        # filters accepted but not applied — unit tests don't need DB-side filtering
        return len(self._store)

    def get_paginated(self, skip, limit, filters=None):
        # filters accepted but not applied — unit tests don't need DB-side filtering
        items = list(self._store.values())
        return items[skip:skip + limit]

    def get_by_category(self, category):
        return [p for p in self._store.values() if p.category and p.category.id == category.id]

    def count_by_category(self, category):
        return len(self.get_by_category(category))

    def update(self, product, data, category=False):
        for field in ["name", "description", "brand"]:
            if field in data:
                setattr(product, field, data[field])
        if "price" in data:
            product.price = float(data["price"])
        if "quantity" in data:
            product.quantity = int(data["quantity"])
        if category is not False:
            product.category = category
        product.updated_at = datetime.now(timezone.utc)
        return product

    def set_category(self, product, category):
        product.category = category
        product.updated_at = datetime.now(timezone.utc)
        return product

    def remove_category(self, product):
        product.category = None
        product.updated_at = datetime.now(timezone.utc)
        return product

    def bulk_create(self, products_data):
        created = []
        for p in products_data:
            product = FakeProduct(
                name=p["name"],
                description=p["description"],
                price=float(p["price"]),
                brand=p["brand"],
                quantity=int(p["quantity"]),
                category=p.get("category"),
            )
            self._store[product.id] = product
            created.append(product)
        return created

    def delete(self, product):
        self._store.pop(product.id, None)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VALID_PRODUCT = {
    "name": "iPhone 15",
    "description": "Latest Apple smartphone",
    "price": 999.99,
    "brand": "Apple",
    "quantity": 50,
}

VALID_CATEGORY = {
    "title": "Electronics",
    "description": "Electronic devices",
}


def make_services():
    """Returns fresh service instances backed by fake repositories."""
    cat_repo = FakeCategoryRepository()
    prod_repo = FakeProductRepository()

    from Product.services.services import ProductCategoryService, ProductService
    cat_service = ProductCategoryService(
        category_repository=cat_repo,
        product_repository=prod_repo,
    )
    prod_service = ProductService(
        repository=prod_repo,
        category_repository=cat_repo,
    )
    return cat_service, prod_service, cat_repo, prod_repo


# ---------------------------------------------------------------------------
# ProductCategoryService tests
# ---------------------------------------------------------------------------

class TestProductCategoryService(TestCase):

    def setUp(self):
        self.cat_service, self.prod_service, self.cat_repo, self.prod_repo = make_services()

    # --- create_category ---

    def test_create_category_success(self):
        result = self.cat_service.create_category(VALID_CATEGORY)
        self.assertIn("category", result)
        self.assertEqual(result["category"]["title"], "Electronics")

    def test_create_category_missing_title(self):
        result = self.cat_service.create_category({"description": "desc"})
        self.assertIn("error", result)
        self.assertIn("title", result["details"])

    def test_create_category_missing_description(self):
        result = self.cat_service.create_category({"title": "Electronics"})
        self.assertIn("error", result)
        self.assertIn("description", result["details"])

    def test_create_category_empty_title(self):
        result = self.cat_service.create_category({"title": "", "description": "desc"})
        self.assertIn("error", result)
        self.assertIn("title", result["details"])

    def test_create_category_title_too_long(self):
        result = self.cat_service.create_category({
            "title": "x" * 256,
            "description": "desc"
        })
        self.assertIn("error", result)
        self.assertIn("title", result["details"])

    # --- get_category ---

    def test_get_category_success(self):
        created = self.cat_service.create_category(VALID_CATEGORY)
        cat_id = created["category"]["id"]
        result = self.cat_service.get_category(cat_id)
        self.assertIn("category", result)
        self.assertEqual(result["category"]["title"], "Electronics")

    def test_get_category_not_found(self):
        result = self.cat_service.get_category("nonexistent_id")
        self.assertEqual(result, {"error": "Category not found"})

    # --- get_all_categories ---

    def test_get_all_categories_empty(self):
        result = self.cat_service.get_all_categories(page=1, page_size=10)
        self.assertEqual(result["total_categories"], 0)
        self.assertEqual(result["categories"], [])

    def test_get_all_categories_pagination(self):
        for i in range(5):
            self.cat_service.create_category({"title": f"Cat {i}", "description": "desc"})
        result = self.cat_service.get_all_categories(page=1, page_size=3)
        self.assertEqual(len(result["categories"]), 3)
        self.assertEqual(result["total_categories"], 5)
        self.assertEqual(result["total_pages"], 2)

    def test_get_all_categories_page_out_of_range(self):
        self.cat_service.create_category(VALID_CATEGORY)
        result = self.cat_service.get_all_categories(page=99, page_size=10)
        self.assertIn("error", result)

    # --- full_update_category ---

    def test_full_update_category_success(self):
        created = self.cat_service.create_category(VALID_CATEGORY)
        cat_id = created["category"]["id"]
        result = self.cat_service.full_update_category(cat_id, {
            "title": "Updated Electronics",
            "description": "Updated desc",
        })
        self.assertEqual(result["category"]["title"], "Updated Electronics")

    def test_full_update_category_not_found(self):
        result = self.cat_service.full_update_category("bad_id", VALID_CATEGORY)
        self.assertEqual(result, {"error": "Category not found"})

    def test_full_update_category_missing_fields(self):
        created = self.cat_service.create_category(VALID_CATEGORY)
        cat_id = created["category"]["id"]
        result = self.cat_service.full_update_category(cat_id, {"title": "Only title"})
        self.assertIn("error", result)
        self.assertIn("description", result["details"])

    # --- partial_update_category ---

    def test_partial_update_category_title_only(self):
        created = self.cat_service.create_category(VALID_CATEGORY)
        cat_id = created["category"]["id"]
        result = self.cat_service.partial_update_category(cat_id, {"title": "New Title"})
        self.assertEqual(result["category"]["title"], "New Title")

    def test_partial_update_category_empty_body(self):
        created = self.cat_service.create_category(VALID_CATEGORY)
        cat_id = created["category"]["id"]
        result = self.cat_service.partial_update_category(cat_id, {})
        self.assertIn("error", result)

    def test_partial_update_category_not_found(self):
        result = self.cat_service.partial_update_category("bad_id", {"title": "x"})
        self.assertEqual(result, {"error": "Category not found"})

    # --- delete_category ---

    def test_delete_category_success(self):
        created = self.cat_service.create_category(VALID_CATEGORY)
        cat_id = created["category"]["id"]
        result = self.cat_service.delete_category(cat_id)
        self.assertEqual(result, {})
        self.assertIsNone(self.cat_repo.get_by_id(cat_id))

    def test_delete_category_not_found(self):
        result = self.cat_service.delete_category("bad_id")
        self.assertEqual(result, {"error": "Category not found"})

    def test_delete_category_blocked_when_products_exist(self):
        # Create a category and assign a product to it
        cat = self.cat_service.create_category(VALID_CATEGORY)
        cat_id = cat["category"]["id"]
        self.prod_service.create_product({**VALID_PRODUCT, "category_id": cat_id})

        result = self.cat_service.delete_category(cat_id)
        self.assertIn("error", result)
        self.assertIn("1 product(s)", result["error"])

    # --- get_products_in_category ---

    def test_get_products_in_category_success(self):
        cat = self.cat_service.create_category(VALID_CATEGORY)
        cat_id = cat["category"]["id"]
        self.prod_service.create_product({**VALID_PRODUCT, "category_id": cat_id})
        self.prod_service.create_product({**VALID_PRODUCT, "name": "iPad", "category_id": cat_id})

        result = self.cat_service.get_products_in_category(cat_id)
        self.assertEqual(result["total_products"], 2)
        self.assertEqual(len(result["products"]), 2)

    def test_get_products_in_category_not_found(self):
        result = self.cat_service.get_products_in_category("bad_id")
        self.assertEqual(result, {"error": "Category not found"})

    def test_get_products_in_category_empty(self):
        cat = self.cat_service.create_category(VALID_CATEGORY)
        cat_id = cat["category"]["id"]
        result = self.cat_service.get_products_in_category(cat_id)
        self.assertEqual(result["total_products"], 0)
        self.assertEqual(result["products"], [])


# ---------------------------------------------------------------------------
# ProductService tests
# ---------------------------------------------------------------------------

class TestProductService(TestCase):

    def setUp(self):
        self.cat_service, self.prod_service, self.cat_repo, self.prod_repo = make_services()
        # Create a default category for tests that need one
        cat = self.cat_service.create_category(VALID_CATEGORY)
        self.cat_id = cat["category"]["id"]

    # --- create_product ---

    def test_create_product_success_no_category(self):
        result = self.prod_service.create_product(VALID_PRODUCT)
        self.assertIn("product", result)
        self.assertEqual(result["product"]["name"], "iPhone 15")
        self.assertIsNone(result["product"]["category"])

    def test_create_product_success_with_category(self):
        result = self.prod_service.create_product({**VALID_PRODUCT, "category_id": self.cat_id})
        self.assertIn("product", result)
        self.assertEqual(result["product"]["category"]["title"], "Electronics")

    def test_create_product_invalid_category_id(self):
        result = self.prod_service.create_product({**VALID_PRODUCT, "category_id": "bad_id"})
        self.assertIn("error", result)
        self.assertIn("not found", result["error"])

    def test_create_product_missing_name(self):
        data = {**VALID_PRODUCT}
        del data["name"]
        result = self.prod_service.create_product(data)
        self.assertIn("error", result)
        self.assertIn("name", result["details"])

    def test_create_product_negative_price(self):
        result = self.prod_service.create_product({**VALID_PRODUCT, "price": -10})
        self.assertIn("error", result)
        self.assertIn("price", result["details"])

    def test_create_product_zero_price(self):
        result = self.prod_service.create_product({**VALID_PRODUCT, "price": 0})
        self.assertIn("error", result)
        self.assertIn("price", result["details"])

    def test_create_product_boolean_price_rejected(self):
        result = self.prod_service.create_product({**VALID_PRODUCT, "price": True})
        self.assertIn("error", result)
        self.assertIn("price", result["details"])

    def test_create_product_negative_quantity(self):
        result = self.prod_service.create_product({**VALID_PRODUCT, "quantity": -1})
        self.assertIn("error", result)
        self.assertIn("quantity", result["details"])

    def test_create_product_float_quantity_rejected(self):
        result = self.prod_service.create_product({**VALID_PRODUCT, "quantity": 5.5})
        self.assertIn("error", result)
        self.assertIn("quantity", result["details"])

    def test_create_product_boolean_quantity_rejected(self):
        result = self.prod_service.create_product({**VALID_PRODUCT, "quantity": True})
        self.assertIn("error", result)
        self.assertIn("quantity", result["details"])

    def test_create_product_name_too_long(self):
        result = self.prod_service.create_product({**VALID_PRODUCT, "name": "x" * 256})
        self.assertIn("error", result)
        self.assertIn("name", result["details"])

    # --- get_product ---

    def test_get_product_success(self):
        created = self.prod_service.create_product(VALID_PRODUCT)
        prod_id = created["product"]["id"]
        result = self.prod_service.get_product(prod_id)
        self.assertIn("product", result)
        self.assertEqual(result["product"]["name"], "iPhone 15")

    def test_get_product_not_found(self):
        result = self.prod_service.get_product("nonexistent")
        self.assertEqual(result, {"error": "Product not found"})

    # --- get_all_products ---

    def test_get_all_products_empty(self):
        result = self.prod_service.get_all_products(page=1, page_size=10)
        self.assertEqual(result["total_products"], 0)
        self.assertEqual(result["products"], [])

    def test_get_all_products_pagination(self):
        for i in range(7):
            self.prod_service.create_product({**VALID_PRODUCT, "name": f"Product {i}"})
        result = self.prod_service.get_all_products(page=2, page_size=3)
        self.assertEqual(len(result["products"]), 3)
        self.assertEqual(result["total_products"], 7)
        self.assertEqual(result["total_pages"], 3)

    def test_get_all_products_page_out_of_range(self):
        self.prod_service.create_product(VALID_PRODUCT)
        result = self.prod_service.get_all_products(page=99, page_size=10)
        self.assertIn("error", result)

    # --- full_update_product ---

    def test_full_update_product_success(self):
        created = self.prod_service.create_product(VALID_PRODUCT)
        prod_id = created["product"]["id"]
        result = self.prod_service.full_update_product(prod_id, {
            "name": "iPhone 16",
            "description": "Newer model",
            "price": 1099.99,
            "brand": "Apple",
            "quantity": 30,
        })
        self.assertEqual(result["product"]["name"], "iPhone 16")
        self.assertEqual(result["product"]["price"], 1099.99)

    def test_full_update_product_not_found(self):
        result = self.prod_service.full_update_product("bad_id", VALID_PRODUCT)
        self.assertEqual(result, {"error": "Product not found"})

    def test_full_update_product_missing_required_field(self):
        created = self.prod_service.create_product(VALID_PRODUCT)
        prod_id = created["product"]["id"]
        data = {**VALID_PRODUCT}
        del data["brand"]
        result = self.prod_service.full_update_product(prod_id, data)
        self.assertIn("error", result)
        self.assertIn("brand", result["details"])

    def test_full_update_product_with_category(self):
        created = self.prod_service.create_product(VALID_PRODUCT)
        prod_id = created["product"]["id"]
        result = self.prod_service.full_update_product(prod_id, {
            **VALID_PRODUCT,
            "category_id": self.cat_id,
        })
        self.assertEqual(result["product"]["category"]["title"], "Electronics")

    # --- partial_update_product ---

    def test_partial_update_product_price_only(self):
        created = self.prod_service.create_product(VALID_PRODUCT)
        prod_id = created["product"]["id"]
        result = self.prod_service.partial_update_product(prod_id, {"price": 799.99})
        self.assertEqual(result["product"]["price"], 799.99)
        # Other fields unchanged
        self.assertEqual(result["product"]["name"], "iPhone 15")

    def test_partial_update_product_category_unchanged_when_not_sent(self):
        # Create product with a category
        created = self.prod_service.create_product({**VALID_PRODUCT, "category_id": self.cat_id})
        prod_id = created["product"]["id"]
        # Patch only the price — category_id not in body
        result = self.prod_service.partial_update_product(prod_id, {"price": 500.0})
        # Category should still be set
        self.assertEqual(result["product"]["category"]["title"], "Electronics")

    def test_partial_update_product_remove_category_via_null(self):
        created = self.prod_service.create_product({**VALID_PRODUCT, "category_id": self.cat_id})
        prod_id = created["product"]["id"]
        result = self.prod_service.partial_update_product(prod_id, {"category_id": None})
        self.assertIsNone(result["product"]["category"])

    def test_partial_update_product_empty_body(self):
        created = self.prod_service.create_product(VALID_PRODUCT)
        prod_id = created["product"]["id"]
        result = self.prod_service.partial_update_product(prod_id, {})
        self.assertIn("error", result)

    def test_partial_update_product_not_found(self):
        result = self.prod_service.partial_update_product("bad_id", {"price": 10})
        self.assertEqual(result, {"error": "Product not found"})

    # --- delete_product ---

    def test_delete_product_success(self):
        created = self.prod_service.create_product(VALID_PRODUCT)
        prod_id = created["product"]["id"]
        result = self.prod_service.delete_product(prod_id)
        self.assertEqual(result, {})
        self.assertIsNone(self.prod_repo.get_by_id(prod_id))

    def test_delete_product_not_found(self):
        result = self.prod_service.delete_product("bad_id")
        self.assertEqual(result, {"error": "Product not found"})

    # --- add_product_to_category ---

    def test_add_product_to_category_success(self):
        created = self.prod_service.create_product(VALID_PRODUCT)
        prod_id = created["product"]["id"]
        result = self.prod_service.add_product_to_category(prod_id, self.cat_id)
        self.assertEqual(result["product"]["category"]["title"], "Electronics")

    def test_add_product_to_category_product_not_found(self):
        result = self.prod_service.add_product_to_category("bad_id", self.cat_id)
        self.assertEqual(result, {"error": "Product not found"})

    def test_add_product_to_category_category_not_found(self):
        created = self.prod_service.create_product(VALID_PRODUCT)
        prod_id = created["product"]["id"]
        result = self.prod_service.add_product_to_category(prod_id, "bad_cat_id")
        self.assertEqual(result, {"error": "Category not found"})

    # --- remove_product_from_category ---

    def test_remove_product_from_category_success(self):
        created = self.prod_service.create_product({**VALID_PRODUCT, "category_id": self.cat_id})
        prod_id = created["product"]["id"]
        result = self.prod_service.remove_product_from_category(prod_id)
        self.assertIsNone(result["product"]["category"])

    def test_remove_product_from_category_not_in_category(self):
        created = self.prod_service.create_product(VALID_PRODUCT)
        prod_id = created["product"]["id"]
        result = self.prod_service.remove_product_from_category(prod_id)
        self.assertIn("error", result)
        self.assertIn("not assigned", result["error"])

    def test_remove_product_from_category_product_not_found(self):
        result = self.prod_service.remove_product_from_category("bad_id")
        self.assertEqual(result, {"error": "Product not found"})

    # --- bulk_create_from_csv ---

    def test_bulk_create_csv_success(self):
        csv_content = (
            "name,description,price,brand,quantity\n"
            "MacBook Pro,Apple laptop,1999.99,Apple,30\n"
            "iPad Air,Apple tablet,799.99,Apple,75\n"
        )
        result = self.prod_service.bulk_create_from_csv(csv_content)
        self.assertEqual(result["total_created"], 2)
        self.assertIn("products", result)

    def test_bulk_create_csv_with_category(self):
        csv_content = (
            f"name,description,price,brand,quantity,category_id\n"
            f"MacBook Pro,Apple laptop,1999.99,Apple,30,{self.cat_id}\n"
        )
        result = self.prod_service.bulk_create_from_csv(csv_content)
        self.assertEqual(result["total_created"], 1)
        self.assertEqual(result["products"][0]["category"]["title"], "Electronics")

    def test_bulk_create_csv_invalid_row_rejects_all(self):
        csv_content = (
            "name,description,price,brand,quantity\n"
            "MacBook Pro,Apple laptop,1999.99,Apple,30\n"
            "BadProduct,,not-a-price,,-5\n"
        )
        result = self.prod_service.bulk_create_from_csv(csv_content)
        self.assertIn("error", result)
        self.assertEqual(result["total_failed"], 1)
        self.assertEqual(result["failed_rows"][0]["row"], 2)
        # Nothing was inserted
        self.assertEqual(self.prod_repo.count(), 0)

    def test_bulk_create_csv_missing_required_column(self):
        csv_content = (
            "name,price,brand,quantity\n"  # missing 'description'
            "MacBook Pro,1999.99,Apple,30\n"
        )
        result = self.prod_service.bulk_create_from_csv(csv_content)
        self.assertIn("error", result)
        self.assertIn("missing_columns", result)

    def test_bulk_create_csv_invalid_category_id(self):
        csv_content = (
            "name,description,price,brand,quantity,category_id\n"
            "MacBook Pro,Apple laptop,1999.99,Apple,30,nonexistent_cat\n"
        )
        result = self.prod_service.bulk_create_from_csv(csv_content)
        self.assertIn("error", result)
        self.assertEqual(self.prod_repo.count(), 0)

    def test_bulk_create_csv_empty_file(self):
        result = self.prod_service.bulk_create_from_csv("name,description,price,brand,quantity\n")
        self.assertIn("error", result)