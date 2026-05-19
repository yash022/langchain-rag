# 🤖 Dell AI Support Bot

An AI-powered RAG (Retrieval-Augmented Generation) support assistant built to automate repetitive Dell L1 support queries using semantic search, vector databases, and LLM-powered grounded responses.

The bot scrapes Dell support documentation, converts it into embeddings, stores them in a FAISS vector database, and retrieves the most relevant information in real time to generate accurate answers with source citations in under 10 seconds.

---

# 🚀 Problem Statement

Traditional L1 customer support workflows are slow and repetitive:

1. Customer raises issue  
2. Agent manually searches knowledge base  
3. Reads documentation  
4. Relays solution  

⏱️ Average resolution time: **8–11 minutes per ticket**

Most support queries are repetitive and document-driven:

- Battery not charging
- Blue screen issues
- BIOS update help
- WiFi problems
- Monitor/display issues
- Audio problems

This project replaces manual KB search with an AI-powered retrieval system.

---

# 💡 Solution

The Dell AI Support Bot uses a complete RAG pipeline:

- Scrapes Dell support documentation
- Splits data into semantic chunks
- Converts text into embeddings
- Stores embeddings in FAISS vector DB
- Retrieves top-k relevant chunks
- Uses Gemini LLM to generate grounded responses
- Displays source citations for transparency

---

# 🏗️ System Architecture

```text
User Query
    ↓
Streamlit Chat UI
    ↓
Query Embedding
    ↓
FAISS Semantic Search
    ↓
Top-K Relevant Chunks Retrieved
    ↓
Gemini 2.5 Flash LLM
    ↓
Grounded AI Response + Source Links
