import os
import django
from mongoengine import connect
from products.models import Product

def run_migration():
    print("Connecting to database...")
    connect(
        db='inventory_db',           
        host='localhost',
        port=27019,                  
        username='root',   
        password='example',   
        authentication_source='admin' 
    )
    print("Starting brand migration...")
    
    all_products = Product.objects()
    print(f"Found {len(all_products)} products in the database")
    
    count=0
    for product in all_products:
        if not product.brand:
            product.brand = "Legacy (Unknown Brand)"
            product.save()
            count+=1
            print(f"Updated product: {product.name}")
        
    print(f"Migration complete! Successfully updated {count} products.")
    
if __name__== "__main__":
    run_migration()