# this file creates the 4 langchain tools that the quote agent can call

from langchain_core.tools import tool
from week4.db_connection import initialize_mongo
from week4.repository import product_repository
from week7.semantic_search import semantic_search
from week9_10.config import DISCOUNT_TIERS, PRODUCT_SEARCH_TOP_K, PRODUCT_SEARCH_MODEL_NAME
from week9_10.policy import apply_policy_cap


initialize_mongo()


# helper function to create dict of products
def product_to_dict(product):
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "brand": product.brand,
        "price": float(product.price),
        "quantity": product.quantity,
        "category": product.category.title if product.category else None,
    }


# case 1 (manual .invoke() with the args)
# langchain runs the function body
# product_repository.get(1) actually hits mongoDB
# function returns the dict to langchain
# langChain returns the dict to us

# case 2 (LLM triggers call)
# LLM sees the user message + tool descriptions
# LLM outputs: "please call get_product_info with product_id=1" — this is a request, not a result
# LangChain reads that request and dispatches: get_product_info.invoke({"product_id": 1})
# LangChain runs the function body — same as case 1
# product_repository.get(1) actually hits MongoDB
# Function returns the dict to LangChain
# LangChain takes the dict and sends it to the LLM in the next API call as a "tool result"
# LLM uses that dict to decide what to do next (call another tool, or generate the final answer)


# when product id is not given
@tool
def find_product_by_query(query: str) -> list:
    """Search the inventory using semantic similarity and return top matches.

    Use this tool first when the user describes a product in natural language
    instead of giving a product ID. Returns the top candidates ranked by relevance.

    Args:
        query: A natural language description of the product (e.g. "building blocks",
            "gift for toddler", "Lego Castle").

    Returns:
        A list of product candidates. Each candidate contains id, name, brand, price,
        category, and semantic_score. Pick the most relevant one and use its id for
        further tool calls.
    """
    results = semantic_search(
        query=query,
        top_k=PRODUCT_SEARCH_TOP_K,
        model_name=PRODUCT_SEARCH_MODEL_NAME,
    )
    return results


@tool
def get_product_info(product_id: int) -> dict:
    """Get full details of a product by its integer ID.

    Args:
        product_id: The unique integer ID of the product.

    Returns:
        A dict with id, name, description, brand, price, quantity, and category.
        Returns an error dict if the product does not exist.
    """
    product = product_repository.get(product_id)
    if not product:
        return {"error": f"Product with id {product_id} not found."}
    return product_to_dict(product)


@tool
def check_inventory(product_id: int) -> dict:
    """Check the current stock level for a product.

    Use this tool to confirm availability before generating a quote.

    Args:
        product_id: The unique integer ID of the product.

    Returns:
        A dict with product_id, product_name, quantity_in_stock, and is_in_stock.
        Returns an error dict if the product does not exist.
    """
    product = product_repository.get(product_id)
    if not product:
        return {"error": f"Product with id {product_id} not found."}
    return {
        "product_id": product.id,
        "product_name": product.name,
        "quantity_in_stock": product.quantity,
        "is_in_stock": product.quantity > 0,
    }


@tool
def calculate_quote(product_id: int, quantity: int) -> dict:
    """Compute the final quote for a product and a requested quantity.

    Applies the tiered discount from the discount tier table, then runs the result
    through the policy guard which caps any rate above the maximum allowed discount.

    Args:
        product_id: The unique integer ID of the product.
        quantity: The number of units the customer wants to order. Must be at least 1.

    Returns:
        A dict with unit_price, subtotal, discount_rate, discount_label,
        discount_amount, total, and policy_warning (None when within policy).
        Returns an error dict if the product is missing or quantity is invalid.
    """
    if quantity < 1:
        return {"error": f"Quantity must be at least 1, got {quantity}."}

    product = product_repository.get(product_id)
    if not product:
        return {"error": f"Product with id {product_id} not found."}
    matched_tier = None
    for tier in DISCOUNT_TIERS:
        min_q = tier["min_qty"]
        max_q = tier["max_qty"]
        if quantity >= min_q and (max_q is None or quantity <= max_q):
            matched_tier = tier
            break

    if matched_tier is None:
        return {"error": f"No discount tier matches quantity {quantity}."}

    raw_rate = matched_tier["discount_rate"]
    label = matched_tier["label"]
    final_rate, policy_warning = apply_policy_cap(raw_rate)
    unit_price = float(product.price)
    subtotal = unit_price * quantity
    discount_amount = subtotal * final_rate
    total = subtotal - discount_amount
    return {
        "product_id": product.id,
        "product_name": product.name,
        "brand": product.brand,
        "quantity": quantity,
        "unit_price": unit_price,
        "subtotal": round(subtotal, 2),
        "discount_rate": final_rate,
        "discount_label": label,
        "discount_amount": round(discount_amount, 2),
        "total": round(total, 2),
        "policy_warning": policy_warning,
    }


if __name__ == "__main__":
    # tools are called using invoke, it is common in langchain although ig we can use directly get_product_info(1)
    print('-'*60)
    print("find_product_by_query")
    print('-'*60)
    print(find_product_by_query.invoke({"query": "building blocks"}))
    print()
    print('-'*60)
    print("get_product_info")
    print('-'*60)
    print(get_product_info.invoke({"product_id": 62}))
    print()
    print('-'*60)
    print("check_inventory")
    print('-'*60)
    print(check_inventory.invoke({"product_id": 62}))
    print()
    print('-'*60)
    print("calculate_quote (qty 60)")
    print('-'*60)
    print(calculate_quote.invoke({"product_id": 62, "quantity": 60}))
