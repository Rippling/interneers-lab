from product_csr.models import Product
from product_csr.repositories.category_repository import CategoryRepository


class ProductRepository:
     def __init__(self):
        self.category_repo = CategoryRepository() 


     def create(self, data):
        product = Product(**data)
        product.save()
        return product

    
     def get_all(self):
        return Product.objects()

    
     def filter_products(self, filters):
       queryset = Product.objects()

       if filters.get("brand"):
        queryset = queryset.filter(brand=filters["brand"])

       if filters.get("search"):
        queryset = queryset.filter(name__icontains=filters["search"])

       if filters.get("min_price") is not None:
        queryset = queryset.filter(price__gte=filters["min_price"])

       if filters.get("max_price") is not None:
        queryset = queryset.filter(price__lte=filters["max_price"])

       if filters.get("min_quantity") is not None:
        queryset = queryset.filter(quantity__gte=filters["min_quantity"])

       if filters.get("max_quantity") is not None:
        queryset = queryset.filter(quantity__lte=filters["max_quantity"])

       if filters.get("categories"):
        category_ids = filters.get("categories")
        category_ids = [cid.strip() for cid in category_ids.split(",") if cid.strip()]

        category_objects = []

        for cid in category_ids:
            category = self.category_repo.get_by_id(cid)
            if category:
                category_objects.append(category)

        queryset = queryset.filter(category__in=category_objects)

        return queryset


    
    
     def get_by_id(self, product_id):
        return Product.objects(id=product_id).first()

    
     def update(self, product, data):
        product.name = data.get("name", product.name)
        product.brand = data.get("brand", product.brand)
        product.price = data.get("price", product.price)
        product.quantity = data.get("quantity", product.quantity)
        product.save()
        return product

    
     def delete(self, product):
        product.delete()

    
     def get_by_category(self, category):
        return Product.objects(category=category)