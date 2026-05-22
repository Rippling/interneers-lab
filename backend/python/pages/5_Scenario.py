# pages/5_Scenario.py

import streamlit as st
import sys
import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db_connection import connect_to_mongodb
connect_to_mongodb()

from products.models import Product
from products.category_model import ProductCategory

st.set_page_config(page_title="AI Scenario Selector", page_icon="🎯", layout="wide")

def get_all_categories():
    return list(ProductCategory.objects.all())

# ─── PAGE ──────────────────────────────────────────────────────
st.title("🎯 AI Scenario Selector")
st.markdown("Choose a warehouse scenario and let AI populate the database with relevant products!")
st.markdown("---")

SCENARIOS = {
    "🎄 Holiday Rush": {
        "description": "Festive season — high demand for gifts, decorations, and party items",
        "stock_min": 300,
        "stock_max": 500,
        "prompt_hint": "festive holiday season products like gifts, decorations, party supplies, winter clothing, and electronics",
        "color": "#2d4a2d"
    },
    "☀️ Summer Collection": {
        "description": "Summer season — outdoor, cooling, and seasonal products",
        "stock_min": 200,
        "stock_max": 400,
        "prompt_hint": "summer season products like light clothing, outdoor gear, cooling appliances, summer foods and beverages",
        "color": "#4a3d1a"
    },
    "📚 Back to School": {
        "description": "School season — stationery, books, electronics, and essentials",
        "stock_min": 150,
        "stock_max": 350,
        "prompt_hint": "back to school products like books, stationery, bags, electronics like laptops and calculators, and school essentials",
        "color": "#1a2d4a"
    },
    "🎆 New Year Sale": {
        "description": "New Year — discounted items, party supplies, and fresh start products",
        "stock_min": 250,
        "stock_max": 450,
        "prompt_hint": "new year sale products like party supplies, fitness equipment, kitchen appliances, and lifestyle products",
        "color": "#3d1a4a"
    },
}

# ── Initialize selected scenario in session state ───────────────
if "selected_scenario" not in st.session_state:
    st.session_state.selected_scenario = None

# ── Render scenario cards ───────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
cols = [col1, col2, col3, col4]

for i, (scenario_name, scenario_data) in enumerate(SCENARIOS.items()):
    with cols[i]:
        is_selected = st.session_state.selected_scenario == scenario_name
        border_color = "#ff4b4b" if is_selected else "#333333"
        bg_color = scenario_data["color"] if is_selected else "#1a1a1a"

        st.markdown(f"""
<div style="
    border: 2px solid {border_color};
    border-radius: 12px;
    padding: 20px;
    background-color: {bg_color};
    min-height: 160px;
    margin-bottom: 10px;
">
    <h3 style="margin: 0 0 8px 0; font-size: 18px;">{scenario_name}</h3>
    <p style="margin: 0; font-size: 13px; color: #cccccc;">{scenario_data['description']}</p>
    <p style="margin: 8px 0 0 0; font-size: 12px; color: #aaaaaa;">
        Stock: {scenario_data['stock_min']}–{scenario_data['stock_max']} units
    </p>
</div>
""", unsafe_allow_html=True)

        btn_label = "✅ Selected" if is_selected else "Select"
        if st.button(btn_label, key=f"scenario_{i}", use_container_width=True):
            st.session_state.selected_scenario = scenario_name
            st.rerun()

# ── Show number input + generate button if scenario selected ────
if st.session_state.selected_scenario:
    scenario_info = SCENARIOS[st.session_state.selected_scenario]
    st.markdown("---")
    st.markdown(f"**Selected:** {st.session_state.selected_scenario} — {scenario_info['description']}")

    num_products = st.number_input(
        "How many products to generate?",
        min_value=1,
        max_value=50,
        value=10,
        step=1,
        key="num_products_input"
    )

    if st.button("🚀 Generate & Save Products", type="primary"):
        try:
            from groq import Groq
            from pydantic import BaseModel, field_validator
            from typing import Optional
            from datetime import datetime, timezone

            client = Groq(api_key=os.getenv("GROQ_API_KEY"))

            all_categories = get_all_categories()
            category_map = {cat.title: cat for cat in all_categories}
            category_names = list(category_map.keys())

            selected_scenario = st.session_state.selected_scenario

            prompt = f"""
Generate exactly {num_products} realistic warehouse products for a "{selected_scenario.replace('🎄 ', '').replace('☀️ ', '').replace('📚 ', '').replace('🎆 ', '')}" scenario as a JSON array.
Focus on: {scenario_info['prompt_hint']}
Each product must belong to one of these categories only: {category_names}
Each product must have exactly these fields:
- name: string
- description: string (1-2 sentences)
- category: string (must be exactly one of: {category_names})
- price: float (min 0.01)
- brand: string
- quantity_in_warehouse: integer (between {scenario_info['stock_min']} and {scenario_info['stock_max']})
Rules: Return ONLY a valid JSON array, no explanation, no markdown, no extra text
"""

            with st.spinner("🤖 AI is generating products..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )

            raw_output = response.choices[0].message.content
            cleaned = raw_output.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            products_data = json.loads(cleaned)

            class ProductSchema(BaseModel):
                name: str
                description: Optional[str] = ""
                category: str
                price: float
                brand: str
                quantity_in_warehouse: int

                @field_validator('price')
                def price_must_be_positive(cls, v):
                    if v <= 0:
                        raise ValueError("Price must be greater than 0")
                    return round(v, 2)

                @field_validator('quantity_in_warehouse')
                def quantity_must_be_non_negative(cls, v):
                    if v < 0:
                        raise ValueError("Quantity cannot be negative")
                    return v

                @field_validator('category')
                def category_must_exist(cls, v):
                    if v not in category_names:
                        raise ValueError(f"Invalid category: {v}")
                    return v

            valid_products = []
            invalid_count = 0

            for product in products_data:
                try:
                    validated = ProductSchema(**product)
                    valid_products.append(validated)
                except Exception:
                    invalid_count += 1

            saved = 0
            now = datetime.now(timezone.utc)

            for vp in valid_products:
                try:
                    category_obj = category_map.get(vp.category)
                    if not category_obj:
                        continue
                    Product(
                        name=vp.name,
                        description=vp.description,
                        category=category_obj,
                        price=vp.price,
                        brand=vp.brand,
                        quantity_in_warehouse=vp.quantity_in_warehouse,
                        created_at=now,
                        updated_at=now
                    ).save()
                    saved += 1
                except Exception:
                    invalid_count += 1

            st.success(f"🎉 Successfully saved {saved} products for '{st.session_state.selected_scenario}' scenario!")
            if invalid_count > 0:
                st.warning(f"⚠️ {invalid_count} products were skipped due to validation errors.")

            import pandas as pd
            preview_data = [{"Name": vp.name, "Category": vp.category, "Brand": vp.brand,
                             "Price (₹)": vp.price, "Stock": vp.quantity_in_warehouse}
                            for vp in valid_products]
            st.dataframe(pd.DataFrame(preview_data), use_container_width=True, hide_index=True)
            st.info("🔄 Go to Home page to see updated inventory!")

        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")
else:
    st.info("👆 Select a scenario above to get started!")