## 🛠️ Tech Stack

<p align="left">
  <img src="https://skillicons.dev/icons?i=python,flask,html,css,js,git,github,docker" />
</p>

### 🤖 AI / RAG

- Google Gemini
- Gemini Embeddings
- FAISS Vector Database
- Retrieval-Augmented Generation (RAG)

### 🔧 Development

- Python
- Flask
- REST API
- Git & GitHub
- Docker
# EATM Student Assistant

An AI-powered student assistant prototype for Einstein Academy of Technology and Management (EATM).

The system combines Flask, Google Gemini, FAISS vector search, and a curated local knowledge base to provide grounded answers to EATM-specific questions while also handling general academic questions.

> **Important:** This is an independently developed student project prototype. It is not an official EATM application and does not connect to live college databases or student records.

---

## 🚀 Features

* AI-powered student assistant
* Retrieval-Augmented Generation (RAG)
* FAISS-based vector search
* Google Gemini integration
* Gemini embeddings
* Curated EATM knowledge base
* EATM-specific query routing
* General academic question handling
* Session-based conversation context
* Protected knowledge-base ingestion endpoint
* Request validation
* Security headers
* Error handling and logging
* Automated API tests
* Responsive student-friendly web interface
* Docker configuration for optional containerization

---

## 🏗️ Architecture

```text
                         Student
                            |
                            v
                    Web Interface
                            |
                            v
                     Flask REST API
                            |
                  +---------+---------+
                  |                   |
                  v                   v
            Query Router       Session Service
                  |
           +------+------+
           |             |
           v             v
    EATM-specific    General Academic
       Question         Question
           |                 |
           v                 v
      Embedding            Gemini
           |
           v
      FAISS Search
           |
           v
   Retrieved Context
           |
           v
         Gemini
           |
           v
    Grounded Answer
```

---

## 🧠 RAG Pipeline

For EATM-specific questions, the application follows this process:

```text
Student Question
       |
       v
Query Classification
       |
       v
Generate Embedding
       |
       v
FAISS Similarity Search
       |
       v
Retrieve Relevant Documents
       |
       v
Build Grounded Prompt
       |
       v
Google Gemini
       |
       v
Student Answer
```

The assistant is instructed not to invent EATM-specific information when the requested information is not available in the knowledge base.

---

## 📚 Knowledge Base

The knowledge base is organized into the following categories:

```text
knowledge/
├── college/
├── departments/
├── examinations/
├── admissions/
├── facilities/
├── hostel/
├── placements/
├── regulations/
└── notices/
```

The ingestion script:

```text
scripts/ingest.py
```

reads the Markdown documents, divides them into chunks, generates embeddings, and creates the local FAISS vector store.

Generated files:

```text
data/vector_store/
├── index.faiss
└── documents.json
```

---

## 🛠️ Technologies

### Backend

* Python
* Flask
* Gunicorn

### AI

* Google Gemini
* Google GenAI SDK
* Gemini Embeddings

### Retrieval

* FAISS
* NumPy

### Frontend

* HTML
* CSS
* JavaScript

### Testing

* pytest

### Containerization

* Docker
* Docker Compose

---

## 📂 Project Structure

```text
student_assistant/
│
├── app/
│   ├── routes/
│   │   ├── admin.py
│   │   ├── chat.py
│   │   └── health.py
│   │
│   ├── services/
│   │   ├── embedding_service.py
│   │   ├── llm_service.py
│   │   ├── query_router.py
│   │   ├── rag_service.py
│   │   ├── retrieval_service.py
│   │   └── session_service.py
│   │
│   ├── utils/
│   │
│   ├── __init__.py
│   ├── config.py
│   └── extensions.py
│
├── knowledge/
│   ├── college/
│   ├── departments/
│   ├── examinations/
│   ├── admissions/
│   ├── facilities/
│   ├── hostel/
│   ├── placements/
│   ├── regulations/
│   └── notices/
│
├── scripts/
│   └── ingest.py
│
├── static/
│
├── templates/
│   └── index.html
│
├── tests/
│   └── test_api.py
│
├── data/
│   └── vector_store/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 💻 Requirements

Before running the project, install:

* Python 3.12+
* pip
* Git

You also need a Google Gemini API key.

---

## ⚙️ Local Setup

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd student_assistant
```

### 2. Create a Virtual Environment

For Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Use `.env.example` as the template.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
EMBEDDING_MODEL=gemini-embedding-001
EMBEDDING_DIMENSION=768

VECTOR_STORE_PATH=data/vector_store
KNOWLEDGE_DIR=knowledge

TOP_K=5
RAG_DISTANCE_THRESHOLD=1.2
MAX_MESSAGE_LENGTH=4000

ADMIN_TOKEN=your_admin_token

