import json
from rank_bm25 import BM25Okapi


class BM25Retriever:
    def __init__(self, catalog_path):
        with open(catalog_path, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

        self.documents = [
            f"{item['title']} {item['description']}"
            for item in self.catalog
        ]

        tokenized_docs = [doc.lower().split() for doc in self.documents]

        self.bm25 = BM25Okapi(tokenized_docs)

    def search(self, query, top_k=10):
        tokenized_query = query.lower().split()

        scores = self.bm25.get_scores(tokenized_query)

        ranked = sorted(
            zip(scores, self.catalog),
            reverse=True,
            key=lambda x: x[0]
        )

        return [item for score, item in ranked[:top_k]]