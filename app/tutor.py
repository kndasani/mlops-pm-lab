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

import streamlit as st

@st.cache_data(show_spinner=False)
def ask_tutor(question, role="Product Manager"):
    # 1. Setup DB and Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
    # 2. Retrieve top 3 chunks
    results = db.similarity_search(question, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    
    # 3. Build the Persona-based Prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=question, role=role)
    
    # 4. Call the LLM
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7
    )
    response = model.invoke(prompt)
    
    print(f"\n[Tutor Response for {role}]:")
    print(response.content)
    
    return response.content

if __name__ == "__main__":
    # Example question
    user_query = "What is the importance of storage for GenAI?"
    ask_tutor(user_query, role="Marketing Executive")

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
