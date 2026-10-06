import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from week4.db_connection import initialize_mongo
from week4.models import Product, ProductCategory
from week6.schema import ProductListSchema, FutureStockEventListSchema
from decimal import Decimal
from google import genai


load_dotenv()


initialize_mongo()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# page settings
st.set_page_config(
    page_title="Week 5 + Week 6 Inventory Dashboard", layout="wide")
st.title("Week 5 + Week 6: Interactive Data Tools")
st.write("Streamlit dashboard connected to MongoDB using MongoEngine and Gemini")


# helpers
def get_all_categories():
    return list(ProductCategory.objects().order_by("title"))


def fetch_products(selected_category_id=None):
    if selected_category_id is None:
        products = Product.objects()
    else:
        products = Product.objects(category=selected_category_id)

    rows = []

    for product in products:
        rows.append({
            "ID": product.id,
            "Name": product.name,
            "Description": product.description,
            "Price": float(product.price),
            "Brand": product.brand,
            "Quantity": product.quantity,
            "Category": product.category.title if product.category else "No Category"
        })

    return pd.DataFrame(rows)


def get_or_create_category(category_title):
    cat_title = (category_title or "").strip()

    if not cat_title:
        cat_title = "Miscellaneous"

    category = ProductCategory.objects(title=cat_title).first()
    if category:
        return category

    category = ProductCategory(
        title=cat_title,
        description=f"Auto-created from AI generated data for {cat_title}",
    )
    category.save()
    return category


def product_already_exists(name, brand):
    return Product.objects(name=name, brand=brand).first() is not None


def save_ai_products(validated_data):
    saved_count = 0
    skipped_count = 0

    for item in validated_data.products:
        name = item.name.strip()
        description = item.description.strip()
        category_title = item.category.strip()
        brand = item.brand.strip()
        price = item.price
        quantity = item.quantity

        if not name:
            skipped_count += 1
            continue

        if not description:
            skipped_count += 1
            continue

        if not brand:
            skipped_count += 1
            continue

        if price is None or price <= 0:
            skipped_count += 1
            continue

        if quantity is None or quantity < 0:
            skipped_count += 1
            continue

        if product_already_exists(name, brand):
            skipped_count += 1
            continue

        category_obj = get_or_create_category(category_title)

        product = Product(
            name=name,
            description=description,
            price=Decimal(str(price)),
            brand=brand,
            quantity=int(quantity),
            category=category_obj,
        ).save()
        saved_count += 1

    return saved_count, skipped_count


def generate_products_from_ai(product_count=10, theme="general toy store"):
    prompt = f"""
Generate exactly {product_count} products for a toy store.

Theme: {theme}

Return valid JSON only in this structure:
{{
  "products": [
    {{
      "name": "string",
      "description": "string",
      "category": "string",
      "brand": "string",
      "price": 10.99,
      "quantity": 25
    }}
  ]
}}

Rules:
- Include exactly {product_count} products
- Product name must never be empty
- Brand must never be empty
- Description must never be empty
- Category must never be empty
- Use realistic toy store categories
- Match the requested theme where possible
- price must be a float greater than or equal to 0.01
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
        },
    )

    validated = ProductListSchema.model_validate_json(response.text)
    return validated, response.text


def generate_future_events(event_count=5, theme="general toy store"):
    prompt = f"""
Generate exactly {event_count} future stock events for a toy store.

Theme: {theme}

Return valid JSON only in this structure:
{{
  "events": [
    {{
      "title": "string",
      "event_type": "string",
      "expected_date": "YYYY-MM-DD",
      "product_name": "string",
      "quantity_change": 10,
      "note": "string"
    }}
  ]
}}

Rules:
- Include exactly {event_count} events
- All dates must be future dates
- Keep events realistic for toy inventory
- Match the requested theme where possible
- event_type can be: incoming_shipment, seasonal_spike, low_stock_warning, preorder_arrival, supplier_delay, warehouse_transfer
- title must not be empty
- product_name must not be empty
- quantity_change must be an integer
- output valid JSON only
- do not include markdown
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "temperature": 0.6,
            "response_mime_type": "application/json",
            "response_schema": FutureStockEventListSchema,
        },
    )

    validated_data = FutureStockEventListSchema.model_validate_json(
        response.text)
    return validated_data, response.text


# creating sidebar category filter

st.sidebar.header("Filter Inventory")

all_category = get_all_categories()
# creating dictionary where all maps to none so that no conflict arises
category_options = {"All": None}

