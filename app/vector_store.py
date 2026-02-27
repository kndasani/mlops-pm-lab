import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# when the app is imported as a package, use the full package path; when run
# directly as a script (during development) Python adds the containing directory
# to sys.path, so the bare import still works.
try:
    # preferred for MCP server or any packaged usage
    from app.ingest import load_and_chunk_documents
except ImportError:
    # fallback for direct execution (`python app/vector_store.py`)
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