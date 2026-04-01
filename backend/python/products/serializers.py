def serialize_product(product):
    return {
        "id": str(product.id),
        "name": product.name,
        "description": product.description,
        "category": str(product.category.id) if product.category else None,
        "price": product.price,
        "brand": product.brand,
        "quantity": product.quantity,
        "created_at": product.created_at,
        "updated_at": product.updated_at
    }

def serialize_catgeory(category):
    return {
        "id": str(category.id),
        "name": category.name,
        "description": category.description,
        "created_at": category.created_at,
        "updated_at": category.updated_at,
    }
