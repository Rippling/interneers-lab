# this file checks whether the ans behaves sensibly end to end
from week8.rag_pipeline import run_rag_pipeline
from week8.config import DEFAULT_TOP_K


RAG_TEST_CASES = [
    {
        "query": "What's the return policy for damaged items?",
        "expected_keywords": ["damaged", "replacement", "refund"],
    },
    {
        "query": "What is the warranty period for Coding Robot for Kids?",
        "expected_keywords": ["12-month", "warranty"],
    },
    {
        "query": "Can vendors provide replacement parts for missing components?",
        "expected_keywords": ["replacement parts", "vendors", "components"],
    },
    {
        "query": "If I use the wrong batteries and my toy stops working, is that covered?",
        "expected_keywords": ["battery", "not covered"],
    },
    {
        "query": "Why do educational kits take longer to restock sometimes?",
        "expected_keywords": ["lead times", "educational", "restock"],
    },
]


def evaluate_rag(top_k: int = DEFAULT_TOP_K):
    results_summary = []
    for test_case in RAG_TEST_CASES:
        query = test_case["query"]
        expected_keywords = test_case["expected_keywords"]
        rag_result = run_rag_pipeline(query, top_k=top_k)
        answer = rag_result["answer"].lower()
        matched_keywords = [
            keyword for keyword in expected_keywords if keyword.lower() in answer
        ]
        all_keywords_found = len(matched_keywords) == len(expected_keywords)
        results_summary.append(
            {
                "query": query,
                "expected_keywords": expected_keywords,
                "matched_keywords": matched_keywords,
                "all_keywords_found": all_keywords_found,
                "answer": rag_result["answer"],
                "retrieved_chunks": rag_result["retrieved_chunks"],
            }
        )
    return results_summary


if __name__ == "__main__":
    evaluation_results = evaluate_rag(top_k=DEFAULT_TOP_K)
    total_cases = len(evaluation_results)
    passed_case = 0
    print("RAG Evaluation Results\n")
    for index, result in enumerate(evaluation_results, start=1):
        print("=" * 100)
        print(f"Test Case #{index}")
        print(f"Query: {result['query']}")
        print(f"Answer: {result['answer']}")
        print(f"Expected Keywords: {result['expected_keywords']}")
        print(f"Matched Keywords: {result['matched_keywords']}")
        print(f"All Keywords Found: {result['all_keywords_found']}")
        if result["all_keywords_found"]:
            passed_case += 1

    score = passed_case/total_cases if total_cases else 0
    print("\n" + "=" * 100)
    print(f"Total Test Cases: {total_cases}")
    print(f"Passed Cases: {passed_case}")
    print(f"RAG Score: {score:.2f}")
