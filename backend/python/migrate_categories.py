from mongoengine import connect
from products.models import Product, ProductCategory

def run_category_migration():
    
    print("Connecting to Database...")
    
    connect(
        db='inventory_db',           
        host='localhost',
        port=27019,                  
        username='root',    
        password='example',    
        authentication_source='admin' 
    )
    print("Starting category migration...")
    
    uncategorized = ProductCategory.objects(title = "Uncategorized").first()
    
    if not uncategorized:
        print("Creating 'uncategorized' fallback category...")
        uncategorized = ProductCategory(title = 'Uncategorized', description="System default for legacy products missing a category")
        uncategorized.save()
        
    else:
        print("Found 'Uncategorized' category.")
        
    all_products = Product.objects()
    print(f"Found {len(all_products)} total products in the database.")
    
    count = 0
    for product in all_products:
        if not product.category:
            product.category = uncategorized
            product.save()
            count+=1
            print(f" -> Assigned category to product: {product.name}")
            
    print(f"Migration complete! Successfully linked {count} legacy products to the Uncategorized bucket.")
    
    
if __name__ == "__main__":
    run_category_migration()