# pages/4_Quote_Agent.py

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

st.set_page_config(page_title="Quote Agent", page_icon="💰", layout="wide")

# ── Quote Agent Functions ───────────────────────────────────────
def find_product(product_name: str):
    product = Product.objects(name__icontains=product_name).first()
    if product:
        return product
    product = Product.objects(name__icontains=product_name[:-1]).first()
    if product:
        return product
    first_word = product_name.split()[0]
    product = Product.objects(name__icontains=first_word).first()
    return product

def get_product_info(product_name: str) -> dict:
    product = find_product(product_name)
    if not product:
        return {"error": f"Product '{product_name}' not found"}
    try:
        category = product.category.title if product.category else "Unknown"
    except:
        category = "Unknown"
    return {
        "product_id": str(product.id),
        "name": product.name,
        "brand": product.brand,
        "category": category,
        "price": float(str(product.price)),
        "description": product.description
    }

def check_inventory(product_name: str) -> dict:
    product = find_product(product_name)
    if not product:
        return {"error": f"Product '{product_name}' not found"}
    stock = product.quantity_in_warehouse
    if stock == 0:
        status = "OUT OF STOCK"
    elif stock < 10:
        status = "LOW STOCK"
    elif stock < 50:
        status = "IN STOCK"
    else:
        status = "WELL STOCKED"
    return {
        "product_id": str(product.id),
        "name": product.name,
        "stock": stock,
        "status": status,
        "can_fulfill": stock > 0
    }

def calculate_quote(product_name: str, quantity: int) -> dict:
    MAX_DISCOUNT = 20.0
    product = find_product(product_name)
    if not product:
        return {"error": f"Product '{product_name}' not found"}
    stock = product.quantity_in_warehouse
    if stock < quantity:
        return {"error": f"Insufficient stock. Requested: {quantity}, Available: {stock}"}
    unit_price = float(str(product.price))
    if quantity <= 10:
        discount_pct = 0
        discount_reason = "No discount for small orders"
    elif quantity <= 50:
        discount_pct = 10
        discount_reason = "10% bulk discount for orders of 11-50 units"
    else:
        discount_pct = MAX_DISCOUNT
        discount_reason = "20% bulk discount for orders of 51+ units"
    original_total = unit_price * quantity
    discount_amount = original_total * (discount_pct / 100)
    final_total = original_total - discount_amount
    return {
        "product_name": product.name,
        "brand": product.brand,
        "quantity": quantity,
        "unit_price": round(unit_price, 2),
        "discount_percentage": discount_pct,
        "discount_reason": discount_reason,
        "original_total": round(original_total, 2),
        "discount_amount": round(discount_amount, 2),
        "final_total": round(final_total, 2),
        "currency": "INR",
        "policy_override": False
    }

def confirm_order(product_name: str, quantity: int) -> dict:
    from datetime import datetime, timezone
    product = find_product(product_name)
    if not product:
        return {"error": f"Product '{product_name}' not found"}
    current_stock = product.quantity_in_warehouse
    if current_stock < quantity:
        return {"error": f"Insufficient stock. Available: {current_stock}, Requested: {quantity}"}
    product.quantity_in_warehouse = current_stock - quantity
    product.updated_at = datetime.now(timezone.utc)
    product.save()
    unit_price = float(str(product.price))
    if quantity <= 10:
        discount_pct = 0
    elif quantity <= 50:
        discount_pct = 10
    else:
        discount_pct = 20
    original_total = unit_price * quantity
    discount_amount = original_total * (discount_pct / 100)
    final_total = original_total - discount_amount
    return {
        "success": True,
        "order_id": f"ORD-{str(product.id)[-6:].upper()}-{quantity}",
        "product_name": product.name,
        "brand": product.brand,
        "quantity": quantity,
        "unit_price": round(unit_price, 2),
        "discount_percentage": discount_pct,
        "discount_amount": round(discount_amount, 2),
        "original_total": round(original_total, 2),
        "final_total": round(final_total, 2),
        "stock_before": current_stock,
        "stock_after": product.quantity_in_warehouse,
        "order_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    }

QUOTE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_product_info",
            "description": "Get product details like price, brand, and category from inventory",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string", "description": "The name or partial name of the product"}
                },
                "required": ["product_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_inventory",
            "description": "Check how many units of a product are currently in stock",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string", "description": "The name of the product to check inventory for"}
                },
                "required": ["product_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_quote",
            "description": "Calculate total price quote with bulk discounts applied",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string", "description": "The name of the product"},
                    "quantity": {"type": "integer", "description": "The number of units requested"}
                },
                "required": ["product_name", "quantity"]
            }
        }
    }
]

QUOTE_TOOL_MAP = {
    "get_product_info": get_product_info,
    "check_inventory": check_inventory,
    "calculate_quote": calculate_quote
}

