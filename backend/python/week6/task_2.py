import os
import json
from decimal import Decimal
from dotenv import load_dotenv
from google import genai
from week4.db_connection import initialize_mongo
from week4.models import Product, ProductCategory
from week6.schema import ProductListSchema

load_dotenv()
initialize_mongo()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# creating category if it does not exist
def get_create_category(category_title):
    cat_title = category_title.strip()
    if not cat_title:
        cat_title = "Miscellaneous"
    category = ProductCategory.objects(title=cat_title).first()
    if category:
        return category
    category = ProductCategory(
        title=cat_title,
        description=f"Auto-created from Gemini synthetic inventory data for {cat_title}"
    )
    category.save()
    return category


# creating products with gemini
def generate_products_with_gemini():
    prompt = """
Generate exactly 5 products for a toy store.

Return valid JSON only in this structure:
{
  "products": [
    {
      "name": "string",
      "description": "string",
      "category": "string",
      "brand": "string",
      "price": 10.99,
      "quantity": 25
    }
  ]
}

Rules:
- Include exactly 5 products
- Product name must never be empty
- Brand must never be empty
- Description must never be empty
- Use realistic toy store categories like puzzles, dolls, action figures, board games, educational toys, building blocks, plush toys, remote control toys, outdoor toys
- price must be a float greater than 0
- quantity must be an integer greater than or equal to 0
- do not include markdown
- output valid JSON only
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "temperature": 0.3,
            "response_mime_type": "application/json",
            "response_schema": ProductListSchema,
        }
    )
    print("\nRAW GEMINI RESPONSE:\n")
    print(response.text)
    validated_data = ProductListSchema.model_validate_json(response.text)
    print(f"\nValidated product count: {len(validated_data.products)}")
    return validated_data


# exporting products as json
def export_product_to_json(validated_data, filepath: str = "week6/generated_products.json"):
    product_as_dicts = []
    for product in validated_data.products:
        # .model_dump converts each product into dictionary (from pydantic form)
        product_dict = product.model_dump()
        product_as_dicts.append(product_dict)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump({"products": product_as_dicts}, file, indent=2)
    print(f"\nValidated products exported to {filepath}")


# saving products to week4 db
def save_products_to_week4(validated_data):
    saved_count = 0

    for item in validated_data.products:
        new_name = item.name.strip()
        new_brand = item.brand.strip()
        new_description = item.description.strip()
        new_category = item.category.strip()
        new_price = item.price
        new_quantity = item.quantity

        if not new_name:
            print("Skipped one product because name was empty after stripping.")
            continue

        if not new_brand:
            print(
                f"Skipped product '{new_name}' because brand was empty after stripping.")
            continue

        if not new_description:
            print(
                f"Skipped product '{new_name}' because description was empty after stripping.")
            continue

        if new_price is None or new_price <= 0:
            print(
                f"Skipped product '{new_name}' because price was invalid: {new_price}")
            continue

        if new_quantity is None or new_quantity < 0:
            print(
                f"Skipped product '{new_name}' because quantity was invalid: {new_quantity}")
            continue

        category_obj = get_create_category(new_category)

        product = Product(
            name=new_name,
            description=new_description,
            price=Decimal(str(new_price)),
            brand=new_brand,
            quantity=int(new_quantity),
            category=category_obj,
        )
        product.save()
        saved_count += 1

    return saved_count


# run the block only if file is executed directly
if __name__ == "__main__":
    validated_data = generate_products_with_gemini()
    export_product_to_json(validated_data)
    saved = save_products_to_week4(validated_data)
    print(f"\nSaved {saved} products into Week 4 MongoDB collection.")
