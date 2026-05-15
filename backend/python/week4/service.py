# bridge between views and repository ( business logic layer )
from .repository import product_category_repository, product_repository
from .csv_helper import read_csv_file


# some rules used
# 1. brand is compulsary now
# 2. if category is missing use Miscellaneous
# 3. category title should be unique
# 4. category cannot be deleted if products belong to it
# 5. CSV rows should be validated before insertion


# category related business logic
class ProductCategoryService:
    # creating category
    def create(self, data):
        existing_category = product_category_repository.get_by_title(
            data["title"])
        if existing_category:
            return {"error": "Category with this title already exists"}

        return product_category_repository.create(data)

    # get category by id
    def get(self, id):
        return product_category_repository.get(id)

    # list all categories
    def list_all(self, filters=None, sort_by=None):
        return product_category_repository.list_all(filters=filters, sort_by=sort_by)

    # update category
    def update(self, id, data):
        category = product_category_repository.get(id)
        if not category:
            return {"error": "Category not found"}
        # avoid duplicating
        existing_category = product_category_repository.get_by_title(
            data["title"])
        if existing_category and existing_category.id != id:
            return {"error": "Another category with this title already exists"}
        else:
            return product_category_repository.update(id, data)

    # delete category
    def delete(self, id):
        category = product_category_repository.get(id)
        if not category:
            return {"error": "Category not found"}
        product_in_category = product_repository.list_by_category(category)
        if product_in_category.count() > 0:
            return {"error": "Cannot delete category because products are assigned to it"}
        else:
            return product_category_repository.delete(id)

    # get products belonging to same category_id
    def get_products(self, category_id, filters=None, sort_by=None):
        category = product_category_repository.get(category_id)
        if not category:
            return {"error": "Category not found"}
        else:
            return product_repository.list_by_category(category, filters=filters, sort_by=sort_by)

    # add products to a category
    def add_product_to_category(self, category_id, product_id):
        category = product_category_repository.get(category_id)
        if not category:
            return {"error": "Category not found"}
        else:
            product = product_repository.get(product_id)
            if not product:
                return {"error": "Product not found"}
            else:
                return product_repository.assign_to_category(product, category)

    # remove product from category
    def remove_product_category(self, category_id, product_id):
        category = product_category_repository.get(category_id)
        if not category:
            return {"error": "Category not found"}
        else:
            product = product_repository.get(product_id)
            if not product:
                return {"error": "Product not found"}
            if not product.category or product.category.id != category.id:
                return {"error": "Product does not belong to this category"}
            return product_repository.remove_from_category(product)


# product related business logic
class ProductService:
    # creating Miscellaneous category for "no category" products
    def get_default_category(self):
        default_category = product_category_repository.get_by_title(
            "Miscellaneous")
        if not default_category:
            default_category = product_category_repository.create({
                "title": "Miscellaneous",
                "description": "Default category for uncategorized products"
            })
        return default_category

    # creating products
    def create(self, data):
        # brand is compulsary now
        if not data.get("brand") or not str(data["brand"]).strip():
            return {"error": "Brand is required"}
        category_id = data.get("category_id")
        if category_id is not None:
            category_obj = product_category_repository.get(category_id)
            if not category_obj:
                return {"error": "Category not found"}
        else:
            # if category is not defined then go to misc
            category_obj = self.get_default_category()
        product_data = {
            "name": data["name"],
            "description": data["description"],
            "price": data["price"],
            "brand": data["brand"].strip(),
            "quantity": data["quantity"],
            "category": category_obj,
        }
        return product_repository.create(product_data)

    # get product by id
    def get(self, id):
        return product_repository.get(id)

    # list all products
    def list_all(self, filters=None, sort_by=None):
        return product_repository.list_all(filters=filters, sort_by=sort_by)

    # update product
    def update(self, id, data):
        existing_product = product_repository.get(id)
        if not existing_product:
            return None
        if not data.get("brand") or not str(data["brand"]).strip():
            return {"error": "Brand is required"}
        category_id = data.get("category_id")
        if category_id is not None:
            category_obj = product_category_repository.get(category_id)
            if not category_obj:
                return {"error": "Category not found"}
        else:
            category_obj = self.get_default_category()

        product_data = {
            "name": data["name"],
            "description": data["description"],
            "price": data["price"],
            "brand": data["brand"].strip(),
            "quantity": data["quantity"],
            "category": category_obj
        }
        return product_repository.update(id, product_data)

    # delete product
    def delete(self, id):
        return product_repository.delete(id)

    def create_from_csv(self, uploaded_file):
        # these handles must exist in CSV
        required_col = ["name", "description", "price",
                        "brand", "quantity", "category_id"]
        try:
            reader = read_csv_file(
                uploaded_file, requiered_columns=required_col)
        except ValueError as error:
            return {"error": str(error)}

        products_to_create = []

        # start from 2 since row 1 is header line
        for row_number, row in enumerate(reader, start=2):
            name = (row.get("name") or "").strip()
            description = (row.get("description") or "").strip()
            price = (row.get("price") or "").strip()
            brand = (row.get("brand") or "").strip()
            quantity = (row.get("quantity") or "").strip()
            category_id = (row.get("category_id") or "").strip()

            if not name:
                return {"error": f"Row {row_number}: name cannot be empty"}

            if not description:
                return {"error": f"Row {row_number}: description cannot be empty"}

            if not brand:
                # brand is compulsary now
                return {"error": f"Row {row_number}: brand is required"}

            try:
                price = float(price)
            except ValueError:
                return {"error": f"Row {row_number}: invalid price"}

            if price <= 0:
                return {"error": f"Row {row_number}: price must be greater than 0"}

            try:
                quantity = int(quantity)
            except ValueError:
                return {"error": f"Row {row_number}: invalid quantity"}

            if quantity < 0:
                return {"error": f"Row {row_number}: quantity cannot be negative"}

            if category_id:
                try:
                    category_id = int(category_id)
                except ValueError:
                    return {"error": f"Row {row_number}: invalid category_id"}

                category_obj = product_category_repository.get(category_id)
                if not category_obj:
                    return {"error": f"Row {row_number}: category not found"}
            else:
                category_obj = self.get_default_category()

            products_to_create.append({
                "name": name,
                "description": description,
                "price": price,
                "brand": brand,
                "quantity": quantity,
                "category": category_obj,
            })

        return product_repository.bulk_create(products_to_create)


product_service = ProductService()
product_category_service = ProductCategoryService()
