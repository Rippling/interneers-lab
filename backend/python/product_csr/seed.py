from product_csr.models import Product, ProductCategory


def clear_product_csr_data():
    Product.drop_collection()
    ProductCategory.drop_collection()


def seed_product_csr_data():
    electronics = ProductCategory(
        title="Electronics",
        description="Devices and gadgets"
    ).save()

    fashion = ProductCategory(
        title="Fashion",
        description="Clothing and accessories"
    ).save()

    home = ProductCategory(
        title="Home",
        description="Home essentials"
    ).save()

    iphone = Product(
        name="iPhone 15",
        brand="Apple",
        price=799.0,
        quantity=10,
        category=electronics,
    ).save()

    galaxy = Product(
        name="Galaxy S24",
        brand="Samsung",
        price=699.0,
        quantity=8,
        category=electronics,
    ).save()

    tshirt = Product(
        name="T-Shirt",
        brand="H&M",
        price=19.99,
        quantity=25,
        category=fashion,
    ).save()

    return {
        "categories": {
            "electronics": electronics,
            "fashion": fashion,
            "home": home,
        },
        "products": {
            "iphone": iphone,
            "galaxy": galaxy,
            "tshirt": tshirt,
        },
    }
