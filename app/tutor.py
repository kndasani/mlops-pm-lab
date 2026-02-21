import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate

load_dotenv() # This automatically looks for the .env file and loads the key

# Configuration
CHROMA_PATH = "chroma_db"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:
{context}

---
Answer the question as if you are a mentor speaking to a {role}. 
Use language and analogies that a {role} would understand.

Question: {question}
"""

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

if __name__ == "__main__":
    # Example question
    user_query = "What is the importance of storage for GenAI?"
    ask_tutor(user_query, role="Marketing Executive")