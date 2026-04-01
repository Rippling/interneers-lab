from django.urls import path
from .controllers import product, category

urlpatterns = [
    path("products/", product.products, name="products"),
    # GET  -> list products
    # POST -> create product

    path("products/<str:product_id>/", product.product_detail, name="product_detail"),
    # GET    -> get product
    # PUT    -> update product
    # PATCH  -> partial update
    # DELETE -> delete product

]

urlpatterns += [
    path("categories/", category.categories, name="categories"),
    # GET  -> list categories
    # POST -> create category

    path(
        "categories/<str:category_id>/",
        category.category_detail,
        name="category_detail",
    ),
    # GET    -> retrieve category
    # PUT    -> update category
    # PATCH  -> partial update
    # DELETE -> delete category

    path(
        "categories/<str:category_id>/products/",
        category.list_products_by_category_id,
        name="products_by_category",
    ),
    # GET -> list products by category
]