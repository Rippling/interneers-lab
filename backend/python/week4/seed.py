from datetime import datetime
from .models import Product, ProductCategory

DEFAULT_CATEGORY_TITLE = "Miscellaneous"
DEFAULT_CATEGORY_DESCRIPTION = "Default category for uncategorized products"
DEFAULT_BRAND = "Unknown"


# ensures default category exists, it is also safe to run multiple time (idempotency)
def seed_prod_category():
    created_count = 0
    existing = ProductCategory.objects(
        title__iexact=DEFAULT_CATEGORY_TITLE
    ).first()

    if not existing:
        ProductCategory(
            title=DEFAULT_CATEGORY_TITLE,
            description=DEFAULT_CATEGORY_DESCRIPTION,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ).save()
        created_count += 1

    return created_count


# returns the miscellaneos categorym creats if it doesnt exist
def get_default_category():
    category = ProductCategory.objects(
        title__iexact=DEFAULT_CATEGORY_TITLE
    ).first()

    if not category:
        category = ProductCategory(
            title=DEFAULT_CATEGORY_TITLE,
            description=DEFAULT_CATEGORY_DESCRIPTION,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        category.save()

    return category


# fixing old products
def migrate_products():
    default_category = get_default_category()
    tot_prod_check = 0
    cat_fix_count = 0
    brand_fix_count = 0
    tot_prod_upd = 0

    products = Product.objects

    for product in products:
        tot_prod_check += 1
        changed = False

        # fix missing category
        if product.category is None:
            product.category = default_category
            cat_fix_count += 1
            changed = True

        # fix missing brand
        current_brand = product.brand if product.brand is not None else ""
        if not str(current_brand).strip():
            product.brand = DEFAULT_BRAND
            brand_fix_count += 1
            changed = True

        if changed:
            product.updated_at = datetime.utcnow()
            product.save()
            tot_prod_upd += 1

    return {
        "tot_prod_check": tot_prod_check,
        "cat_fix_count": cat_fix_count,
        "brand_fix_count": brand_fix_count,
        "tot_prod_upd": tot_prod_upd,
    }


def startup_seed_and_migration():
    categories_created = seed_prod_category()
    migration_summary = migrate_products()

    print("\nStartup seed/migration summary")
    print(f"Categories created      : {categories_created}")
    print(
        f"Products checked        : {migration_summary['tot_prod_check']}")
    print(
        f"Products updated        : {migration_summary['tot_prod_upd']}")
    print(
        f"Category fixes applied  : {migration_summary['cat_fix_count']}")
    print(
        f"Brand fixes applied     : {migration_summary['brand_fix_count']}")
