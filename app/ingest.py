import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_PATH = "data_lake/"

def load_and_chunk_documents():
    documents = []
    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf"):
            print(f"Loading: {file}...")
            loader = PyPDFLoader(os.path.join(DATA_PATH, file))
            # We add metadata here: the filename
            data = loader.load()
            for page in data:
                page.metadata["source_file"] = file 
            documents.extend(data)
    
    # The "Chunker": 1000 characters with a small overlap so sentences aren't cut in half
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    
    print(f"\n--- Ingestion Stats ---")
    print(f"Total Pages: {len(documents)}")
    print(f"Total Chunks created: {len(chunks)}")
    return chunks

if __name__ == "__main__":
    chunks = load_and_chunk_documents()
    if chunks:
        print(f"\n--- Preview of Chunk 1 ---")
        print(f"Source: {chunks[0].metadata['source_file']}")
        print(f"Content: {chunks[0].page_content[:300]}...")