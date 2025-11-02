import logging
from sentence_transformers import CrossEncoder


class ArxivReranker:
    """Reranker for Arxiv documents using a cross-encoder model."""

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self.reranker = CrossEncoder(self.model_name)

    def rerank_documents(self, query: str, documents, top_k: int = 3):
        """Rerank documents using a cross-encoder model."""
        pairs = [[query, doc.page_content] for doc in documents]

        scores = self.reranker.predict(pairs)

        scored_docs = list(zip(documents, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)

        reranked = [doc for doc, score in scored_docs[:top_k]]

        logging.info(
            f"Reranking scores: {[f'{score:.2f}' for _, score in scored_docs[:top_k]]}"
        )

        return reranked
