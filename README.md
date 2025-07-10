# RAG Assessment – Chat with Your PDFs

A **Retrieval-Augmented Generation (RAG)** application built with **FastAPI**, **OpenAI**, **FAISS**, and **LangChain**, enabling users to intelligently interact with uploaded documents using Large Language Models (LLMs).

This repository provides a complete backend implementation that fulfills all RAG assessment requirements, including GenAI and Non-GenAI endpoints, containerization, JWT authentication, vector database indexing, and comprehensive test coverage.

---

## 🎯 Objective

Build an end-to-end RAG-based backend application that:
- Accepts and indexes PDF files for intelligent document processing
- Enables chat-based querying with contextual document understanding
- Supports secure user authentication and session management
- Provides scalable document storage and retrieval capabilities

---

## 🔌 API Endpoints

### GenAI APIs (60% Assessment Weight)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/process-document` | POST | Upload and chunk documents; stores embeddings in vector database |
| `/chat` | POST | Process user queries, retrieve relevant context, and generate LLM responses |

### Non-GenAI APIs (40% Assessment Weight)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/get-documents` | GET | Retrieve list of uploaded documents with `doc_id` and `doc_name` |
| `/get-document/{id}` | GET | Fetch specific PDF file using document identifier |
| `/new-chat` | POST | Initialize new chat session (clears context and document history) |
| `/login` | POST | User authentication endpoint returning JWT token |
| `/logout` | POST | Terminate current user session |
| `/register` | POST | Create new user account |
| `/user` | GET | Retrieve current user profile information |
| `/user` | POST | Update user profile details |

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend Framework** | FastAPI | High-performance API development |
| **Language Model** | OpenAI GPT | Natural language processing via `langchain-openai` |
| **Embeddings** | `text-embedding-3-small` | Vector representation of document content |
| **Vector Database** | FAISS | Efficient similarity search and clustering |
| **PDF Processing** | PyMuPDF, PyPDF2 | Document parsing and text extraction |
| **Authentication** | JWT via PyJWT | Secure user session management |
| **Containerization** | Docker + Docker Compose | Consistent deployment environment |
| **Testing Framework** | Pytest | Comprehensive test coverage |

---

## 🚀 Quick Start Guide

### Prerequisites

Ensure you have the following tools installed:

| Tool | Purpose | Installation Guide |
|------|---------|-------------------|
| **Docker + Docker Compose** | Containerized deployment (recommended) | [Docker Installation Guide](https://docs.docker.com/get-docker/) |
| **Git** | Repository management (optional) | [Git Installation Guide](https://git-scm.com/downloads) |
| **Python 3.10+** | Local development (optional) | [Python Installation Guide](https://www.python.org/downloads/) |

> **📝 Note:**  
> - Docker is the recommended deployment method and eliminates the need for local Python installation
> - Tested on macOS (Intel & Apple Silicon), Linux, and Windows 10/11 with WSL 2
> - Ensure port **8000** is available before starting the application

---

### Step 1: Repository Setup

Clone the repository to your local machine:

```bash
git clone <repository-url>
cd rag-assessment
```

### Step 2: Environment Configuration

Create a `.env` file in the project root directory with the following configuration:

```env
OPENAI_API_KEY=your_actual_openai_api_key_here
SECRET_KEY=change_me_to_any_random_long_string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> **🔑 Important:** Replace `your_actual_openai_api_key_here` with your actual OpenAI API key. If you don't have one, see the instructions below.

> **🔐 Security Note:**  
> Choose a strong, random value for `SECRET_KEY`. This key remains private on the server and is critical for JWT token security.

<details>
<summary>📋 <strong>Click here for step-by-step instructions to get your OpenAI API key</strong></summary>

### 📌 Important
Open `config.py` and replace `YOUR_API_KEY_HERE` with your real OpenAI key **before running**.

#### How to Get Your OpenAI API Key

1. **Create an OpenAI Account**
   - Go to [OpenAI's website](https://platform.openai.com)
   - Click "Sign up" if you don't have an account, or "Log in" if you do

2. **Navigate to API Keys**
   - Once logged in, click on your profile icon in the top-right corner
   - Select "View API keys" from the dropdown menu
   - Or directly visit: https://platform.openai.com/api-keys

3. **Create a New API Key**
   - Click the "Create new secret key" button
   - Give your key a descriptive name (e.g., "RAG Assessment Project")
   - Click "Create secret key"

4. **Copy Your API Key**
   - **Important:** Copy the key immediately and store it securely
   - The key will look like: `sk-proj-...` or `sk-...`
   - You won't be able to see it again once you close the dialog

5. **Add Billing Information (Required)**
   - Go to [Billing settings](https://platform.openai.com/account/billing/overview)
   - Add a payment method to use the API
   - Consider setting usage limits to control costs

6. **Paste into .env File**
   - Replace `your_actual_openai_api_key_here` with your actual key
   - Example: `OPENAI_API_KEY=sk-proj-abc123...`

#### 💡 Pro Tips:
- Keep your API key secure and never commit it to version control
- Monitor your usage at https://platform.openai.com/usage
- Start with a low usage limit to avoid unexpected charges
- The API key is case-sensitive, so copy it exactly as shown

</details>

### Step 3: Docker Deployment (Recommended)

Launch the application using Docker Compose:

```bash
docker-compose up --build
```

**Access Points:**
- **API Root:** http://localhost:8000
- **Interactive Documentation:** http://localhost:8000/docs

To stop and clean up containers:

```bash
docker-compose down
```

### Step 4: Local Development (Alternative)

For local development without Docker:

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start development server
uvicorn main:app --reload
```

Access the application at: http://127.0.0.1:8000/docs

### Step 5: First-Time Usage

Follow these steps to get started with the RAG application:

#### 1. User Registration
```http
POST /register
Content-Type: application/json

{
    "username": "alice",
    "password": "strongpassword"
}
```

#### 2. User Authentication
```http
POST /login
Content-Type: application/json

{
    "username": "alice",
    "password": "strongpassword"
}
```

Copy the `token` value from the response.

#### 3. API Authorization
In Swagger UI, click the **Authorize** button and enter:
```
Bearer <your_token_here>
```

#### 4. Document Upload
```http
POST /process-document
Content-Type: multipart/form-data

[Upload PDF file via file field]
```

#### 5. Chat Interaction
```http
POST /chat
Content-Type: application/json

{
    "query": "What is this document about?"
}
```

#### 6. Session Management (Optional)
```http
POST /new-chat
```

---

## 🎉 Success!

You're now ready to intelligently chat with your documents using the RAG application. The system will process your PDFs, create searchable embeddings, and provide contextually relevant responses to your queries.

For additional support or advanced configuration options, please refer to the API documentation available at `/docs` when the application is running.
