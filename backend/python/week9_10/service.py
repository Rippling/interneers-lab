# cleanup and packaging layer
# sits between agent and final result
import re
import json
from week9_10.schema import QuoteInvoiceSchema
from week9_10.agent import run_quote_agent


# gemini sometime returns [{"type":"text","text":""....}]
# this fnc will append all the readable part into a single string
def agent_output(raw_output):
    if isinstance(raw_output, str):
        return raw_output
    if isinstance(raw_output, list):
        parts = []
        for item in raw_output:
            if isinstance(item, dict) and "text" in item:
                parts.append(item["text"])
            elif isinstance(item, str):
                parts.append(item)
        return "".join(parts)
    return str(raw_output)


# figures out customer's originally requested quantity
#   1. "Requested Quantity: N" pattern in the agent's final text
#   2. first integer in the original user query
#   3. fallback (typically the quoted quantity = no adjustment)
def extract_req_quantity(answer_text, user_query, fallback):
    # first try that the agent write "Requested Quantity:60" in its final ans
    match = re.search(
        r"requested\s+quantity[\s\W]*(\d+)", answer_text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    # then write the first integer in the users natural langauge query
    match = re.search(r"\b(\d+)\b", user_query)
    if match:
        return int(match.group(1))
    return fallback


# func that goes through intermediate steps and pulls out quote and inventory results
def extract_quote_from_steps(intermediate_steps):
    quote_result = None
    stock_result = None
    for action, observation in intermediate_steps:
        if action.tool == "calculate_quote":
            quote_result = observation
        elif action.tool == "check_inventory":
            stock_result = observation
    return quote_result, stock_result


# main function that takes input and produces ans
def run_quote_service(user_query):
    # S-1 run the agent
    agent_result = run_quote_agent(user_query)
    # S-2 clean up gemini multi ouput into one string
    answer_text = agent_output(agent_result["output"])
    # S-3 extract results out of intermediate steps
    quote_result, stock_result = extract_quote_from_steps(
        agent_result["intermediate_steps"])
    # S-4 build structures invoice if a valid quote was produced
    invoice = None
    if quote_result and "error" not in quote_result:
        quoted_quantity = quote_result["quantity"]
        stock_available = stock_result["quantity_in_stock"] if stock_result else 0
        requested_quantity = extract_req_quantity(
            answer_text=answer_text, user_query=user_query, fallback=quoted_quantity)
        stock_warning = None
        if requested_quantity > quoted_quantity:
            stock_warning = (
                f"Requested {requested_quantity} units but only {stock_available} in stock. "
                f"Quote adjusted to {quoted_quantity} units."
            )
        # any invalid value will immediately raise validation error
        invoice = QuoteInvoiceSchema(
            product_id=quote_result["product_id"],
            product_name=quote_result["product_name"],
            brand=quote_result["brand"],
            requested_quantity=requested_quantity,
            quantity=quoted_quantity,
            unit_price=quote_result["unit_price"],
            subtotal=quote_result["subtotal"],
            discount_rate=quote_result["discount_rate"],
            discount_label=quote_result["discount_label"],
            discount_amount=quote_result["discount_amount"],
            total=quote_result["total"],
            stock_available=stock_available,
            stock_warning=stock_warning,
            policy_warning=quote_result.get("policy_warning"),
        )
    return {
        "query": user_query,
        "answer": answer_text,
        "invoice": invoice.model_dump() if invoice else None,
        "intermediate_steps": [
            {"tool": action.tool, "arguments": action.tool_input, "result": observation}
            for action, observation in agent_result["intermediate_steps"]
        ],
    }


if __name__ == "__main__":
    query = input("Enter your quote request: ").strip()
    if not query:
        print("No query entered.")
        exit(0)
    result = run_quote_service(query)
    print()
    print("=" * 60)
    print("CLEAN ANSWER TEXT:")
    print("=" * 60)
    print(result["answer"])
    print()
    print("=" * 60)
    print("JSON INVOICE :")
    print("=" * 60)
    print(json.dumps(result["invoice"], indent=2, default=str))
    print()
    print("=" * 60)
    print("TOOL CALL TRACE:")
    print("=" * 60)
    for index, step in enumerate(result["intermediate_steps"], start=1):
        print(f"Step {index}: {step['tool']}({step['arguments']})")
