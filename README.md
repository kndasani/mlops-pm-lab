# Strategy Mentor: AI Learning & Strategy Builder

A comprehensive AI intelligence platform that combines concept explanation with strategic planning. Ask specific questions about AI, or build a personalized AI implementation strategy tailored to your unique situation.

## Key Features

### 🎓 Ask a Question Mode
* **Role-Based Answers**: Ask questions about AI concepts, techniques, and applications tailored to your specific role and expertise level
* **Knowledge Transparency**: Browse topic inventory to discover what's available in the knowledge base
* **Career-Specific Explanations**: Get answers that match your professional context, not generic technical jargon

### 🗺️ Build Your AI Strategy Mode  
* **Conversational Interview**: Natural multi-step conversation (no rigid forms) where the system adapts to your context
* **Context-Aware Analysis**: Automatically detects your role, goals, challenges, and maturity level
* **Phased Roadmap Generation**: Creates a detailed 3-4 phase implementation plan with:
  - Clear goals for each phase
  - Specific activities and deliverables
  - Required tools and technologies
  - Success criteria and milestones
  - Resource requirements
  - Risk mitigation strategies
  
* **Visual Dashboard**:
  - Color-coded timeline showing phase progression and completion status
  - Quick wins and success metrics overview
  - Interactive expandable phase detail cards
  - Risk assessment and mitigation table
  - Download as Markdown or JSON

## Universal Design

Works for **any user type**—not just tech professionals:
- 👨‍🏫 Teachers wanting to incorporate AI in classrooms
- 💼 Business owners exploring AI for operations
- 📚 Bookstore owners looking to increase sales with AI
- 🎨 Creatives integrating AI into workflows
- 🚀 Entrepreneurs building AI-powered products
- 👔 Enterprise executives planning digital transformation

## Tech Stack

* **Core**: Python 3.13, Google Gemini 2.5 Flash (LLM), ChromaDB vector database
* **Frontend**: Streamlit with responsive card-based UI
* **Backend Server**: FastAPI + Uvicorn (Model Context Protocol)
* **Visualization**: SVG timelines, interactive HTML dashboards
* **Data Retrieval**: Semantic search with HuggingFace embeddings (all-MiniLM-L6-v2)

## Setup

### Quick Start

1. **Clone and setup**:
   ```bash
   git clone https://github.com/kndasani/mlops-pm-lab
   cd mlops-pm-lab
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   # Create .env file with your API key
   echo "GOOGLE_API_KEY=your-key-here" > .env
   ```

3. **Add your knowledge base** (optional):
   ```bash
   # Place PDFs in the data_lake/ folder
   python app/ingest.py  # Builds the vector database
   ```

4. **Launch the app**:
   ```bash
   streamlit run app/main_ui.py
   ```

The app will open at `http://localhost:8501` with a clean home page offering two options.

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

* `POST /mcp/v1/ask` – Ask a question (returns tailored answer)
* `POST /mcp/v1/strategy/analyze` – Analyze user context (role, goals, challenges)
* `POST /mcp/v1/strategy/build` – Generate complete AI strategy roadmap
* `POST /mcp/v1/strategy/export-markdown` – Export strategy as Markdown
* `GET /mcp/v1/topics` – Get list of available topics
* `GET /mcp/v1/sources` – Get inventory of source documents
* `POST /mcp/v1/ingest` – Re-run document ingestion
* `GET /mcp/v1/health` – Health check

## Application Architecture

### Files Overview

| File | Purpose |
|------|---------|
| `main_ui.py` | Streamlit app with dual modes (Ask + Strategy) |
| `strategy_builder.py` | Core strategy generation logic with context analysis & roadmap creation |
| `roadmap_renderer.py` | Visual rendering of strategies (SVG timelines, HTML dashboards) |
| `tutor.py` | Question-answering system with role-based context |
| `mcp_server.py` | FastAPI backend exposing REST endpoints |
| `vector_store.py` | ChromaDB integration and semantic search |
| `ingest.py` | Document ingestion pipeline (PDF → embeddings) |

### Strategy Builder Flow

1. **Step 1**: User describes their situation in free-form text
2. **Step 2**: System analyzes context and asks 2-3 follow-up questions
3. **Step 3**: Generate phased roadmap based on full conversation context
4. **Step 4**: Display interactive dashboard with timelines, metrics, and export options

## Example Usage

### Ask a Question
1. Click "Start Asking Questions"
2. Enter your role (e.g., "Product Manager")
3. Ask a question (e.g., "What is Model Drift?")
4. Get a tailored explanation for your role's context

### Build Your AI Strategy
1. Click "Build Your Strategy"
2. Describe your situation (e.g., "I'm a bookstore owner wanting to increase sales using AI")
3. Answer follow-up questions about expectations and concerns
4. Receive a phased roadmap with:
   - Foundation phase (weeks 1-3)
   - Implementation phase (weeks 3-6)
   - Scale phase (weeks 6+)
5. Download as Markdown or JSON

## Customization

### Add Your Knowledge Base

Place PDF files in the `data_lake/` folder, then run:
```bash
python app/ingest.py
```

This will:
- Extract text from PDFs
- Split into semantic chunks
- Generate embeddings
- Store in ChromaDB

### Configure LLM

Edit `.env`:
```bash
GOOGLE_API_KEY=your-key-here
MCP_SERVER_URL=http://localhost:8000  # Optional, for remote server
```

## Future Enhancements

- [ ] Interactive phase editing and refinement
- [ ] Strategy comparison and templates
- [ ] User authentication and strategy saving
- [ ] Integration with project management tools
- [ ] Multi-language support
- [ ] Custom embedding models
- [ ] Fine-tuned prompts per industry

## Contributing

Contributions welcome! Areas for improvement:
- Better context detection for edge cases
- Enhanced timeline visualizations
- Additional export formats (PDF, etc.)
- Performance optimizations
- Expanded knowledge base

## License

MIT
