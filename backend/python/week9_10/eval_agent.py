from week9_10.service import run_quote_service
from week9_10.policy import is_within_policy

EVAL_TEST_CASES = [
    # SIMPLE SCENARIOS - clean inputs, expected smooth flow
    {
        "name": "simple_tier1_no_discount",
        "query": "I want a quote for 5 building blocks",
        "expected_tools": ["find_product_by_query", "check_inventory", "calculate_quote"],
        "expected_discount": 0.00,
        "expected_quantity": 5,
        "expected_keywords": ["building blocks"],
        "should_have_invoice": True,
        "should_have_stock_warning": False,
    },
    {
        "name": "simple_tier2_five_percent",
        "query": "Can I get pricing for 25 building blocks?",
        "expected_tools": ["find_product_by_query", "check_inventory", "calculate_quote"],
        "expected_discount": 0.05,
        "expected_quantity": 25,
        "expected_keywords": ["building blocks", "5%"],
        "should_have_invoice": True,
        "should_have_stock_warning": False,
    },
    {
        "name": "simple_tier3_ten_percent_spec_example",
        "query": "I need 60 building blocks for a school project",
        "expected_tools": ["find_product_by_query", "check_inventory", "calculate_quote"],
        "expected_discount": 0.10,
        "expected_quantity": None,  # depends on stock, allow either 60 or capped
        "expected_keywords": ["building blocks", "10%"],
        "should_have_invoice": True,
        "should_have_stock_warning": None,  # unknown without knowing stock
    },
    {
        "name": "simple_tier4_fifteen_percent",
        "query": "Quote for 120 building blocks please",
        "expected_tools": ["find_product_by_query", "check_inventory", "calculate_quote"],
        "expected_discount": 0.15,
        "expected_quantity": None,  # may be capped by stock
        "expected_keywords": ["building blocks", "15%"],
        "should_have_invoice": True,
        "should_have_stock_warning": None,
    },
    {
        "name": "simple_tier2_alternate_phrasing",
        "query": "How much would 30 lego cost?",
        "expected_tools": ["find_product_by_query", "check_inventory", "calculate_quote"],
        "expected_discount": 0.05,
        "expected_quantity": 30,
        "expected_keywords": ["5%"],
        "should_have_invoice": True,
        "should_have_stock_warning": False,
    },

    # COMPLEX SCENARIOS - edge cases that stress the agent
    {
        "name": "complex_quantity_above_stock",
        "query": "I need 9999 building blocks",
        "expected_tools": ["find_product_by_query", "check_inventory", "calculate_quote"],
        "expected_discount": None,  # tier depends on the capped quantity
        "expected_quantity": None,  # whatever stock currently is
        "expected_keywords": ["stock"],  # answer should mention stock issue
        "should_have_invoice": True,
        "should_have_stock_warning": True,  # this is the key check
    },
    {
        "name": "complex_boundary_exactly_50",
        "query": "I want a quote for exactly 50 building blocks",
        "expected_tools": ["find_product_by_query", "check_inventory", "calculate_quote"],
        "expected_discount": 0.10,  # 50 falls in 50-99 tier
        "expected_quantity": None,  # may equal stock if stock=50
        "expected_keywords": ["10%"],
        "should_have_invoice": True,
        "should_have_stock_warning": None,
    },
    {
        "name": "complex_non_existent_product",
        "query": "I need 20 spaceships from Mars please",
        # at minimum, search must run
        "expected_tools": ["find_product_by_query"],
        "expected_discount": None,
        "expected_quantity": None,
        "expected_keywords": [],  # we don't enforce wording on graceful failures
        "should_have_invoice": False,  # no real product = no invoice
        "should_have_stock_warning": None,
    },
]


def evaluate_case(case):
    query = case["query"]
    result = run_quote_service(query)
    invoice = result["invoice"]
    answer = result["answer"]
    tools_called = [step["tool"] for step in result["intermediate_steps"]]
    checks = {}

    # check 1 : were the expected tools called ?
    expected_tools = set(case["expected_tools"])
    tools_called_set = set(tools_called)
    checks["expected_tools_called"] = expected_tools.issubset(tools_called_set)

    # check 2 : is invoive matching expectation ?
    has_invoice = invoice is not None
    checks["invoice_presence"] = has_invoice == case["should_have_invoice"]

    # check 3 : discount rates
    if invoice and case["expected_discount"] is not None:
        checks["discount_rate"] = invoice["discount_rate"] == case["expected_discount"]
    else:
        checks["discount_rate"] = True

    # check 4 : quoted quantity
    if invoice and case["expected_quantity"] is not None:
        checks["quoted_quantity"] = invoice["quantity"] == case["expected_quantity"]
    else:
        checks["quoted_quantity"] = True

    # check 5 : expected keywork appears in answer text
    answer_lower = answer.lower()
    missing_keywords = [kw for kw in case["expected_keywords"]
                        if kw.lower() not in answer_lower]
    checks["expected_keywords"] = len(missing_keywords) == 0

    # check 6 : stock warning
    if invoice and case["should_have_stock_warning"] is not None:
        has_stock_warning = invoice.get("stock_warning") is not None
        checks["stock_warning"] = has_stock_warning == case["should_have_stock_warning"]
    else:
        checks["stock_warning"] = True

    # check 7 : policy should never be violated
    if invoice:
        checks["policy_within_bounds"] = is_within_policy(
            invoice["discount_rate"])
    else:
        checks["policy_within_bounds"] = True  # skipped

    overall_passed = all(checks.values())

    return {
        "name": case["name"],
        "query": query,
        "checks": checks,
        "missing_keywords": missing_keywords if not checks["expected_keywords"] else [],
        "tools_called": tools_called,
        "discount_rate": invoice["discount_rate"] if invoice else None,
        "quoted_quantity": invoice["quantity"] if invoice else None,
        "stock_warning": invoice.get("stock_warning") if invoice else None,
        "overall_passed": overall_passed,
    }


def run_eval_suite():
    print("=" * 80)
    print("AI QUOTE AGENT - EVAL SUITE")
    print("=" * 80)

    results = []
    for case in EVAL_TEST_CASES:
        print(f"\nRunning: {case['name']}")
        print(f"  Query: {case['query']}")
        try:
            result = evaluate_case(case)
        except Exception as e:
            print(f"  ERROR during evaluation: {e}")
            result = {
                "name": case["name"],
                "query": case["query"],
                "checks": {},
                "overall_passed": False,
                "error": str(e),
            }
        results.append(result)

        status = "PASS" if result["overall_passed"] else "FAIL"
        print(f"  Status: {status}")
        if not result["overall_passed"]:
            failed_checks = [k for k, v in result["checks"].items() if not v]
            print(f"  Failed checks: {failed_checks}")
            if result.get("missing_keywords"):
                print(f"  Missing keywords: {result['missing_keywords']}")
            print(f"  Tools called: {result.get('tools_called')}")
            print(f"  Discount rate: {result.get('discount_rate')}")
            print(f"  Quoted quantity: {result.get('quoted_quantity')}")
            print(f"  Stock warning: {result.get('stock_warning')}")

    # summary
    total = len(results)
    passed = sum(1 for r in results if r["overall_passed"])
    score = passed / total if total else 0

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total cases: {total}")
    print(f"Passed:      {passed}")
    print(f"Failed:      {total - passed}")
    print(f"Score:       {score:.2%}")

    return results


if __name__ == "__main__":
    run_eval_suite()