FLASK_DEBUG=true
```

> **Never commit the real `.env` file to GitHub.**

---

## 📖 Build the Knowledge Index

Before starting the application for the first time, run:

```powershell
python scripts/ingest.py
```

This processes the knowledge-base documents and generates:

```text
data/vector_store/index.faiss
data/vector_store/documents.json
```

The generated FAISS index is used during EATM-specific queries.

---

## ▶️ Run the Application

Start the Flask application:

```powershell
python app.py
```

The application will run at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

## 🔌 API Endpoints

### Health Check

```http
GET /api/health
```

Example response:

```json
{
  "status": "ok",
  "service": "EATM Student Assistant"
}
```

### Chat

```http
POST /api/chat
```

Example request:

```json
{
  "message": "What departments are available at EATM?",
  "session_id": "student-session-1"
}
```

The API returns the generated answer and relevant source metadata for RAG responses.

### Admin Knowledge Ingestion

```http
POST /api/admin/ingest
```

The endpoint requires the configured admin token.

Example header:

```http
X-Admin-Token: your_admin_token
```

This endpoint runs the knowledge-base ingestion process.

---

## 🧭 Query Routing

The application separates questions into two categories.

### EATM-Specific Questions

Examples:

```text
What departments are available at EATM?

Tell me about hostel facilities.

What are the examination regulations?
```

These questions follow the RAG pipeline:

```text
Question
   ↓
Embedding
   ↓
FAISS Search
   ↓
Relevant Documents
   ↓
Grounded Prompt
   ↓
Gemini
   ↓
Answer
```

### General Academic Questions

Examples:

```text
What is inheritance in Java?

Explain polymorphism.

What is an operating system?
```

These questions can be answered directly using Gemini without retrieving EATM-specific documents.

---

## 💬 Conversation Context

The application supports session-based conversation context.

A client can provide a `session_id`:

```json
{
  "message": "Explain Java inheritance",
  "session_id": "student-session-1"
}
```

A follow-up question using the same session can refer to the previous conversation.

The current implementation stores conversation history in memory.

Therefore, conversation history is lost when the Flask process restarts.

No external database is currently required.

---

## 🔐 Security

The project includes several basic security measures:

* API keys stored in environment variables
* Protected admin ingestion endpoint
* Request validation
* Maximum message length
* Maximum request size
* Security response headers
* Error handling
* Logging
* `.env` excluded from Git
* Virtual environment excluded from Git

Security headers include:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: no-referrer
Permissions-Policy
```

---

## 🧪 Testing

Run the automated tests with:

```powershell
pytest -v
```

The test suite currently covers:

* Health endpoint
* Empty messages
* Invalid JSON
* Oversized messages
* Unauthorized admin ingestion requests

---

## 🐳 Docker

The repository includes:

```text
Dockerfile
docker-compose.yml
```

These provide an optional containerized setup.

Docker is **not required** for the current local presentation/demo workflow.

The recommended presentation setup is:

```text
Python
   ↓
Flask
   ↓
http://127.0.0.1:5000
```

---

## 🎓 Presentation Demo

For a local presentation:

### 1. Activate the virtual environment

```powershell
venv\Scripts\activate
```

### 2. Start the application

```powershell
python app.py
```

### 3. Open the application

```text
http://127.0.0.1:5000
```

### Suggested demonstration flow

1. Open the Student Assistant.
2. Ask a general academic question.
3. Ask an EATM-specific question.
4. Demonstrate a follow-up question.
5. Ask a question that is not available in the knowledge base.
6. Demonstrate that the assistant does not invent college-specific information.
7. Explain the RAG pipeline.
8. Show the project structure.
9. Run the automated tests.

---

## 🔒 Data and Privacy

This prototype does not implement:

* Student login
* Student personal records
* Live ERP integration
* Payment processing
* WhatsApp integration
* Voice assistant
* Mobile application

The application uses a curated local knowledge base and the Google Gemini API for AI generation and embeddings.

API credentials must remain inside `.env` and must never be committed to GitHub.

---

## ⚠️ Limitations

This project is a prototype intended for academic demonstration and project evaluation.

Current limitations include:

* Knowledge is limited to the curated local documents.
* Information is not automatically synchronized with EATM.
* Session history is stored in memory.
* Current notices and operational information require manual knowledge-base updates.
* No student authentication is implemented.
* No live college database integration is implemented.
* No production hosting is included.

---

## 🔮 Future Improvements

Possible future improvements include:

* Automated official-source synchronization
* Persistent conversation storage
* Student authentication
* Role-based administration
* Improved retrieval ranking
* Hybrid keyword + vector search
* Document versioning
* Background ingestion jobs
* Monitoring and analytics
* Production deployment

---

## 📌 Project Status

**Status:** Student Project Prototype

**Purpose:** AI-powered student assistance and RAG demonstration

**Deployment:** Localhost demonstration

**Architecture:** Flask + Gemini + FAISS + Local Knowledge Base

---

## ⚠️ Disclaimer

This project is an independently developed AI student assistant prototype for academic and project demonstration purposes.

It should not be represented as an official EATM system or as a source of authoritative current college information unless the information has been independently verified from an official source.
