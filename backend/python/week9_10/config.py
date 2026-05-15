# central setting file for week 9/10
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
GEMINI_MODEL_NAME = "gemini-2.5-flash"
GEMINI_TEMPERATURE = 0.2
TRACING_PROJECT_NAME = "interneers-lab-week9-10"
# discounts for different cases
DISCOUNT_TIERS = [
    {"min_qty": 1,   "max_qty": 19,   "discount_rate": 0.00, "label": "no discount"},
    {"min_qty": 20,  "max_qty": 49,   "discount_rate": 0.05,
        "label": "5% bulk discount"},
    {"min_qty": 50,  "max_qty": 99,   "discount_rate": 0.10,
        "label": "10% bulk discount"},
    {"min_qty": 100, "max_qty": None, "discount_rate": 0.15,
        "label": "15% bulk discount"},
]
# as given in adv task, max discount should be less than 20 percent
MAX_DISCOUNT_RATE = 0.20
# if the agent keeps calling tools then we can get some timeout errors
AGENT_MAX_ITERATIONS = 6
PRODUCT_SEARCH_TOP_K = 3
PRODUCT_SEARCH_MODEL_NAME = "all-MiniLM-L6-v2"
