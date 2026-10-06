# for adv task we have to retrieve stock level as well
from week4.db_connection import initialize_mongo
from week4.models import Product


def get_product_stock(product_name):
    initialize_mongo()
    product = Product.objects(name__icontains=product_name).first()
    if not product:
        return None
    return {
        "id": product.id,
        "name": product.name,
        "brand": product.brand,
        "category": product.category.title if product.category else None,
        "price": float(product.price),
        "quantity": product.quantity,
        "description": product.description,
    }


if __name__ == "__main__":
    query_name = input("Enter product name to check stock: ").strip()
    if not query_name:
        print("No Product name entered.")
    else:
        result = get_product_stock(query_name)
        if not result:
            print("Product not found in the database.")
        else:
            print("Product found:")
            print(f"ID: {result['id']}")
            print(f"Name: {result['name']}")
            print(f"Brand: {result['brand']}")
            print(f"Category: {result['category']}")
            print(f"Price: {result['price']}")
            print(f"Quantity: {result['quantity']}")
            print(f"Description: {result['description']}")
