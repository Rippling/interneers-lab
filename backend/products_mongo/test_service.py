from product_service import ProductService

def run_tests():
    print("\n🚀 Running Product Service Tests...\n")

    # ✅ Step 1: Create a Product
    product_data = {
        "name": "New Product",
        "description": "Latest Samsung smartphone with AI features.",
        "category": "Electronics",
        "price": 1199.99,
        "brand": "Samsung",
        "quantity_in_warehouse": 100
    }
    new_product = ProductService.create_product(product_data)
    print(f"✅ Created Product: {new_product['id']}")

    # ✅ Step 2: Get All Products
    all_products = ProductService.get_all_products()
    print("\n📦 All Products:", all_products)

    # ✅ Step 3: Get a Single Product
    product = ProductService.get_product_by_id(new_product['id'])
    print(f"\n🔍 Found Product: {product['name']}")

    # ✅ Step 4: Update a Product
    updated_data = {"price": 1099.99}
    updated_product = ProductService.update_product(new_product['id'], updated_data)
    print(f"\n💰 Updated Price: {updated_product['price']}")

    # ✅ Step 5: Fetch Paginated Products (First 5)
    products_page_1 = ProductService.get_all_products(page=1, per_page=5)
    print("\n📄 Page 1 Products:", products_page_1)

    # ✅ Step 6: Fetch Products by Date Range
    filtered_products = ProductService.get_products_by_date_range("2024-03-01", "2024-03-10")
    print("\n📆 Products Created in Date Range:", filtered_products)

    # ✅ Step 7: Update Another Product
    if products_page_1:
        product_id = products_page_1[0]["id"]  # Take first product's ID
        updated_product = ProductService.update_product(product_id, {"price": 1299.99})
        print("\n🛠️ Updated Product:", updated_product)

    # ✅ Step 8: Delete a Product (Optional)
    delete_flag = input("\n❗ Do you want to delete the newly created product? (y/n): ").strip().lower()
    if delete_flag == "y":
        if ProductService.delete_product(new_product['id']):
            print(f"🗑️ Deleted Product: {new_product['id']}")
        else:
            print("❌ Error: Product deletion failed.")

if __name__ == "__main__":
    run_tests()
