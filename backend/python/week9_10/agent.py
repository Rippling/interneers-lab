# this file builds a langchain tool-calling agent backed by gemini
# the agent decides which tools to call based on the user's natural language request

from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from week9_10.langsimth_setup import setup_langsmith_tracing
from week9_10.config import AGENT_MAX_ITERATIONS
from week9_10.llm_client import get_chat_model
from week9_10.tools import (
    find_product_by_query,
    get_product_info,
    check_inventory,
    calculate_quote,
)

# create_tool_calling_agent : function that builds an agent from llm, list of tools, and prompt template. It returns an object that knows how to decide which tool to call next.
# AgentExecuter : runtime that actually executes the agent's decisions


setup_langsmith_tracing()


PROMPT = """You are an inventory quote assistant for a toy store.

Your job is to produce accurate price quotes for customers who describe what they want.

You have access to four tools:
- find_product_by_query: search inventory by natural language description, returns ranked candidates
- get_product_info: fetch full details by product ID
- check_inventory: fetch the current stock level for a product ID
- calculate_quote: compute the final price with discount and policy cap

Workflow:
1. If the user did not give a product ID, call find_product_by_query first to identify the product.
2. Call check_inventory to see the current stock level.
3. Determine the quantity to quote:
   - If the requested quantity is less than or equal to current stock, use the requested quantity.
   - If the requested quantity is greater than current stock, use the stock quantity instead.
4. Call calculate_quote with the chosen quantity.
5. Produce a clear final answer for the customer.

In the final answer always include:
- Product name and ID
- Requested quantity (what the customer asked for)
- Quoted quantity (the quantity calculate_quote was actually called with)
- Unit price and subtotal
- Discount rate, label, and amount (or note "no discount" if rate is 0%)
- Total price
- Stock available
- A clear stock_warning whenever the quoted quantity is less than the requested quantity.
  Explain that the quote was adjusted because stock is insufficient for the full request.
- A policy_warning whenever the calculate_quote result includes one.

Rules you must follow:
- If find_product_by_query returns multiple candidates, pick the most relevant one based on the user's intent.
- If a tool returns an error dict, retry with corrected arguments or ask the user to clarify.
- Never invent products, prices, or discounts. Use only values returned by the tools.
- Never call calculate_quote with a quantity greater than the available stock.
- Keep the final answer professional and easy to read.
"""


prompt = ChatPromptTemplate.from_messages([
    ("system", PROMPT),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])


agent_tools = [
    find_product_by_query,
    get_product_info,
    check_inventory,
    calculate_quote,
]


def build_quote_agent():
    llm = get_chat_model()
    agent = create_tool_calling_agent(llm, agent_tools, prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=agent_tools,
        max_iterations=AGENT_MAX_ITERATIONS,
        verbose=False,
        return_intermediate_steps=True,
    )
    return executor


def run_quote_agent(user_query: str):
    executor = build_quote_agent()
    result = executor.invoke({"input": user_query})
    # executor.invoke looks like
    # {
    #     "input": "I need 60 building block ....",
    #     "output": "Here is your quote: ....."
    #     "intermediate_steps": [
    #         "",
    #         "",
    #     ]
    # }
    return result


if __name__ == "__main__":
    query = "I need 60 building blocks for a school project, can I get a deal?"
    print(f"User query: {query}")
    print()

    result = run_quote_agent(query)

    print()
    print("=" * 60)
    print("Final answer:")
    print("=" * 60)
    print(result["output"])
    print()
    print("=" * 60)
    print("Intermediate steps (what the agent did):")
    print("=" * 60)
    for index, step in enumerate(result["intermediate_steps"], start=1):
        action, observation = step
        print(f"\nStep {index}:")
        print(f"  Tool called: {action.tool}")
        print(f"  Arguments:   {action.tool_input}")
        print(f"  Result:      {observation}")
