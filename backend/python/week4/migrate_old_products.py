from datetime import datetime
from .db_connection import initialize_mongo
from .models import Product, ProductCategory

DEFAULT_CATEGORY_TITLE = "Miscellaneous"
DEFAULT_CATEGORY_DESCRIPTION = "Default category for uncategorized products"
DEFAULT_BRAND = "Unknown"


# creating default category
def create_default_category():
    category = ProductCategory.objects(
        title__iexact=DEFAULT_CATEGORY_TITLE).first()
    if not category:
        category = ProductCategory(
            title=DEFAULT_CATEGORY_TITLE,
            description=DEFAULT_CATEGORY_DESCRIPTION,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        category.save()
        print(f"Created default category: {DEFAULT_CATEGORY_TITLE}")

    else:
        print(f"Default category already exists: {DEFAULT_CATEGORY_TITLE}")

    return category


def migrate_product():
    # connect mongodb
    initialize_mongo()
    print("Connected to MongoDB")

    # ensuring default categories
    default_category = create_default_category()

    # finding and fixing all products
    tot_prod_checked = 0
    cat_fix_count = 0
    brand_fix_count = 0
    tot_prod_upd = 0

    products = Product.objects

    for product in products:
        tot_prod_checked += 1
        changed = False

        # fix missing category
        if product.category is None:
            product.category = default_category
            cat_fix_count += 1
            changed = True

        # fix missing brand
        if product.brand is not None:
            current_brand = product.brand
        else:
            current_brand = ""
        if not str(current_brand).strip():
            product.brand = DEFAULT_BRAND
            brand_fix_count += 1
            changed = True

        # save only if something is changed
        if changed:
            product.updated_at = datetime.utcnow()
            product.save()
            tot_prod_upd += 1

    print("\nMigration completed successfully")
    print(f"Total products checked   : {tot_prod_checked}")
    print(f"Products updated         : {tot_prod_upd}")
    print(f"Missing category fixed   : {cat_fix_count}")
    print(f"Missing brand fixed      : {brand_fix_count}")


if __name__ == "__main__":
    migrate_product()
