from productAPI.repositories import ProductRepository, ProductCategoryRepository
from django.core.paginator import Paginator
import csv
from io import StringIO
from productAPI.constants import DEFAULT_PRODUCT_PAGE_SIZE

class ProductService:
    
    @staticmethod
    def list_products(filters=None):
        
        if filters:
            category_names=filters.get("categories")
            if category_names:
                resolved_categories = []
                for title in category_names:
                    category = ProductCategoryRepository.get_by_title(title)
                    if category:
                        resolved_categories.append(category)
                filters["categories"]=resolved_categories
            
            products=ProductRepository.get_filtered(filters)
        else:
            products=ProductRepository.get_all()
            
        sortby = filters.get("sortby", "desc")
        page_number = filters.get("page_number", 1)
        
        
        
        if sortby == "asc":
            products=products.order_by("updated_at")
        else:
            products=products.order_by("-updated_at")
        
        if page_number:
            paginator = Paginator(products,DEFAULT_PRODUCT_PAGE_SIZE)
            page=paginator.get_page(page_number)
            return page

        return products
    
    @staticmethod
    def list_single_product(product_id):
        product = ProductRepository.get_by_id(product_id)
        
        if not product:
            return None
        
        return product
        
    
    @staticmethod
    def create_product(validated_data):
        return ProductRepository.create(validated_data)
    
    @staticmethod
    def update_product(product_id, validated_data):
        product = ProductRepository.get_by_id(product_id)
        
        if not product:
            return None
        
        return ProductRepository.update(product, validated_data)
    
    
    @staticmethod
    def delete_product(product_id):
        product = ProductRepository.get_by_id(product_id)
        
        if not product:
            return None
        
        ProductRepository.delete(product)
        
        return True
    
        
    @staticmethod
    def assign_category(product_id, category_id):
        product = ProductRepository.get_by_id(product_id)
        category = ProductCategoryRepository.get_by_id(category_id)
        
        if product is None or category is None:
            return False
        
        return ProductRepository.assign_category(product, category)
        
        
        
    @staticmethod
    def unassign_category(product_id, category_id):
        product = ProductRepository.get_by_id(product_id)
        
        if product is None:
            return False
        
        if product.category is None or str(product.category.id) != category_id:
            return False
        
        return ProductRepository.unassign_category(product)
        
        
        
    @staticmethod
    def bulk_create_products(file):
        
        file_decode = file.read().decode("utf-8")
        io_string = StringIO(file_decode)
        
        reader = csv.DictReader(io_string)
        
        required_headers = {'name', 'brand'}
        
        if not required_headers.issubset(reader.fieldnames):
            raise ValueError(f"CSV missing required headers: {required_headers - set(reader.fieldnames)}")

        for row_num, row in enumerate(reader, start=2):  
            if not row.get('name') or not row.get('brand'):
                raise ValueError(f"Row {row_num}: 'name' and 'brand' are required")
            if row.get('price') and not row['price'].isdigit():
                raise ValueError(f"Row {row_num}: 'price' must be a number")        
                
        
        products_data = []
        
        for row in reader:
            if not row.get("category"):
                row["category"] = None
            products_data.append(row)
        
        result = ProductRepository.bulk_insert(products_data)
        if result is not False:
            return {
                "message": "Bulk Insert Successful!!",
                "count": len(products_data)
            }