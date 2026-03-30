import csv
import io
from .models import Product

class CategoryService:
    def __init__(self, repository):
        self.repository = repository

    def create_category(self, data):
        if not data.get('title'):
            raise ValueError("Category title is required.")
        return self.repository.create(data)

    def get_all_categories(self):
        return self.repository.get_all()
    
    def delete_category(self, category_id):
        # 1. First, orphan any products that belonged to this category
        from .models import Product # Import here to avoid circular imports if necessary
        Product.objects(category=category_id).update(set__category=None)
        
        # 2. Then, safely delete the category
        return self.repository.delete(category_id)


class ProductService:
    def __init__(self, repository):
        self.repository = repository

    def get_products_by_category(self, category_id):
        return self.repository.get_by_category(category_id)

    def update_product_category(self, product_id, category_id):
        return self.repository.update_category(product_id, category_id)

    def process_bulk_csv(self, file_obj):
        # Decode and read the CSV
        decoded_file = file_obj.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        
        products_to_insert = []
        
        for row in reader:
            # Requirement 5 Validation: Enforce brand at the Service level
            if not row.get('brand'):
                raise ValueError(f"Validation failed: Product '{row.get('name')}' is missing a brand.")
            
            # Convert CSV strings to floats/ints where necessary
            try:
                row['price'] = float(row['price'])
                row['quantity'] = int(row['quantity'])
            except ValueError:
                raise ValueError(f"Invalid price or quantity for product '{row.get('name')}'.")

            # Create a MongoEngine model instance in memory (don't save yet)
            product = Product(**row)
            products_to_insert.append(product)

        # If we loop through the whole CSV and no ValueError is raised, bulk save them all
        if products_to_insert:
            self.repository.bulk_insert(products_to_insert)
            return len(products_to_insert)
        return 0