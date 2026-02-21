import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from ingest import load_and_chunk_documents

# This is where the "Database" will be stored on your hard drive
CHROMA_PATH = "chroma_db"

def create_vector_store():
    # 1. Get the chunks from our previous step
    chunks = load_and_chunk_documents()
    
    # 2. Define the "Embedding Model" (The math engine)
    # This model turns text into a list of numbers
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 3. Create the database and save it to your laptop
    print(f"Creating vector store at {CHROMA_PATH}...")
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    
    print("Vector store created and saved successfully!")
    return vector_db

if __name__ == "__main__":
    create_vector_store()