from langchain_community.document_loaders import HuggingFaceDatasetLoader
from langchain_classic.text_splitter import SentenceTransformersTokenTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.core.config import settings
from langchain_community.vectorstores import FAISS
import os
import logging


class ArxivRetriever(BaseRetriever):
    """Retriever for Arxiv documents using a combination of dense and sparse retrieval."""

    k: int = 4

    def __init__(self, cache_path="./vector_store"):
        super().__init__()

        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Try to load cached vector store first
        if os.path.exists(cache_path):
            logging.info("Loading vector store from cache...")
            self._vectorstore = FAISS.load_local(
                cache_path, embedding, allow_dangerous_deserialization=True
            )
        else:
            # Build and save
            loader = HuggingFaceDatasetLoader(
                "MaartenGr/arxiv_nlp", page_content_column="Abstracts"
            )
            documents = loader.load()

            splitter = splitter = SentenceTransformersTokenTextSplitter(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                chunk_size=128,
                chunk_overlap=20
            )
            self._documents = splitter.split_documents(documents)

            self._vectorstore = FAISS.from_documents(self._documents, embedding)
            self._vectorstore.save_local(cache_path)

        self._sparse_retriever = BM25Retriever.from_documents(
            self._vectorstore.docstore._dict.values()
        )

    def _get_relevant_documents(self, query: str) -> list[Document]:
        """
        Retrieve relevant documents using Reciprocal Rank Fusion of dense and sparse retrieval.
        """

        # Dense & sparse retrieval results
        dense_docs = self._vectorstore.search(query, k=self.k, search_type="similarity")
        sparse_docs = self._sparse_retriever.invoke(query)[: self.k]

        rrf_scores = {}
        k_constant = settings.RETRIEVER_K_CONSTANT

        # Add dense retrieval scores. Use content as key
        for rank, doc in enumerate(dense_docs, start=1):
            doc_key = doc.page_content
            rrf_scores[doc_key] = rrf_scores.get(doc_key, 0) + 1 / (k_constant + rank)

        # Add sparse retrieval scores
        for rank, doc in enumerate(sparse_docs, start=1):
            doc_key = doc.page_content
            rrf_scores[doc_key] = rrf_scores.get(doc_key, 0) + 1 / (k_constant + rank)

        # Create a mapping from content to doc
        doc_map = {doc.page_content: doc for doc in dense_docs + sparse_docs}

        # Sort by RRF score and return docs
        sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        fused_docs = [doc_map[doc_key] for doc_key, score in sorted_docs[: self.k]]

        return fused_docs
