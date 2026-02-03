from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def create_vector_data_store(chunks: list[str], collection_name: str, metadata):
    embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadata,
        collection_name=collection_name,
        persist_directory="./chroma_data"
    )
    return vectordb

def load_vectordb(collection_name):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return Chroma(
        collection_name=collection_name,
        persist_directory="./chroma_data",
        embedding_function=embeddings
    )