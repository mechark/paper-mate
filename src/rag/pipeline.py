import logging

from src.rag.retriever import ArxivRetriever
from src.rag.llm import get_chain

logging.basicConfig(level=logging.INFO)

def create_context(docs) -> str:
    context = ""
    for doc in docs:
        context += f"Title: {doc.metadata.get('Titles', 'No Title')}\n"
        context += f"Content: {doc.page_content}\n"
        context += f"Year of Publication: {doc.metadata.get('Years', 'Unknown')}\n"
    return context

def answer_question(question: str, k: int = 3) -> str:
    retriever = ArxivRetriever()
    results = retriever.search(question, k=k)
    
    context = create_context(results)
    logging.info(f"Constructed context for LLM: {context}")
    chain = get_chain()

    response = chain.invoke({"context": context, "question": question})
    return response
