# repository.py : bridge between service and databse
from datetime import datetime
from .models import Product, ProductCategory


class ProductCategoryRepository:
    # create category
    def create(self, data):
        category = ProductCategory(
            title=data["title"],
            description=data.get("description", ""),
            updated_at=datetime.utcnow(),
        )
        category.save()
        return category

    # get category with id
    def get(self, id):
        return ProductCategory.objects(id=id).first()

    # get category with title
    def get_by_title(self, title):
        return ProductCategory.objects(title__iexact=title.strip()).first()

    # list all categories
    def list_all(self, filters=None, sort_by=None):
        queryset = ProductCategory.objects
        # repository.py will only do filtering+sorting and returning queryset, pagination is done in views.py

        # manual filtering is added (icontains : case sensitive substring match)
        if filters:
            if filters.get("title"):
                queryset = queryset.filter(title__icontains=filters["title"])

        # manual sorting is added
        allowed_sort_fields = ["id", "title", "created_at", "updated_at"]
        if sort_by and sort_by.lstrip("-") in allowed_sort_fields:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by("id")

        return queryset

    # update category
    def update(self, id, data):
        category = self.get(id)
        if not category:
            return None

        category.title = data["title"]
        category.description = data.get("description", "")
        category.updated_at = datetime.utcnow()
        category.save()
        return category

    # delete category
    def delete(self, id):
        category = self.get(id)
        if not category:
            return False

        category.delete()
        return True


class ProductRepository:
    # create product
    def create(self, data):
        product = Product(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            brand=data["brand"],
            quantity=data["quantity"],
            category=data.get("category"),
            updated_at=datetime.utcnow(),
        )
        product.save()
        return product

    # get product with id
    def get(self, id):
        return Product.objects(id=id).first()

    # list all products
    def list_all(self, filters=None, sort_by=None):
        queryset = Product.objects
        # filtering
        if filters:
            if filters.get("name"):
                queryset = queryset.filter(name__icontains=filters["name"])

            if filters.get("brand"):
                queryset = queryset.filter(brand__icontains=filters["brand"])

            if filters.get("min_price") is not None:
                queryset = queryset.filter(price__gte=filters["min_price"])

            if filters.get("max_price") is not None:
                queryset = queryset.filter(price__lte=filters["max_price"])

            if filters.get("min_quantity") is not None:
                queryset = queryset.filter(
                    quantity__gte=filters["min_quantity"])

            if filters.get("max_quantity") is not None:
                queryset = queryset.filter(
                    quantity__lte=filters["max_quantity"])

            if filters.get("category"):
                queryset = queryset.filter(category=filters["category"])

        # sorting
        allowed_sort_fields = ["id", "name", "price",
                               "brand", "quantity", "created_at", "updated_at"]

        if sort_by and sort_by.lstrip("-") in allowed_sort_fields:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by("id")

        return queryset

    # update product
    def update(self, id, data):
        product = self.get(id)
        if not product:
            return None

        product.name = data["name"]
        product.description = data["description"]
        product.price = data["price"]
        product.brand = data["brand"]
        product.quantity = data["quantity"]
        product.category = data.get("category")
        product.updated_at = datetime.utcnow()
        product.save()
        return product

    # delete product
    def delete(self, id):
        product = self.get(id)
        if not product:
            return False

        product.delete()
        return True

    # list all products belonging to one category
    def list_by_category(self, category, filters=None, sort_by=None):
        queryset = Product.objects(category=category)

        if filters:
            if filters.get("name"):
                queryset = queryset.filter(name__icontains=filters["name"])

            if filters.get("brand"):
                queryset = queryset.filter(brand__icontains=filters["brand"])

            if filters.get("min_price") is not None:
                queryset = queryset.filter(price__gte=filters["min_price"])

            if filters.get("max_price") is not None:
                queryset = queryset.filter(price__lte=filters["max_price"])

            if filters.get("min_quantity") is not None:
                queryset = queryset.filter(
                    quantity__gte=filters["min_quantity"])

            if filters.get("max_quantity") is not None:
                queryset = queryset.filter(
                    quantity__lte=filters["max_quantity"])

        allowed_sort_fields = ["id", "name", "price",
                               "brand", "quantity", "created_at", "updated_at"]

        if sort_by and sort_by.lstrip("-") in allowed_sort_fields:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by("id")

        return queryset

    # assign product to category
    def assign_to_category(self, product, category):
        product.category = category
        product.updated_at = datetime.utcnow()
        product.save()
        return product

    # remove product from category
    def remove_from_category(self, product):
        product.category = None
        product.updated_at = datetime.utcnow()
        product.save()
        return product

    # bulk create many products in case of CSV
    def bulk_create(self, products_data):
        created_products = []

        for data in products_data:
            product = Product(
                name=data["name"],
                description=data["description"],
                price=data["price"],
                # brand consistency is taken care in serializers and service so need to check here again
                brand=data["brand"],
                quantity=data["quantity"],
                category=data.get("category"),
                updated_at=datetime.utcnow(),
            )
            product.save()
            created_products.append(product)

        return created_products


product_repository = ProductRepository()
product_category_repository = ProductCategoryRepository()
