def retrieve_context(vector_db, question: str, min_score: float = 0.3):
    retriever = vectordb.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 4,
            "score_threshold": min_score
        }
    )
    docs = retriever.get_relevant_documents(question)
    if not docs:
        return None
    context = "\n\n".join([d.page_content for d in docs])
    return context