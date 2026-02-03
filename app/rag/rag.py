def retrieve_context(vector_db, question: str):
    """
    Retrieves the most relevant and similar chunks to the given query using MMR
    """
    retriever=vector_db.as_retriever(
        search_type="mmr", # Using Maximal Margin Retrieval technique
        search_kwargs={
            "k": 4, # gives top 4 most relevant context chunks
            "fetch_k": 20,  # out of 20 fetched chunks
            "lambda_mult": 0.5  # a knob to adjust extent of similar chunks retrieved, more value, less similar retrieval
        }
    )
    # retrieve conytext chunks
    docs=retriever.invoke(question)
    if not docs:
        return None
    context_blocks=[]
    doc_ids=[]
    for doc in docs:
        # extract metadata fields from the chunk
        source=doc.metadata.get("filename", "unknown") # getting file name
        chunk_id=doc.metadata.get("chunk_index") # getting chunk id
        doc_id=doc.metadata.get("document_id") # getting document/file id
        context_blocks.append(
            f"[Source: {source}, Chunk: {chunk_id}]\n{doc.page_content}"
        ) # gathering all the context blocks
        doc_ids.append({
            "source": source,
            "id": doc_id
        }) # gathering all the document ids
    context="\n\n".join(context_blocks) # prepare the context string block to augment the query
    return doc_ids, context # share the context as well as its source refrences
