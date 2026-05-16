import csv
import io
from ..repositories.repositories import ProductRepository, ProductCategoryRepository
from ..validators.validators import validate_product_data, validate_category_data, validate_csv_row

"""
    Service layer — owns all business logic for the Product and ProductCategory domains.
"""


class ProductCategoryService:
    def __init__(
        self,
        category_repository: ProductCategoryRepository = None,
        product_repository: ProductRepository = None,
    ):
        self.category_repository = category_repository or ProductCategoryRepository()
        self.product_repository = product_repository or ProductRepository()

    def create_category(self, data: dict) -> dict:
        errors = validate_category_data(data, require_all_fields=True)
        if errors:
            return {"error": "Validation failed", "details": errors}
        category = self.category_repository.create(data)
        return {"category": category.to_dict()}

    def get_category(self, category_id: str) -> dict:
        category = self.category_repository.get_by_id(category_id)
        if not category:
            return {"error": "Category not found"}
        return {"category": category.to_dict()}

    def get_all_categories(self, page: int, page_size: int) -> dict:
        total = self.category_repository.count()
        total_pages = max(1, (total + page_size - 1) // page_size)

        if page > total_pages and total > 0:
            return {"error": f"Page {page} does not exist. Only {total_pages} page(s) available."}

        skip = (page - 1) * page_size
        categories = self.category_repository.get_paginated(skip=skip, limit=page_size)

        return {
            "page": page,
            "page_size": page_size,
            "total_categories": total,
            "total_pages": total_pages,
            "categories": [c.to_dict() for c in categories],
        }

    def full_update_category(self, category_id: str, data: dict) -> dict:
        category = self.category_repository.get_by_id(category_id)
        if not category:
            return {"error": "Category not found"}
        errors = validate_category_data(data, require_all_fields=True)
        if errors:
            return {"error": "Validation failed", "details": errors}
        updated = self.category_repository.update(category, data)
        return {"category": updated.to_dict()}

    def partial_update_category(self, category_id: str, data: dict) -> dict:
        category = self.category_repository.get_by_id(category_id)
        if not category:
            return {"error": "Category not found"}
        if not data:
            return {"error": "Provide at least one field to update."}
        errors = validate_category_data(data, require_all_fields=False)
        if errors:
            return {"error": "Validation failed", "details": errors}
        updated = self.category_repository.update(category, data)
        return {"category": updated.to_dict()}

    def delete_category(self, category_id: str) -> dict:
        category = self.category_repository.get_by_id(category_id)
        if not category:
            return {"error": "Category not found"}

        product_count = self.product_repository.count_by_category(category)
        if product_count > 0:
            return {
                "error": f"Cannot delete category '{category.title}' — "
                         f"{product_count} product(s) are still assigned to it. "
                         f"Reassign or remove those products first."
            }

        self.category_repository.delete(category)
        return {}

    def get_products_in_category(self, category_id: str) -> dict:
        category = self.category_repository.get_by_id(category_id)
        if not category:
            return {"error": "Category not found"}
        products = self.product_repository.get_by_category(category)
        return {
            "category": category.to_dict(),
            "total_products": len(products),
            "products": [p.to_dict() for p in products],
        }


class ProductService:
    def __init__(
        self,
        repository: ProductRepository = None,
        category_repository: ProductCategoryRepository = None,
    ):
        self.repository = repository or ProductRepository()
        self.category_repository = category_repository or ProductCategoryRepository()

    def _resolve_category(self, category_id: str | None):
        """
        Resolves a category_id string to a ProductCategory object.
        Returns:
          - ProductCategory if found
          - None if category_id is None
          - dict with "error" key if not found
        """
        if not category_id:
            return None
        category = self.category_repository.get_by_id(category_id)
        if not category:
            return {"error": f"Category with id '{category_id}' not found"}
        return category

    def _build_filters(self, params: dict) -> dict | str:
        """
        Translates raw query parameters into MongoEngine filter kwargs.

        Supported filters:
          category_ids  — comma-separated ObjectId strings e.g. ?category_ids=id1,id2
          min_price     — inclusive minimum price e.g. ?min_price=100
          max_price     — inclusive maximum price e.g. ?max_price=500
          min_quantity  — inclusive minimum quantity e.g. ?min_quantity=10
          max_quantity  — inclusive maximum quantity e.g. ?max_quantity=100
          brand         — exact brand match e.g. ?brand=Apple
          search        — case-insensitive name contains e.g. ?search=iphone

        Returns a MongoEngine filter dict or an error string if validation fails.
        Filter building lives here in the Service because resolving category IDs
        and validating ranges is business logic, not HTTP parsing.
        """
        filters = {}

        # --- category_ids ---
        category_ids_raw = params.get("category_ids", "").strip()
        if category_ids_raw:
            category_id_list = [c.strip() for c in category_ids_raw.split(",") if c.strip()]
            resolved = []
            for cat_id in category_id_list:
                category = self.category_repository.get_by_id(cat_id)
                if not category:
                    return f"Category with id '{cat_id}' not found"
                resolved.append(category)
            if resolved:
                filters["category__in"] = resolved

        # --- price range ---
        if params.get("min_price"):
            try:
                min_price = float(params["min_price"])
                if min_price < 0:
                    return "min_price must be a non-negative number"
                filters["price__gte"] = min_price
            except ValueError:
                return "min_price must be a valid number"

        if params.get("max_price"):
            try:
                max_price = float(params["max_price"])
                if max_price < 0:
                    return "max_price must be a non-negative number"
                filters["price__lte"] = max_price
            except ValueError:
                return "max_price must be a valid number"

        if "price__gte" in filters and "price__lte" in filters:
            if filters["price__gte"] > filters["price__lte"]:
                return "min_price cannot be greater than max_price"

        # --- quantity range ---
        if params.get("min_quantity"):
            try:
                min_qty = int(params["min_quantity"])
                if min_qty < 0:
                    return "min_quantity must be a non-negative integer"
                filters["quantity__gte"] = min_qty
            except ValueError:
                return "min_quantity must be a valid integer"

        if params.get("max_quantity"):
            try:
                max_qty = int(params["max_quantity"])
                if max_qty < 0:
                    return "max_quantity must be a non-negative integer"
                filters["quantity__lte"] = max_qty
            except ValueError:
                return "max_quantity must be a valid integer"

        if "quantity__gte" in filters and "quantity__lte" in filters:
            if filters["quantity__gte"] > filters["quantity__lte"]:
                return "min_quantity cannot be greater than max_quantity"

        # --- brand ---
        brand = params.get("brand", "").strip()
        if brand:
            filters["brand"] = brand

        # --- name search ---
        search = params.get("search", "").strip()
        if search:
            filters["name__icontains"] = search

        return filters

    def create_product(self, data: dict) -> dict:
        errors = validate_product_data(data, require_all_fields=True)
        if errors:
            return {"error": "Validation failed", "details": errors}

        category_id = data.get("category_id")
        category = self._resolve_category(category_id)
        if isinstance(category, dict):
            return category

        product = self.repository.create(data, category=category)
        return {"product": product.to_dict()}

    def get_product(self, product_id: str) -> dict:
        product = self.repository.get_by_id(product_id)
        if not product:
            return {"error": "Product not found"}
        return {"product": product.to_dict()}

    def get_all_products(self, page: int, page_size: int, filter_params: dict = None) -> dict:
        """
        Fetches a paginated, optionally filtered page of products.

        filter_params is a dict of raw query string values from the request.
        The Service translates these into MongoEngine filter kwargs via
        _build_filters() and passes them to the Repository for DB-side filtering.
        """
        filters = {}
        if filter_params:
            filters = self._build_filters(filter_params)
            if isinstance(filters, str):
                # _build_filters returned an error message
                return {"error": filters}

        total_products = self.repository.count(filters=filters or None)
        total_pages = max(1, (total_products + page_size - 1) // page_size)

        if page > total_pages and total_products > 0:
            return {"error": f"Page {page} does not exist. Only {total_pages} page(s) available."}

        skip = (page - 1) * page_size
        products = self.repository.get_paginated(skip=skip, limit=page_size, filters=filters or None)

        return {
            "page": page,
            "page_size": page_size,
            "total_products": total_products,
            "total_pages": total_pages,
            "filters_applied": {
                k: [str(c.id) for c in v] if k == "category__in" else v
                for k, v in filters.items()
            } if filter_params and filters else {},
            "products": [p.to_dict() for p in products],
        }

    def full_update_product(self, product_id: str, data: dict) -> dict:
        product = self.repository.get_by_id(product_id)
        if not product:
            return {"error": "Product not found"}

        errors = validate_product_data(data, require_all_fields=True)
        if errors:
            return {"error": "Validation failed", "details": errors}

        category_id = data.get("category_id")
        category = self._resolve_category(category_id)
        if isinstance(category, dict):
            return category

        updated = self.repository.update(product, data, category=category)
        return {"product": updated.to_dict()}

    def partial_update_product(self, product_id: str, data: dict) -> dict:
        product = self.repository.get_by_id(product_id)
        if not product:
            return {"error": "Product not found"}

        if not data:
            return {"error": "Provide at least one field to update."}

        errors = validate_product_data(data, require_all_fields=False)
        if errors:
            return {"error": "Validation failed", "details": errors}

        if "category_id" in data:
            category = self._resolve_category(data["category_id"])
            if isinstance(category, dict):
                return category
        else:
            category = False  # sentinel: do not touch category

        updated = self.repository.update(product, data, category=category)
        return {"product": updated.to_dict()}

    def delete_product(self, product_id: str) -> dict:
        product = self.repository.get_by_id(product_id)
        if not product:
            return {"error": "Product not found"}
        self.repository.delete(product)
        return {}

    def add_product_to_category(self, product_id: str, category_id: str) -> dict:
        product = self.repository.get_by_id(product_id)
        if not product:
            return {"error": "Product not found"}
        category = self.category_repository.get_by_id(category_id)
        if not category:
            return {"error": "Category not found"}
        updated = self.repository.set_category(product, category)
        return {"product": updated.to_dict()}

    def remove_product_from_category(self, product_id: str) -> dict:
        product = self.repository.get_by_id(product_id)
        if not product:
            return {"error": "Product not found"}
        if not product.category:
            return {"error": "Product is not assigned to any category"}
        updated = self.repository.remove_category(product)
        return {"product": updated.to_dict()}

    def bulk_create_from_csv(self, csv_content: str) -> dict:
        try:
            reader = csv.DictReader(io.StringIO(csv_content))
        except Exception:
            return {"error": "Failed to parse CSV content"}

        required_columns = {"name", "description", "price", "brand", "quantity"}
        rows = []
        all_errors = []

        for row_number, row in enumerate(reader, start=1):
            if row_number == 1 and not required_columns.issubset(set(row.keys())):
                missing = required_columns - set(row.keys())
                return {
                    "error": "CSV is missing required columns",
                    "missing_columns": list(missing),
                    "required_columns": list(required_columns),
                }

            parsed_row = dict(row)
            try:
                parsed_row["price"] = float(parsed_row["price"])
            except (ValueError, TypeError):
                pass
            try:
                parsed_row["quantity"] = int(parsed_row["quantity"])
            except (ValueError, TypeError):
                pass

            category_id = parsed_row.get("category_id", "").strip() or None
            parsed_row["category_id"] = category_id

            validation = validate_csv_row(parsed_row, row_number)
            if validation["errors"]:
                all_errors.append(validation)
            else:
                category = None
                if category_id:
                    category = self.category_repository.get_by_id(category_id)
                    if not category:
                        all_errors.append({
                            "row": row_number,
                            "errors": {"category_id": f"Category '{category_id}' not found"},
                        })
                        continue
                parsed_row["category"] = category
                rows.append(parsed_row)

        if all_errors:
            return {
                "error": "CSV validation failed — no products were created",
                "failed_rows": all_errors,
                "total_failed": len(all_errors),
            }

        if not rows:
            return {"error": "CSV file is empty or has no valid rows"}

        created = self.repository.bulk_create(rows)
        return {
            "message": f"Successfully created {len(created)} product(s)",
            "total_created": len(created),
            "products": [p.to_dict() for p in created],
        }