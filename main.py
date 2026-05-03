import sys
import os
import requests
from fastapi import FastAPI
from supabase import create_client
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# 1. Environment Setup
load_dotenv()

# 2. Configuration & API Keys
HF_TOKEN = os.getenv("HF_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 3. Client Initialization
inference_client = InferenceClient(token=HF_TOKEN)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Enterprise RAG System - AI Engineer Portfolio")

# --- Core Functions ---

def get_embedding(text):
    """Converts input text into a vector embedding for semantic search."""
    try:
        response = inference_client.feature_extraction(
            text, 
            model="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Ensure result is JSON serializable for Supabase
        if hasattr(response, "tolist"):
            return response.tolist()
        
        if isinstance(response, list) and len(response) > 0:
            if isinstance(response[0], list):
                return response[0] 
                
        return response
    except Exception as e:
        print(f"❌ Embedding Error: {str(e)}")
        raise e

def generate_answer_with_groq(question, context):
    """Generates a grounded answer using Groq LPU acceleration."""
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # SYSTEM PROMPT: This prevents the AI from using external knowledge
    system_message = (
        "You are a professional Data Analyst. You must answer the user's question "
        "STRICTLY using the provided context. If the information is not present "
        "in the context, politely state that the information is not available "
        "in the uploaded documents. Do NOT use outside knowledge."
    )
    
    prompt = f"Context: {context}\n\nUser Question: {question}"
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1 # Low temperature for high accuracy/less creativity
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=data)
        result = response.json()
        
        if 'error' in result:
            print(f"❌ Groq API Error: {result['error']}")
            return f"Service currently unavailable."
            
        return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"❌ Inference Error: {str(e)}")
        return "An error occurred while generating the response."

# --- API Endpoints ---

@app.get("/")
def health_check():
    return {
        "status": "Healthy", 
        "system": "RAG-Engine-v1",
        "engineer": "Ahmed"
    }

@app.get("/search")
def search(q: str):
    """
    Main Search Endpoint: 
    Embeds query -> Vector Search (Supabase) -> LLM Synthesis (Groq)
    """
    # Step 1: Generate Vector
    vector = get_embedding(q)
    
    # Step 2: Semantic Search in Vector Database
    try:
        res = supabase.rpc('match_educational_content', {
            'query_embedding': vector,
            'match_threshold': 0.35, # Optimized for precision
            'match_count': 1 
        }).execute()  
    except Exception as e:
        print(f"❌ Database Error: {str(e)}")
        return {"error": "Internal Database Connection Issue"}
    
    # Handle Case: No relevant data found
    if not res.data:
        return {"answer": "I could not find any relevant information in the database."}

    # Step 3: Synthesis via Groq LLM
    retrieved_text = res.data[0]['content']
    final_answer = generate_answer_with_groq(q, retrieved_text)
    
    return {
        "query": q,
        "ai_response": final_answer,
        "document_reference": retrieved_text
    }