for category in all_category:
    category_options[category.title] = category.id

selected_category_title = st.sidebar.selectbox(
    "Select Product Category", list(category_options.keys()))

selected_category_id = category_options[selected_category_title]


# showing inventory table for current id

@st.fragment
def inventory_table(category_id):
    st.subheader("Current Inventory")
    df = fetch_products(category_id)
    if df.empty:
        st.info("No products found in this category")
    else:
        st.dataframe(df, use_container_width=True)
    return df


# showing stock alert

@st.fragment
def stock_alert(df):
    st.subheader("Stock Alert")
    if not df.empty:
        low_stock_row = []
        for index, row in df.iterrows():
            if row["Quantity"] < 5:
                low_stock_row.append(row)
        low_stock_df = pd.DataFrame(low_stock_row)

        if not low_stock_df.empty:
            st.error("Some products are running low in stock")
            st.dataframe(low_stock_df, use_container_width=True)
        else:
            st.success("No products are running low in stock")
    else:
        st.info("No products found in this category")


# adding product

@st.fragment
def add_product(categories):
    st.subheader("Add Product")
    category_title = []
    for category in categories:
        category_title.append(category.title)

    with st.form("add_product_form"):
        new_name = st.text_input("Name")
        new_description = st.text_area("Description")
        new_price = st.number_input(
            "Price", min_value=0.0, step=1.0, format="%.2f")
        new_brand = st.text_input("Brand")
        new_quantity = st.number_input(
            "Quantity", min_value=0, step=1)
        if category_title:
            new_category_title = st.selectbox("Category", category_title)
        else:
            new_category_title = None
            st.warning("No categories found. Please create a category first.")
        submitted = st.form_submit_button("Add Product")

    if submitted:
        if not new_name.strip():
            st.error("Product name cannot be empty")
        elif not new_description.strip():
            st.error("Description cannot be empty")
        elif not new_brand.strip():
            st.error("Brand cannot be empty")
        elif not new_category_title:
            st.error("No category exist. Pls create a category first in week 4")
        else:
            selected_category = ProductCategory.objects(
                title=new_category_title).first()
            Product(name=new_name, description=new_description,
                    price=Decimal(str(new_price)), brand=new_brand, quantity=int(new_quantity), category=selected_category).save()
            st.success(f"Product '{new_name}' added successfully")


# removing product

@st.fragment
def remove_product():
    st.subheader("Remove Product")
    all_products = Product.objects().order_by("name")
    product_options = {}
    for product in all_products:
        label = f"{product.name} (ID: {product.id})"
        product_options[label] = product.id

    if product_options:
        selected_product_label = st.selectbox(
            "Select Product to remove", list(product_options.keys()))
        if st.button("Remove Product"):
            selected_product_id = product_options[selected_product_label]
            Product.objects(id=selected_product_id).delete()
            st.success("Product removed successfully")
    else:
        st.info("No products found")


# AI generator

@st.fragment
def ai_scenario_generator():
    st.subheader("Week 6 Advanced: AI Scenario Generator")

    scenario_options = [
        "Holiday Rush",
        "Summer Sale",
        "Back to School",
        "New Year Restock",
        "Outdoor Play Season",
        "Educational Toys Campaign",
    ]

    selected_scenario = st.selectbox("Choose Scenario", scenario_options)

    product_count = st.number_input(
        "How many products to generate?",
        min_value=1,
        max_value=50,
        value=10,
        step=1,
    )

    event_count = st.number_input(
        "How many future events to generate?",
        min_value=1,
        max_value=20,
        value=5,
        step=1,
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate AI Products"):
            validated_products, raw_product_json = generate_products_from_ai(
                product_count=product_count,
                theme=selected_scenario,
            )

            saved_count, skipped_count = save_ai_products(validated_products)

            st.success(f"{saved_count} AI products saved successfully")

            if skipped_count > 0:
                st.warning(f"{skipped_count} products were skipped")

            st.text_area("Generated Product JSON",
                         raw_product_json, height=300)

    with col2:
        if st.button("Generate Future Events"):
            validated_events, raw_event_json = generate_future_events(
                event_count=event_count,
                theme=selected_scenario,
            )

            st.success(
                f"{len(validated_events.events)} future events generated successfully")
            st.text_area("Generated Event JSON", raw_event_json, height=300)


df = inventory_table(selected_category_id)
stock_alert(df)
ai_scenario_generator()
add_product(all_category)
remove_product()
