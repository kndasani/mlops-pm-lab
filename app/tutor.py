import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv() # This automatically looks for the .env file and loads the key

# Configuration
CHROMA_PATH = "chroma_db"
PROMPT_TEMPLATE = """
You are a world-class mentor known for extreme personalization. 
Explain the following MLOps concept using the provided context, but you MUST adapt your vocabulary and analogies based on the user's role.

STRICT ADAPTATION RULES:
1. If the role is TECHNICAL (e.g., VP of Eng, Architect): Focus on infrastructure, latency, CI/CD pipelines, and technical debt.
2. If the role is BUSINESS (e.g., Marketing, Sales): Avoid jargon. Use analogies from building a house, running a kitchen, or a supply chain. Focus on ROI and speed.
3. DO NOT use personal names.
4. If the context doesn't have the answer, say you don't know based on the current library.

Context: {context}
User Role: {role}
Question: {question}

Answer for a {role} perspective:"""


# NOTE: the `ask_tutor` wrapper is now just a thin convenience over
# `generate_answer` and exists so that the old Streamlit UI can keep using
# the same function signature.  The heavier work is done by
# `generate_answer` which is protocol‑agnostic and can be reused by our new
# MCP server.

def _retrieve_context(question: str, k: int = 3) -> str:
    """Return the top *k* chunks as a single string separated by delimiters.
    The MCP server and the old UI both rely on this helper under the hood.
    """
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    results = db.similarity_search(question, k=k)
    return "\n\n---\n\n".join([doc.page_content for doc in results])


def generate_answer(question: str, role: str = "Product Manager") -> str:
    """Core logic for querying the vector store and calling the LLM.

    This function can be used by the Streamlit UI (via ``ask_tutor``) or by
    any external caller (e.g. our MCP server).
    """

    context_text = _retrieve_context(question)

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(
        context=context_text, question=question, role=role
    )

    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
    )
    response = model.invoke(prompt)
    print(f"\n[Tutor Response for {role}]:")
    print(response.content)
    return response.content


# keep the old helper for backwards compatibility with Streamlit

def ask_tutor(question, role="Product Manager"):
    return generate_answer(question, role=role)


if __name__ == "__main__":
    # Example question
    user_query = "What is the importance of storage for GenAI?"
    print(generate_answer(user_query, role="Marketing Executive"))

def get_knowledge_inventory():
    """Returns a list of unique source filenames present in the vector store."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
    
    # Get all metadata from the database
    data = vector_db.get()
    metadatas = data.get('metadatas', [])
    
    # Extract unique source filenames
    sources = set()
    for meta in metadatas:
        source_path = meta.get('source', 'Unknown')
        sources.add(os.path.basename(source_path))
    
    return sorted(list(sources))

def get_knowledge_topics():
    """Extracts unique topics covered in the document library."""
    # Initialize the DB connection
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
    
    # Pull data from the vector store
    data = vector_db.get()
    documents = data.get('documents', [])
    
    topics = set() # Using a 'set' automatically handles de-duplication

    for text in documents:
        text_lower = text.lower()
        # Mapping keywords found in the PDFs to clean "Topic Names"
        if "drift" in text_lower or "monitoring" in text_lower:
            topics.add("Model Monitoring & Drift")
        elif "llm" in text_lower or "generative" in text_lower:
            topics.add("Generative AI Architecture")
        elif "deployment" in text_lower or "pipeline" in text_lower:
            topics.add("MLOps Deployment Strategies")
        elif "security" in text_lower or "privacy" in text_lower:
            topics.add("AI Security & Compliance")
        else:
            topics.add("General AI Infrastructure")
    
    # Return as a sorted list for a professional look in the UI
    return sorted(list(topics))
