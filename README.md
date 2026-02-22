# Strategy Mentor: Personalized MLOps Learning

A professional RAG (Retrieval-Augmented Generation) application that translates complex MLOps and AI infrastructure concepts into career-specific analogies.

## Key Features
* Persona-Based Translation: Tailors technical explanations for roles ranging from VP of Engineering to Marketing Leads using custom-tuned prompts.
* Knowledge Transparency: Automatically scans the underlying PDF data lake to present a Knowledge Inventory of covered topics.
* Google-Style UX: A minimalist, Search-First interface that dynamically transforms from a discovery home screen to a focused results view.
* Privacy by Design: Interacts with users without requiring personal data like names, focusing strictly on professional roles.

## Tech Stack
* Core: Python 3.13, Google Gemini 1.5 (LLM), Google Generative AI Embeddings.
* Vector Database: ChromaDB for semantic search and document storage.
* Frontend: Streamlit with custom CSS for dynamic UI states and professional dark-mode chips.

## Setup
1. Clone the repo: git clone [your-repo-link]
2. Install dependencies: pip install -r requirements.txt
3. Add your PDFs to the data/ folder.
4. Run ingestion: python app/ingest.py
5. Launch the app: streamlit run app/main_ui.py