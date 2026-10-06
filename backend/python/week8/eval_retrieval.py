# this is for task 3c
# it just checks whether retrieval is actually returning the correct source document or not
from week8.retriever import retrieve_relavant_chunks
from week8.config import DEFAULT_TOP_K


RETRIEVAL_TEST_CASES = [
    {
        "query": "What's the return policy for damaged items?",
        "expected_source": "return_policy.txt",
    },
    {
        "query": "What is the warranty period for Coding Robot for Kids?",
        "expected_source": "product_manual.txt",
    },
    {
        "query": "Can vendors provide replacement parts for missing components?",
        "expected_source": "vendor_faq.txt",
    },
    {
        "query": "If a swing set part gets damaged after weather exposure, is it covered?",
        "expected_source": "return_policy.txt",
    },
    {
        "query": "Why do educational kits and remote-control toys sometimes take longer to restock?",
        "expected_source": "vendor_faq.txt",
    },
]


def evaluate_retrieval(top_k: int = DEFAULT_TOP_K):
    results_summary = []
    for test_case in RETRIEVAL_TEST_CASES:
        query = test_case["query"]
        expected_source = test_case["expected_source"]
        retrieved_chunks = retrieve_relavant_chunks(query, top_k=top_k)
        retrieved_sources = [chunk["source"] for chunk in retrieved_chunks]
        is_match = False
        if expected_source in retrieved_sources:
            is_match = True
        results_summary.append(
            {
                "query": query,
                "expected_source": expected_source,
                "retrieved_sources": retrieved_sources,
                "match_found": is_match,
            }
        )
    return results_summary


if __name__ == "__main__":
    evaluation_results = evaluate_retrieval(top_k=DEFAULT_TOP_K)
    correct_matches = 0
    print("Retrieval Evaluation Results\n")

    for index, result in enumerate(evaluation_results, start=1):
        print("=" * 100)
        print(f"Test Case #{index}")
        print(f"Query: {result['query']}")
        print(f"Expected Source: {result['expected_source']}")
        print(f"Retrieved Sources: {result['retrieved_sources']}")
        print(f"Match Found: {result['match_found']}")

        if result["match_found"]:
            correct_matches += 1

    total_cases = len(evaluation_results)
    accuracy = correct_matches / total_cases if total_cases else 0

    print("\n" + "=" * 100)
    print(f"Total Test Cases: {total_cases}")
    print(f"Correct Matches: {correct_matches}")
    print(f"Retrieval Accuracy: {accuracy:.2f}")
