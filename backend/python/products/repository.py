from .models import Product, ProductCategory
from bson.objectid import ObjectId

class ProductRepository:
    
    def get_all_products(self, filters = None):
        if not filters:
            return Product.objects()
        mongo_query = {}
        
        if 'min_price' in filters:
            mongo_query['price__gte'] = float(filters['min_price'])
        if 'max_price' in filters:
            mongo_query['price__lte'] = float(filters['max_price'])
        if 'brand' in filters:
            mongo_query['brand__icontains'] = filters['brand']
        if 'categories' in filters:
            category_ids = []
            
            for cid in filters['categories']:
                try:
                    category_ids.append(ObjectId(cid))
                except Exception:
                    pass
            if category_ids:
                mongo_query['category__in'] = category_ids
        return Product.objects(**mongo_query)
            

    def get_product_by_id(self, product_id):
        return Product.objects(id=product_id).first()

    def create_product(self, product_data):
        new_product = Product(**product_data) 
        new_product.save() 
        return new_product

    def delete_product(self, product_id):
        product = self.get_product_by_id(product_id)
        if product:
            product.delete() 
            return True
        return False
    
    def get_products_by_category(self, category_id):
        return Product.objects(category=category_id)
    
    def update_product(self, product_id, update_data):
        product = self.get_product_by_id(product_id=product_id)
        if product:
            for key, value in update_data.items():
                if key == 'category' and value is not None:
                    setattr(product,key,ObjectId(value))
                else:
                    setattr(product, key, value)
            product.save()
            return product
        return None
    
    def bulk_create_products(self, product_data_list):
        product_instances=[]
        
        for data in product_data_list:
            if 'category' in data and data['category'] is not None:
                data['category'] = ObjectId(data['category'])
                
            new_product = Product(**data)
            try:
                new_product.validate() 
            except ValidationError as e:
                return {"error": f"Validation failed for '{data.get('name', 'Unknown')}': {str(e)}"}
            product_instances.append(new_product)
        if product_instances:
            Product.objects.insert(product_instances)
            return {"count": len(product_instances)}
        return {"count": 0}



product_repo = ProductRepository()

class ProductCategoryRepository:
    
    def get_all_categories(self):
        return ProductCategory.objects()

    def get_category_by_id(self, category_id):
        return ProductCategory.objects(id=category_id).first()

    def create_category(self, category_data):
        new_category = ProductCategory(**category_data) 
        new_category.save() 
        return new_category

    def delete_category(self, category_id):
        category = self.get_category_by_id(category_id)
        if category:
            category.delete() 
            return True
        return False

category_repo = ProductCategoryRepository()