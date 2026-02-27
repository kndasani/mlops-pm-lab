import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel

from .tutor import generate_answer, get_knowledge_topics, get_knowledge_inventory
from .vector_store import create_vector_store
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

app = FastAPI(title="Strategy Mentor MCP Server")

# globally reused embeddings / db reference
_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
_db = Chroma(persist_directory="chroma_db", embedding_function=_embeddings)


class ContextSearchRequest(BaseModel):
    query: str
    k: int = 3


class AskRequest(BaseModel):
    question: str
    role: str = "Product Manager"


@app.post("/mcp/v1/contexts/search")
def search_context(req: ContextSearchRequest):
    """Return the top *k* documents matching a query."""
    results = _db.similarity_search(req.query, k=req.k)
    return {
        "contexts": [
            {"text": r.page_content, "metadata": r.metadata} for r in results
        ]
    }


@app.post("/mcp/v1/ask")
def ask(req: AskRequest):
    """Generate an answer using the same logic previously used by Streamlit."""
    answer = generate_answer(req.question, role=req.role)
    return {"answer": answer}


@app.get("/mcp/v1/topics")
def topics():
    """Expose the knowledge topics badge API used in the UI."""
    return {"topics": get_knowledge_topics()}


@app.get("/mcp/v1/sources")
def sources():
    """List unique source filenames in the vector store."""
    return {"sources": get_knowledge_inventory()}


@app.post("/mcp/v1/ingest")
def ingest():
    """Trigger a full rebuild of the vector database from the files on disk."""
    create_vector_store()
    # refresh global reference so queries immediately see new data
    global _db
    _db = Chroma(persist_directory="chroma_db", embedding_function=_embeddings)
    return {"status": "vector store rebuilt"}


@app.post("/mcp/v1/documents")
def upload_document(file: UploadFile = None):
    """Accept a new PDF, store it in the data lake and rebuild the index.

    This endpoint illustrates how MCP clients can push new content without
    needing direct access to the filesystem.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported")

    contents = file.file.read()
    dest = os.path.join("data_lake", file.filename)
    with open(dest, "wb") as f:
        f.write(contents)

    # rebuild everything after the new document arrives
    create_vector_store()
    global _db
    _db = Chroma(persist_directory="chroma_db", embedding_function=_embeddings)
    return {"status": "uploaded and reindexed", "filename": file.filename}


@app.get("/mcp/v1/health")
def health():
    """Simple health check used by Kubernetes or load balancers."""
    return {"status": "ok"}
