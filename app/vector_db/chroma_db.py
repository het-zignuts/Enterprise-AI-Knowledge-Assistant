from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def create_vector_data_store(chunks: list[str], collection_name: str, metadata):
    """
    This method takes text chunks, the vector collection name, metadata per chunk, etc., 
    generate embeddings from them and store them in vector database.
    """
    embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2") #Usng HuggingFace Embedding model
    # Ceating Chroma vector db instance for persistant data storage, along with the metadata and given collection
    vectordb=Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadata,
        collection_name=collection_name,
        persist_directory="./chroma_data"
    )
    return vectordb

def load_vectordb(collection_name):
    """
    This function loads existing persistant Chroma Vector DB, with given Chroma collection.
    """
    #Using the same embedding model in retrieval as used in ingestion.
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    #load the persisted Chroma collection.
    return Chroma(
        collection_name=collection_name,
        persist_directory="./chroma_data",
        embedding_function=embeddings
    )