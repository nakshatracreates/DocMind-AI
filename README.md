# DocMind-AI
AI document Q&amp;A system with semantic retrieval and LLM-powered answers.

# DocMind — AI Document Q&A

DocMind is an AI-powered document question-answering system that allows users to upload PDF documents and ask questions about their content.

It uses Retrieval-Augmented Generation (RAG) to retrieve relevant document chunks before generating an answer with an LLM.

## Features

* User registration and login
* Password hashing with bcrypt
* JWT-based authentication
* Protected API endpoints
* PDF document upload
* PDF text extraction
* Intelligent text chunking with overlap
* OpenAI embeddings
* ChromaDB vector storage
* Semantic search for relevant document chunks
* User-based document isolation
* PostgreSQL document and user storage
* AI-generated answers using retrieved context
* Source information returned with answers
* Error handling for common failure cases

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* JWT
* bcrypt
* OpenAI API
* ChromaDB
* PyPDF

## How It Works

```text
User
 ↓
JWT Authentication
 ↓
Upload PDF
 ↓
Extract PDF Text
 ↓
Chunk Document
 ↓
Create Embeddings
 ↓
Store in ChromaDB
 ↓
User asks a question
 ↓
Create Question Embedding
 ↓
Semantic Search in ChromaDB
 ↓
Retrieve Relevant Chunks
 ↓
Build Context
 ↓
LLM generates answer
 ↓
Answer + Sources
```

## RAG Pipeline

DocMind uses a Retrieval-Augmented Generation pipeline.

### 1. Document Processing

When a PDF is uploaded:

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
ChromaDB
```

Each chunk is stored with:

* Embedding
* Original text
* Document ID
* User ID
* Chunk index

### 2. Question Answering

When a user asks a question:

```text
Question
 ↓
Question Embedding
 ↓
ChromaDB Semantic Search
 ↓
Relevant Chunks
 ↓
Context Builder
 ↓
LLM
 ↓
Answer
```

The system retrieves only documents belonging to the authenticated user.

## Database

PostgreSQL stores application-level information such as:

* Users
* Uploaded documents
* Document ownership

ChromaDB stores:

* Document chunks
* Embeddings
* Metadata

## Authentication

DocMind uses JWT authentication.

The authentication flow is:

```text
Register
 ↓
Password Hashing
 ↓
PostgreSQL

Login
 ↓
Verify Password
 ↓
Generate JWT
 ↓
Bearer Token

Protected Endpoint
 ↓
Verify JWT
 ↓
Identify User
 ↓
Allow Request
```

## API Endpoints

| Method | Endpoint            | Purpose                          |
| ------ | ------------------- | -------------------------------- |
| GET    | `/`                 | API status                       |
| POST   | `/register`         | Register a user                  |
| POST   | `/login`            | Login and receive JWT            |
| GET    | `/profile`          | Get authenticated user's profile |
| POST   | `/documents/upload` | Upload and process a PDF         |
| GET    | `/documents`        | Get user's documents             |
| POST   | `/documents/ask`    | Ask questions about documents    |

## Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
```

Configure your PostgreSQL connection in the database configuration.

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd AI-DOCUMENT-ANSWER
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the PostgreSQL database and configure the connection.

Then start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

## Project Structure

```text
AI DOCUMENT ANSWER/
│
├── app/
│   ├── auth.py
│   ├── chunking.py
│   ├── context_builder.py
│   ├── database.py
│   ├── embedding.py
│   ├── genrator.py
│   ├── main.py
│   ├── models.py
│   ├── retriever.py
│   ├── schemas.py
│   └── vector_store.py
│
├── uploads/
├── chroma_db/
├── test_pdf.py
├── requirements.txt
└── README.md
```

## Example

After uploading a document, a user can ask:

```text
What is FastAPI?
```

DocMind retrieves the most relevant chunks from the user's documents and provides an answer based on the retrieved context.

If the answer cannot be found in the retrieved document content, the system is instructed to say that it could not find the answer in the documents.

## What I Learned Building This

This project combines several backend and AI concepts:

* FastAPI API development
* PostgreSQL database management
* SQLAlchemy ORM
* JWT authentication
* Password hashing
* File uploads
* PDF processing
* Text chunking
* Embeddings
* Vector databases
* Semantic search
* RAG pipelines
* LLM integration
* Error handling
* User-based data isolation

## Future Improvements

* Document deletion
* Background document processing
* Improved chunking strategies
* Streaming AI responses
* Better source citations
* Production deployment
* Frontend interface
* More advanced retrieval techniques

