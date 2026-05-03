<img width="1270" height="535" alt="Screenshot 2026-05-04 005933" src="https://github.com/user-attachments/assets/47afc2f5-f356-4c3e-9f51-5365e0394fea" />

<img width="1859" height="681" alt="Screenshot 2026-05-04 010310" src="https://github.com/user-attachments/assets/1f0309b1-af42-4119-b7c0-769514acc021" />

<img width="1857" height="703" alt="Screenshot 2026-05-04 010326" src="https://github.com/user-attachments/assets/b9ef0d39-b673-4afb-b41f-38eaee29ef35" />

<img width="994" height="779" alt="Screenshot 2026-05-04 010434" src="https://github.com/user-attachments/assets/e4b5ac87-7900-4953-b7b7-0f5d3c715d44" />

<img width="1078" height="635" alt="image" src="https://github.com/user-attachments/assets/fc3851e2-d458-4e14-86e0-744360cb22b6" />















# Autonomous Telegram AI Agent with Enterprise RAG Integration

This repository showcases a production-ready AI Agent engineered to provide specialized document intelligence. Unlike standard chatbots, this system utilizes a Retrieval-Augmented Generation (RAG) pipeline to ensure all responses are grounded in real-world proprietary data, effectively eliminating AI hallucinations and delivering enterprise-grade accuracy.

## The Problem and The Solution

The Challenge: Standard LLMs often fail when asked about specific, private, or highly technical datasets because they lack the context of that data, leading to inaccurate or invented information.

The Solution: I engineered a closed-loop system where the AI is constrained to a specific knowledge base. The agent retrieves relevant facts from a vector database before formulating any response, ensuring 100% data integrity.

## Technical Architecture and Lifecycle

The complexity of this project lies in the seamless orchestration of a multi-stage data pipeline:

### 1. High-Fidelity Data Engineering
* Real-Data Ingestion: Processed actual technical datasets, transforming raw information into a structured knowledge base.
* Semantic Vectorization: Utilized the all-MiniLM-L6-v2 embedding model to transform text into high-dimensional vectors, capturing the true meaning of the data rather than just keywords.
* Vector Storage: Implemented Supabase with pgvector for professional-grade storage and sub-second similarity searches.

### 2. The RAG Intelligence Loop
When a query is received via Telegram, the system executes the following:
* Semantic Retrieval: A real-time mathematical search is performed in the vector database to find the most relevant contextual chunks.
* Context Augmentation: The retrieved facts are dynamically injected into a strict system prompt.
* Grounded Inference: Using Llama 3.1 8B via Groq, the agent generates a response that is strictly limited to the provided facts.

### 3. Enterprise Orchestration
* Workflow Engine: Used n8n to manage the logic flow and API webhooks between Telegram and the backend.
* High-Speed Backend: A custom FastAPI application serves as the core of the operation, handling embeddings and retrieval logic.
* Performance Optimization: Leveraged Groq LPU acceleration to achieve near-instantaneous response times.

## The Tech Stack

Component | Technology
--- | ---
Backend Framework | Python 3.12, FastAPI
Orchestration | n8n
Vector Database | Supabase (pgvector)
LLM Inference | Groq LPU (Llama 3.1)
Embeddings | Hugging Face (all-MiniLM-L6-v2)
Security | Ngrok, Dotenv (Secret Management)

## Key Technical Achievements

* Hallucination Prevention: The agent is programmed to acknowledge its limitations if the answer is not present in the knowledge base.
* Production-Ready Security: Implemented comprehensive secret management to ensure API keys and database credentials remain secure.
* Scalable Architecture: Designed the system to handle concurrent user requests efficiently through asynchronous processing in FastAPI.

## How to Deploy

1. Environment Setup: Create a .env file using the keys provided in .env.example.
2. Dependencies: Run pip install -r requirements.txt.
3. Run Server: Execute python -m uvicorn main:app --reload.
4. Connect n8n: Import the provided n8n workflow and point it to your backend URL.

Developed by Ahmed
AI Engineer specialized in RAG Architectures and Agentic Workflows
