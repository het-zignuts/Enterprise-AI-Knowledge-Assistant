def retrieve_context(vector_db, question: str, min_score: float = 0.3):
    retriever = vector_db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k": 20,  # pool to choose from
            "lambda_mult": 0.5  # 0.3–0.7 is typical
        }
    )
    docs = retriever.invoke(question)
    if not docs:
        return None
    context_blocks=[]
    doc_ids=[]
    for doc in docs:
        source=doc.metadata.get("filename", "unknown")
        chunk_id=doc.metadata.get("chunk_index")
        doc_id=doc.metadata.get("document_id")
        context_blocks.append(
            f"[Source: {source}, Chunk: {chunk_id}]\n{doc.page_content}"
        )
        doc_ids.append({
            "source": source,
            "id": doc_id
        })
    context="\n\n".join(context_blocks)
    return doc_ids, context
