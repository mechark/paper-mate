import logging
from sentence_transformers import CrossEncoder

from src.rag.retriever import ArxivRetriever
from src.rag.llm import get_chain

logging.basicConfig(level=logging.INFO)

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
retriever = ArxivRetriever()


def create_context(docs) -> str:
    """Create context string from documents."""
    context = ""
    for doc in docs:
        context += f"Title: {doc.metadata.get('Titles', 'No Title')}\n"
        context += f"Content: {doc.page_content}\n"
        context += f"Year of Publication: {doc.metadata.get('Years', 'Unknown')}\n"
    return context


def rerank_documents(query: str, documents, top_k: int = 3):
    """Rerank documents using a cross-encoder model."""
    pairs = [[query, doc.page_content] for doc in documents]

    scores = reranker.predict(pairs)

    scored_docs = list(zip(documents, scores))
    scored_docs.sort(key=lambda x: x[1], reverse=True)

    reranked = [doc for doc, score in scored_docs[:top_k]]

    logging.info(
        f"Reranking scores: {[f'{score:.2f}' for _, score in scored_docs[:top_k]]}"
    )

    return reranked


def answer_question(question: str, k: int = 3) -> str:
    """Answer a question using retrieved and reranked documents."""
    # Retrieve more documents than needed for reranking
    results = retriever.search(question, k=80)

    # Rerank and get top k
    reranked_results = rerank_documents(question, results, top_k=k)

    context = create_context(reranked_results)
    logging.info(f"Constructed context for LLM: {context}")
    chain = get_chain()

    response = chain.invoke({"context": context, "question": question})
    return response
