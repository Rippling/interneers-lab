from product.models.category import ProductCategory

def seed_categories():
    ProductCategory(category_name="Books", description="All kinds of books").save()
    ProductCategory(category_name="Electronics", description="Gadgets and devices").save()
