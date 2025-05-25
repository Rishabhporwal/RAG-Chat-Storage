# RAG Chat Storage Microservice

This project is a FastAPI-based backend microservice designed to store, manage, and retrieve chat sessions and messages for a Retrieval-Augmented Generation (RAG) based chatbot.

It provides RESTful APIs to:

- Create and list chat sessions
- Store and retrieve messages
- Favorite and Rename sessions
- Update timestamps and manage session lifecycles

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **FastAPI** — high-performance web framework
- **SQLAlchemy (Async)** — ORM for database interaction
- **PostgreSQL** — database
- **asyncpg** — PostgreSQL driver
- **Docker + Docker Compose** — containerization

---

## 🧾 Features

- Async support with `asyncpg` + `SQLAlchemy`
- Modular code structure for scalability
- Auto-generated OpenAPI docs via FastAPI
- UUID-based session/message IDs
- Timestamp tracking for session updates
- Pagination support for messages
- Favoriting chat sessions

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/rag-chat-storage.git
cd rag-chat-storage
```

### 2. Create Environment Variables

Create a .env file in the root:

```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/rag_chat
API_KEY=eFfLecsoUuykjI5lgkBp7Ta6j42WCHyK
RATE_LIMIT=10/minute
LOG_LEVEL=INFO
```

### 3. Run with Docker Compose

```bash
docker-compose up --build

```

It will spin up:

- FastAPI app at http://localhost:8000
- PostgreSQL database
- PG Admin Tool

## 📜 API Docs

Once running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI Json: http://localhost:8000/openapi.json

## 🧪 Testing

```bash
pytest

```
