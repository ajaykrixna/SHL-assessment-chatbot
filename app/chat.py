from app.extractor import extract_constraints
from app.retriever import BM25Retriever

retriever = BM25Retriever("data/catalog.json")


def chat(query):
    # Step 1: Extract constraints
    constraints = extract_constraints(query)

    # Step 2: Build search query
    search_query = constraints["keywords"]

    # Step 3: Search catalog
    results = retriever.search(search_query, top_k=5)

    return {
        "constraints": constraints,
        "recommendations": results
    }