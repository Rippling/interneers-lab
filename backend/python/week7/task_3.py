from week7.semantic_search import semantic_search

results = semantic_search(
    query="construction toys",
    top_k=5,
    model_name="all-MiniLM-L6-v2"
)


print("\nSemantic Search Results")
print("-" * 50)

for index, item in enumerate(results, start=1):
    print(f"{index}. {item['name']} | score={item['semantic_score']}")
    print(f"   Description: {item['description']}")
    print(f"   Category   : {item['category']}")
    print()
