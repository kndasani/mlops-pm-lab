from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_PATH = "chroma_db"

def test_retrieval(query):
    # 1. Load the "Math Engine" (Must be the same one we used to create the DB)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 2. Connect to the existing database
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
    # 3. Search for the top 3 most relevant chunks
    print(f"\nSearching for: '{query}'")
    results = db.similarity_search_with_relevance_scores(query, k=3)
    
    for i, (doc, score) in enumerate(results):
        print(f"\n--- Result {i+1} (Score: {score:.4f}) ---")
        print(f"Source: {doc.metadata.get('source_file')}")
        print(f"Content snippet: {doc.page_content[:200]}...")

if __name__ == "__main__":
    # Test it with a question a PM might ask
    test_retrieval("What are the key components of MLOps for a product manager?")