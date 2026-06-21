# 📄 RAG Document Intelligence System

An end-to-end Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask natural language questions grounded in the uploaded document content.

The system extracts text from PDFs, creates semantic embeddings, stores them in a FAISS vector database, retrieves relevant context for user queries, and generates grounded responses using Llama 3.3 70B via the Groq API.

---

## 🚀 Features

### Document Upload & Processing

* Upload PDF documents through FastAPI endpoints
* Automatic text extraction using PyMuPDF (fitz)
* Page-wise document processing
* Sliding window chunking with overlap
* Semantic embedding generation using Sentence Transformers
* FAISS vector database creation and persistence

### Retrieval-Augmented Generation (RAG)

* Query embedding generation
* Semantic similarity search using FAISS
* Top-K relevant chunk retrieval
* Context-aware prompt construction
* Grounded answer generation using Llama 3.3 70B
* Hallucination reduction through retrieval-based context injection

### API Features

* FastAPI-based REST API
* Pydantic request/response validation
* Health check endpoint
* Document upload endpoint
* Question-answering endpoint
* Dynamic document loading using document IDs
* Error handling and validation

### Persistence

* Persistent FAISS vector storage
* Metadata persistence
* Document-based indexing
* Multiple document support

---

# 🏗️ System Architecture

```text
PDF Upload
    │
    ▼
Text Extraction (PyMuPDF)
    │
    ▼
Chunk Creation
(500 chars, 50 overlap)
    │
    ▼
Embedding Generation
(all-MiniLM-L6-v2)
    │
    ▼
FAISS Vector Database
    │
    ▼
Save Index + Metadata
    │
    ▼
───────────────────────────
User Question
    │
    ▼
Query Embedding
    │
    ▼
FAISS Similarity Search
    │
    ▼
Retrieve Relevant Chunks
    │
    ▼
Prompt Construction
    │
    ▼
Llama 3.3 70B (Groq)
    │
    ▼
Grounded Answer
```

---

# 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn

### RAG Components

* Sentence Transformers
* FAISS
* Groq API
* Llama 3.3 70B Versatile

### Document Processing

* PyMuPDF (fitz)

### Validation

* Pydantic

### Persistence

* Pickle
* Local File Storage

---

# 📂 Project Structure

```text
RAG_DOCUMENT_INTELLIGENCE/
│
├── api.py
│
├── uploads/
│
├── vector_db/
│
├── src/
│   │
│   ├── pdf_loader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── vector_search.py
│   ├── prompt.py
│   ├── llm.py
│   ├── rag_pipeline.py
│   ├── ingestion_pipeline.py
│   └── schemas.py
│
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ RAG Pipeline

## 1. PDF Loading

The uploaded PDF is processed using PyMuPDF.

Output:

```python
[
    {
        "page_num": 1,
        "text": "Page content"
    }
]
```

---

## 2. Chunking Strategy

### Chunk Size

```python
500
```

### Chunk Overlap

```python
50
```

### Why Overlap?

Chunk overlap helps preserve context across chunk boundaries and improves retrieval quality.

Example:

```text
Chunk 1:
Characters 0-500

Chunk 2:
Characters 450-950
```

---

## 3. Embedding Generation

Model:

```python
all-MiniLM-L6-v2
```

Embedding Dimension:

```text
384
```

Each chunk is converted into a dense semantic vector representation.

---

## 4. Vector Database

FAISS Index Type:

```python
IndexFlatL2
```

Used for efficient semantic similarity search.

---

## 5. Retrieval

For each user query:

1. Query is converted into embeddings
2. Similar chunks are retrieved from FAISS
3. Top-K chunks are returned

Current:

```python
top_k = 5
```

---

## 6. Prompt Engineering

Retrieved chunks are injected into a controlled prompt template.

Example Structure:

```text
Context:
[Retrieved Chunks]

Question:
[User Query]

Answer:
```

The LLM is instructed to answer only from the provided context.

---

# 🔌 API Endpoints

---

## Home Endpoint

```http
GET /
```

Response:

```json
{
    "message": "RAG System is Running."
}
```

---

## Health Check

```http
GET /health
```

Response:

```json
{
    "status": "healthy"
}
```

---

## Upload Document

```http
POST /upload
```

Accepts:

* PDF file

Response:

```json
{
    "document_id": "abc12345",
    "message": "Document processed successfully.",
    "num_chunks": 128
}
```

---

## Ask Question

```http
POST /ask
```

Request:

```json
{
    "document_id": "abc12345",
    "query": "What is this document about?"
}
```

Response:

```json
{
    "answer": "..."
}
```

---

# 🧠 Design Decisions

### Why FAISS?

* Fast similarity search
* Lightweight
* Easy persistence
* Industry-standard vector retrieval

### Why Sentence Transformers?

* Strong semantic understanding
* Lightweight compared to larger embedding models
* Suitable for local inference

### Why Llama 3.3 70B via Groq?

* High-quality generation
* Fast inference
* Suitable for RAG workloads

### Why Load Models at Startup?

Embedding model and Groq client are loaded once during FastAPI startup to reduce latency and avoid repeated initialization overhead.

---

# 🧪 Validation & Error Handling

Implemented:

* Empty file validation
* PDF-only uploads
* Missing document validation
* Missing vector database validation
* Missing metadata validation
* Empty query prevention
* Empty chunk handling

---

# 📈 Future Improvements

### Retrieval Improvements

* Similarity score filtering
* Retrieval thresholding
* Hybrid search (BM25 + Vector Search)
* Re-ranking

### Document Support

* DOCX support
* TXT support
* Markdown support

### RAG Enhancements

* Source citations
* Page references
* Confidence scores
* Conversational memory

### Production Improvements

* Background document processing
* Async ingestion pipeline
* Redis caching
* User authentication
* Multi-user document isolation
* Cloud storage integration

---

# 🎯 Learning Outcomes

Through this project, the following concepts were implemented manually and understood from first principles:

* Retrieval-Augmented Generation (RAG)
* Document ingestion pipelines
* PDF text extraction
* Chunking strategies
* Embedding generation
* Vector databases (FAISS)
* Semantic search
* Prompt engineering
* Large Language Model integration
* FastAPI API development
* Pydantic validation
* Persistent storage
* Modular project architecture
* End-to-end AI application development

---

# 👨‍💻 Author

**Abhijith E S**

AI/ML Engineer | Generative AI Developer

This project was manually implemented from scratch for learning purposes to gain a deep understanding of Retrieval-Augmented Generation systems, vector databases, semantic retrieval, and production-style AI application architecture.
