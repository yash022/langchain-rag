🤖 Dell AI Support Bot

An AI-powered RAG (Retrieval-Augmented Generation) support assistant built to automate repetitive Dell L1 support queries using semantic search, vector databases, and LLM-powered grounded responses.

The bot scrapes Dell support documentation, converts it into embeddings, stores it in a FAISS vector database, and retrieves the most relevant information in real time to generate accurate answers with source citations in under 10 seconds.

🚀 Problem Statement

Traditional L1 customer support workflows are slow and repetitive:

Customer raises issue
Agent manually searches knowledge base
Reads documentation
Relays solution

⏱️ Average resolution time: 8–11 minutes per ticket

Most queries are repetitive and document-driven:

Battery not charging
Blue screen issues
BIOS update help
WiFi problems
Monitor/display issues
Audio problems

This project replaces manual KB search with an AI-powered retrieval system.

💡 Solution

The Dell AI Support Bot uses a complete RAG pipeline:

Scrapes Dell support documentation
Splits data into semantic chunks
Converts text into embeddings
Stores embeddings in FAISS vector DB
Retrieves top-k relevant chunks
Uses Gemini LLM to generate grounded responses
Displays source citations for transparency
🏗️ System Architecture

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

⚙️ Tech Stack
Component	Technology
Frontend	Streamlit
Web Scraping	Requests + BeautifulSoup
LLM	Gemini 2.5 Flash
Framework	LangChain
Embeddings	HuggingFace all-MiniLM-L6-v2
Vector DB	FAISS
Chunking	RecursiveCharacterTextSplitter
🔥 Features

✅ AI-powered Dell troubleshooting assistant
✅ Real-time semantic search
✅ Source-cited responses
✅ FAISS vector retrieval
✅ Hallucination reduction using RAG
✅ Covers 70+ Dell support topics
✅ Streamlit conversational UI
✅ <10 second response generation

📊 Project Impact
Metric	Value
Manual support resolution	8–11 min
AI response time	<10 sec
Dell support topics covered	70+
Retrieval method	Semantic Vector Search
Top-k retrieval	k = 4

Potential enterprise impact modeled in pitch deck:

Estimated support cost base: ₹360–770 Cr
Potential automation: 30–60%
Potential savings: ₹100–460 Cr annually
🧠 How It Works
1. Web Scraping

The bot scrapes Dell support pages using:

requests
BeautifulSoup
2. Document Processing

Scraped content is:

cleaned
converted into LangChain documents
chunked into smaller semantic sections

Chunk configuration:

chunk_size = 1200
chunk_overlap = 200
3. Embedding Generation

Each chunk is converted into vector embeddings using:

sentence-transformers/all-MiniLM-L6-v2
4. Vector Storage

Embeddings are stored inside a FAISS vector database for fast semantic retrieval.

5. Retrieval

When a user asks a question:

query embedding is generated
top 4 most relevant chunks are retrieved
search_kwargs={"k":4}
6. Response Generation

Gemini 2.5 Flash receives:

user query
retrieved context

and generates a grounded answer with citations.

🖥️ Example Queries
Battery not charging
WiFi not working
Blue screen after update
Laptop overheating
BIOS update help
No audio issue
Monitor not detected
Dell docking station issue
📂 Installation
Clone Repository
git clone <your-repo-link>
cd dell-rag-support-bot
Install Dependencies
pip install -r requirements.txt
Setup Environment Variables

Create .env

GOOGLE_API_KEY=your_api_key
Run Application
streamlit run app.py
