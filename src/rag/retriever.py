from langchain_community.document_loaders import HuggingFaceDatasetLoader
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
import logging


class ArxivRetriever:
    def __init__(self, cache_path="./vector_store"):
        # embedding = HuggingFaceEmbeddings(model_name="allenai/specter2_base")
        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Try to load cached vector store first
        if os.path.exists(cache_path):
            logging.info("Loading vector store from cache...")
            self.vectorstore = FAISS.load_local(
                cache_path, embedding, allow_dangerous_deserialization=True
            )
        else:
            # Build and save
            loader = HuggingFaceDatasetLoader(
                "MaartenGr/arxiv_nlp", page_content_column="Abstracts"
            )
            documents = loader.load()

            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
            self.documents = splitter.split_documents(documents)

            self.vectorstore = FAISS.from_documents(self.documents, embedding)
            self.vectorstore.save_local(cache_path)

    def search(self, query: str, k: int = 5):
        return self.vectorstore.similarity_search(query, k=k)
