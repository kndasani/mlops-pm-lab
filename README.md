# Strategy Mentor: Personalized MLOps Learning

A professional RAG (Retrieval-Augmented Generation) application that translates complex MLOps and AI infrastructure concepts into career-specific analogies.

## Key Features
* Persona-Based Translation: Tailors technical explanations for roles ranging from VP of Engineering to Marketing Leads using custom-tuned prompts.
* Knowledge Transparency: Automatically scans the underlying PDF data lake to present a Knowledge Inventory of covered topics.
* Google-Style UX: A minimalist, Search-First interface that dynamically transforms from a discovery home screen to a focused results view.
* Privacy by Design: Interacts with users without requiring personal data like names, focusing strictly on professional roles.

## Tech Stack
* Core: Python 3.13, Google Gemini 2.5 (LLM), Google Generative AI Embeddings.
* Vector Database: ChromaDB for semantic search and document storage.
* Frontend: Streamlit with custom CSS for dynamic UI states and professional dark-mode chips.

## Setup
1. Clone the repo: git clone https://github.com/kndasani/mlops-pm-lab
2. Install dependencies: pip install -r requirements.txt
3. Add your PDFs to the data/ folder.
4. Run ingestion: python app/ingest.py
5. Launch the app: streamlit run app/main_ui.py

## Model Context Protocol (MCP) Server 🚀

The project now includes a lightweight **MCP-compliant server** that separates
context retrieval from client logic.  Instead of embedding LangChain calls
 directly in the Streamlit UI, the new `app/mcp_server.py` exposes a set of
REST endpoints under `/mcp/v1/*`.  Any application (a chatbot, CLI, or another
service) can query the same knowledge base via HTTP, making the system more
modular and easier to scale.

### Why MCP?

* **Decoupling** – Clients don’t need to know how documents are chunked,
  embedded or stored; they simply request relevant context or ask for an
  answer.  This reduces duplication across multiple consumers.
* **Reusability** – The server can be deployed separately (even in a container)
  and serve many different frontends.  The old Streamlit UI becomes just one
  client of the MCP service.
* **Standardization** – MCP is an open protocol (think similar to OIDC for
  identity) that defines how LLMs and context providers communicate.  Adopting
  it prepares the codebase for integration with third‑party agents and
  orchestration frameworks that already understand the protocol.
* **Observability & Scaling** – A standalone server can be monitored,
  replicated, or replaced without touching UI code.  It also allows caching,
  rate‑limiting, and versioning of the context layer separately.

### Running the MCP Server

After adding your data and building the vector store (steps 1–4 above):

```bash
pip install -r requirements.txt   # includes fastapi & uvicorn
uvicorn app.mcp_server:app --reload  # starts the MCP HTTP service
```

Endpoints include:

* `POST /mcp/v1/contexts/search` – semantic search for context chunks
* `POST /mcp/v1/ask` – ask a question and receive an LLM-generated answer
* `GET /mcp/v1/topics` – list of high-level topics for UI badges
* `GET /mcp/v1/sources` – inventory of source documents
* `POST /mcp/v1/ingest` – re-run ingestion and rebuild the vector store
* `GET /mcp/v1/health` – simple health check

The Streamlit app is unchanged but can now be refactored later to hit these
endpoints instead of running LangChain locally.
