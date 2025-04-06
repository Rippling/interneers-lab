import logging
from product.models.CategoryModel import ProductCategory
from product.models.ProductModel import Product

#set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

logger=logging.getLogger(__name__)

#clear all data from test db
def clear_test_data():
    try:
        ProductCategory.objects.delete()
        Product.objects.delete()
        logger.info("Test database cleared successfully.")
    except Exception as e:
        logger.error("Error clearing test database", exc_info=True)

#seed test db with sample categories
def seed_test_categories():
    categories=[
        {"title": "Electronics", "description": "Electronic devices and accessories"},
        {"title": "Clothing", "description": "Apparel and fashion items"},
        {"title": "Books", "description": "Books and publications"}
    ]
    
    created_categ=[]

    for categ_data in categories:
        try:
            category=ProductCategory(**categ_data)
            category.save()
            created_categ.append(category)
            logger.info(f"Created category: {category.title}")
        except Exception as e:
            logger.error(f"Error creating category {categ_data['title']}", exc_info=True)

    return created_categ

#seed test db with sample products
def seed_test_products(categories):
    if not categories:
        logger.error("No categories available for seeding products")
        return []

#mapping of category titles to category objects
    category_map={cat.title: cat for cat in categories}

    products=[
        {
            "name": "Smartphone",
            "description": "Latest model smartphone",
            "category": category_map.get("Electronics"),
            "price": 9999.99,
            "brand": "Apple",
            "quantity": 50
        },
        {
            "name": "T-shirt",
            "description": "Cotton t-shirt",
            "category": category_map.get("Clothing"),
            "price": 1999.99,
            "brand": "Zara",
            "quantity": 100
        },
        {
            "name": "Python Programming",
            "description": "Guide to Python programming",
            "category": category_map.get("Books"),
            "price": 399.99,
            "brand": "TechBooks",
            "quantity": 30
        },
        {
            "name": "Laptop",
            "description": "High-performance laptop",
            "category": category_map.get("Electronics"),
            "price": 149999.99,
            "brand": "Apple",
            "quantity": 25
        }
    ]

    created_prod=[]

    for prod_data in products:
        if not prod_data["category"]:
            logger.warning(f"Skipping product '{prod_data['name']}' due to missing category")
            continue
        try:
            product=Product(**prod_data)
            product.save()
            created_prod.append(product)
            logger.info(f"Created product: {product.name}")
        except Exception as e:
            logger.error(f"Error creating product {prod_data['name']}", exc_info=True)

    return created_prod

#main func. to seed test db with initial data
def seed_test_database():
    try:
        logger.info("Starting to seed the test database...")

        clear_test_data()
        categories=seed_test_categories()
        products=seed_test_products(categories)

        logger.info("Test database seeding completed successfully.")
        return {
            "categories": categories,
            "products": products
        }

    except Exception as e:
        logger.error("Error during test database seeding", exc_info=True)
        return None

if __name__ == "__main__":
    seed_test_database()


