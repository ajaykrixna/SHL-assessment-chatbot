import json
import re
from rank_bm25 import BM25Okapi


class BM25Retriever:
    def __init__(self, catalog_path):
        with open(catalog_path, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

        self.documents = [
            f"{item['title']} {item['description']}"
            for item in self.catalog
        ]

        tokenized_docs = [self.tokenize(doc) for doc in self.documents]

        self.bm25 = BM25Okapi(tokenized_docs)

    def tokenize(self, text):
        """
        Lowercase the text and remove punctuation before splitting.
        """
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        return text.split()

    def search(self, query, top_k=10):

        if not query.strip():
            return []

        tokenized_query = self.tokenize(query)

        scores = self.bm25.get_scores(tokenized_query)

        ranked = sorted(
            zip(scores, self.catalog),
            key=lambda x: x[0],
            reverse=True
        )

        # Return only documents with a positive BM25 score
        results = []

        for score, item in ranked:
            if score > 0:
                results.append(item)

            if len(results) >= top_k:
                break

        return results