def run_quote_agent_dashboard(user_request: str) -> tuple:
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    messages = [
        {
            "role": "system",
            "content": """You are a Quote Agent for a product inventory system.
When a user asks for a product quote, you must:
1. Find the product using get_product_info
2. Check stock using check_inventory
3. Calculate the quote using calculate_quote
4. Return a clear, friendly quote summary with all pricing details

Always use all 3 tools before giving final answer.
Mention discount if applicable. Be friendly and professional."""
        },
        {"role": "user", "content": user_request}
    ]

    tool_log = []
    step = 1
    max_retries = 3

    while True:
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    tools=QUOTE_TOOLS,
                    tool_choice="auto"
                )
                break
            except Exception as e:
                if "tool_use_failed" in str(e) and attempt < max_retries - 1:
                    continue
                else:
                    return f"Error: {str(e)}", tool_log

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content, tool_log

        messages.append(message)

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            tool_result = QUOTE_TOOL_MAP[tool_name](**tool_args)

            tool_log.append({
                "tool": tool_name,
                "args": tool_args,
                "result": tool_result
            })

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result)
            })

        step += 1
        if step > 10:
            return "Agent exceeded maximum steps", tool_log

# ─── PAGE ──────────────────────────────────────────────────────
st.title("💰 AI Quote Agent")
st.markdown("Get instant quotes for any product — with automatic bulk discounts!")
st.markdown("---")

if "quote_history" not in st.session_state:
    st.session_state.quote_history = []

if "pending_order" not in st.session_state:
    st.session_state.pending_order = None

col1, col2, col3 = st.columns(3)
with col1:
    st.info("📦 1-10 units → No discount")
with col2:
    st.info("📦 11-50 units → 10% off")
with col3:
    st.info("📦 51+ units → 20% off (max)")

for chat in st.session_state.quote_history:
    with st.chat_message("user"):
        st.write(chat["question"])
    with st.chat_message("assistant"):
        st.write(chat["answer"])
        with st.expander("🔧 Tools called by Agent"):
            for log in chat["tool_log"]:
                st.caption(f"🔧 {log['tool']}({log['args']})")
                st.caption(f"📤 Result: {log['result']}")
                st.markdown("---")
        if chat.get("receipt"):
            r = chat["receipt"]
            st.success("✅ Order Confirmed!")
            st.markdown(f"""
**🧾 Order Receipt**
| Field | Details |
|-------|---------|
| **Order ID** | `{r['order_id']}` |
| **Product** | {r['product_name']} ({r['brand']}) |
| **Quantity** | {r['quantity']} units |
| **Unit Price** | ₹{r['unit_price']} |
| **Discount** | {r['discount_percentage']}% (saved ₹{r['discount_amount']}) |
| **Total Paid** | ₹{r['final_total']} |
| **Stock Update** | {r['stock_before']} → {r['stock_after']} units remaining |
| **Order Time** | {r['order_time']} |
""")

quote_question = st.text_input(
    "Ask for a quote",
    placeholder="e.g. 'I need 60 Coffee Makers, any deal?'",
    key="quote_input"
)
get_quote_btn = st.button("🤖 Get Quote", type="primary")

if get_quote_btn and quote_question:
    with st.chat_message("user"):
        st.write(quote_question)
    with st.chat_message("assistant"):
        with st.spinner("🤖 Agent is working on your quote..."):
            try:
                answer, tool_log = run_quote_agent_dashboard(quote_question)
                st.write(answer)
                with st.expander("🔧 Tools called by Agent"):
                    for log in tool_log:
                        st.caption(f"🔧 {log['tool']}({log['args']})")
                        st.caption(f"📤 Result: {log['result']}")
                        st.markdown("---")

                product_name = None
                quantity = None
                for log in tool_log:
                    if log["tool"] == "calculate_quote" and "error" not in log["result"]:
                        product_name = log["result"].get("product_name")
                        quantity = log["result"].get("quantity")

                st.session_state.quote_history.append({
                    "question": quote_question,
                    "answer": answer,
                    "tool_log": tool_log,
                    "receipt": None
                })

                if product_name and quantity:
                    st.session_state.pending_order = {
                        "product_name": product_name,
                        "quantity": quantity,
                        "history_index": len(st.session_state.quote_history) - 1
                    }

            except Exception as e:
                st.error(f"❌ Error: {e}")

if st.session_state.pending_order:
    order = st.session_state.pending_order
    st.markdown("---")
    st.markdown(f"### 🛒 Ready to place this order?")
    st.markdown(f"**{order['quantity']} x {order['product_name']}**")

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("✅ Confirm Order", type="primary", key="confirm_order_btn"):
            with st.spinner("⏳ Processing order..."):
                receipt = confirm_order(order["product_name"], order["quantity"])
                if "error" in receipt:
                    st.error(f"❌ Order failed: {receipt['error']}")
                else:
                    idx = order["history_index"]
                    st.session_state.quote_history[idx]["receipt"] = receipt
                    st.session_state.pending_order = None
                    st.success("🎉 Order confirmed! Inventory updated.")
                    st.rerun()
    with col2:
        if st.button("❌ Cancel", key="cancel_order_btn"):
            st.session_state.pending_order = None
            st.rerun()

if st.session_state.quote_history:
    if st.button("🗑️ Clear Quote History", key="clear_quote"):
        st.session_state.quote_history = []
        st.session_state.pending_order = None
        st.rerun()

st.caption("💡 Discount rules: 1-10 units = 0%, 11-50 units = 10%, 51+ units = 20% (max allowed by policy)")