# 🚀 Week 4 - Interneers Lab

This week, we focused on **joining schemas in our database**. We introduced a **ProductCategory** model and linked it to the **Product** model using a **foreign key (ReferenceField)** in MongoDB.

## ✅ Achievements

By the end of this week, we successfully:
- Established relationships between products and categories
- Implemented CRUD operations for categories
- Added filters for fetching products
- Migrated existing products to the new category structure

---

## 🛠️ Implementation Steps

### Step 1: Add ProductCategory Model
We added a `ProductCategory` model to `models.py` and modified the **Product** model's `category` field:

```python
from mongoengine import Document, StringField, ReferenceField, FloatField

class ProductCategory(Document):
    name = StringField(required=True, unique=True)

class Product(Document):
    name = StringField(required=True)
    price = FloatField(required=True)
    category = ReferenceField(ProductCategory, reverse_delete_rule=2)  # CASCADE
🔹 Reverse Delete Rule Options:
reverse_delete_rule=2 (CASCADE): Deletes all related products if a category is removed

reverse_delete_rule=3 (NULLIFY): Keeps products even if their category is deleted

Step 2: Implement CRUD for Product Categories
We created two new files:

🔹 product_category_repository.py
Handles database operations:

python
Copy
def create_category(name):
    category = ProductCategory(name=name)
    category.save()
    return category
🔹 product_category_services.py
Fetches all products under a category:

python
Copy
def get_products_by_category(category_id):
    return Product.objects(category=category_id)
Step 3: Update product_repository.py
🔹 Enhancements:
When creating a product, if a new category is provided, it gets added to the database

While updating a product, if the category doesn't exist, it raises an error

Added methods to add and remove products in a category

python
Copy
def add_product_to_category(product_id, category_id):
    product = Product.objects(id=product_id).first()
    if product:
        product.category = category_id
        product.save()
Step 4: Add Validations
Used DRF Serializers to validate requests

Set branding to null for existing products without branding

Step 5: Update Views and URLs
Modified views.py to handle all API changes

Updated urls.py to include new category-related routes

🔥 Advanced Tasks
✅ Step 1: Seed Categories
File: seed_categories.py
Ensures all products without a category get assigned a default category when the server starts.

Run it using:

bash
Copy
python -m products_mongo.seed_categories
✅ Step 2: Implement Rich Filters
File: product_services.py
Added advanced filtering options:

python
Copy
def filter_products(category=None, name=None, price_min=None, price_max=None, brand=None):
    query = Product.objects()
    if category:
        query = query.filter(category=category)
    if name:
        query = query.filter(name__icontains=name)
    if price_min and price_max:
        query = query.filter(price__gte=price_min, price__lte=price_max)
    if brand:
        query = query.filter(brand=brand)
    return query
🔹 Supports filtering by:
✅ Category

✅ Name

✅ Price range

✅ Brand

✅ Step 3: Migrate Products Without a Category
File: product_migrations.py
Moves products without a category into a default category.

Run it using:

bash
Copy
python -m products_mongo.migrate_products
🎯 Final Thoughts
By the end of this week, we successfully implemented category-based product management, improved query capabilities with rich filters, and ensured smooth data migration. 🚀🔥

Copy

This README features:
- Clear section headers
- Proper code blocks with syntax highlighting
- Emoji icons for visual organization
- Consistent formatting
- Easy-to-scan bullet points
- Logical flow from setup to advanced features
