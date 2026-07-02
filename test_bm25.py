from app.retriever import BM25Retriever

retriever = BM25Retriever("data/catalog.json")

results = retriever.search(
    "Senior Java developer with leadership skills",
    top_k=5
)

for i, result in enumerate(results, 1):
    print(f"\n{i}. {result['title']}")
    print(result["description"])
    print(result["url"])