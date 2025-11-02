import logging

from src.rag.retriever import ArxivRetriever
from src.rag.llm import get_chain
from src.rag.reranker import ArxivReranker

logging.basicConfig(level=logging.INFO)

reranker = ArxivReranker()
retriever = ArxivRetriever()


def create_context(docs) -> str:
    """Create context string from documents."""
    context = ""
    for doc in docs:
        context += f"Title: {doc.metadata.get('Titles', 'No Title')}\n"
        context += f"Content: {doc.page_content}\n"
        context += f"Year of Publication: {doc.metadata.get('Years', 'Unknown')}\n\n"
    return context


def answer_question(question: str, k: int = 4) -> str:
    """Answer a question using retrieved and reranked documents."""
    # Retrieve more documents than needed for reranking
    retriever.k = 80
    results = retriever.invoke(question)

    # Rerank and get top k
    reranked_results = reranker.rerank_documents(question, results, top_k=k)

    context = create_context(reranked_results)
    logging.info(f"Constructed context for LLM: {context}")
    chain = get_chain()

    response = chain.invoke({"context": context, "question": question})
    return response
