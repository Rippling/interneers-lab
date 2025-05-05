from ..models import Category, Product
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

def seed_categories():
    """
    Seed the database with test categories
    """
    categories = [
        {
            'name': 'Electronics',
            'description': 'Electronic devices and accessories'
        },
        {
            'name': 'Clothing',
            'description': 'Apparel and fashion items'
        },
        {
            'name': 'Books',
            'description': 'Books and publications'
        },
        {
            'name': 'Home & Kitchen',
            'description': 'Home and kitchen appliances and accessories'
        }
    ]
    
    created_categories = []
    for category_data in categories:
        try:
            # Skip if category with same name already exists
            if not Category.objects(name=category_data['name']):
                category = Category(**category_data)
                category.save()
                created_categories.append(category)
                logger.info(f"Created category: {category.name}")
            else:
                logger.info(f"Category already exists: {category_data['name']}")
        except Exception as e:
            logger.error(f"Error creating category {category_data['name']}: {str(e)}")
    
    return created_categories

def seed_products(categories=None):
    """
    Seed the database with test products
    If categories are provided, use them; otherwise create new ones
    """
    if not categories:
        categories = seed_categories()
    
    # If still no categories, can't create products
    if not categories:
        # Get existing categories
        categories = list(Category.objects.all())
        if not categories:
            logger.error("No categories available, can't create products")
            return []
    
    # Dictionary to map category name to category object
    category_map = {category.name: category for category in categories}
    
    products = [
        {
            'sku': 'ELE-12345',
            'name': 'Smartphone',
            'description': 'Latest smartphone with advanced features',
            'category': category_map.get('Electronics', categories[0]),
            'brand': 'TechBrand',
            'tags': ['phone', 'mobile', 'tech'],
            'price': Decimal('999.99'),
            'quantity': 25,
            'low_stock_threshold': 5,
            'dimensions': '15x7x1',
            'status': 'active',
            'featured': True
        },
        {
            'sku': 'CLO-12345',
            'name': 'T-Shirt',
            'description': 'Comfortable cotton t-shirt',
            'category': category_map.get('Clothing', categories[0]),
            'brand': 'FashionBrand',
            'tags': ['apparel', 'casual', 'cotton'],
            'price': Decimal('29.99'),
            'quantity': 100,
            'low_stock_threshold': 20,
            'dimensions': '30x40x2',
            'status': 'active',
            'featured': False
        },
        {
            'sku': 'BOK-12345',
            'name': 'Programming Guide',
            'description': 'Comprehensive programming guide for beginners',
            'category': category_map.get('Books', categories[0]),
            'brand': 'TechPublisher',
            'tags': ['programming', 'education', 'tech'],
            'price': Decimal('49.99'),
            'quantity': 50,
            'low_stock_threshold': 10,
            'dimensions': '22x15x3',
            'status': 'active',
            'featured': False
        },
        {
            'sku': 'HMK-12345',
            'name': 'Coffee Maker',
            'description': 'Automatic coffee maker with timer',
            'category': category_map.get('Home & Kitchen', categories[0]),
            'brand': 'HomeBrand',
            'tags': ['appliance', 'kitchen', 'coffee'],
            'price': Decimal('89.99'),
            'quantity': 15,
            'low_stock_threshold': 3,
            'dimensions': '25x20x35',
            'status': 'active',
            'featured': True
        }
    ]
    
    created_products = []
    for product_data in products:
        try:
            # Skip if product with same SKU already exists
            if not Product.objects(sku=product_data['sku']):
                product = Product(**product_data)
                product.save()
                created_products.append(product)
                logger.info(f"Created product: {product.name} (SKU: {product.sku})")
            else:
                logger.info(f"Product already exists: {product_data['sku']}")
        except Exception as e:
            logger.error(f"Error creating product {product_data['name']}: {str(e)}")
    
    return created_products

def seed_all():
    """
    Seed all test data (categories and products)
    """
    logger.info("Seeding test data...")
    categories = seed_categories()
    products = seed_products(categories)
    logger.info(f"Seeded {len(categories)} categories and {len(products)} products")
    return categories, products

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed_all() 