# CLAUDE.md

## Project Overview

**test_20** - FastAPI application generated with [Full-Stack AI Agent Template](https://github.com/vstorm-co/full-stack-ai-agent-template).

**Stack:** FastAPI + Pydantic v2, PostgreSQL (async), JWT auth, Redis, PydanticAI, RAG (milvus), Celery, Next.js 15

## Commands

```bash
# Backend
cd backend
uv run uvicorn app.main:app --reload --port 8000
pytest
ruff check . --fix && ruff format .

# Database
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "Description"

# Frontend
cd frontend
bun dev
bun test

# Docker
docker compose up -d

# RAG
uv run test_20 rag-collections
uv run test_20 rag-ingest /path/to/file.pdf --collection docs
uv run test_20 rag-search "query" --collection docs
uv run test_20 rag-sync-gdrive --collection docs
```

## Project Structure

```
backend/app/
├── api/routes/v1/    # HTTP endpoints
├── services/         # Business logic
├── repositories/     # Data access
├── schemas/          # Pydantic models
├── db/models/        # Database models
├── core/config.py    # Settings
├── agents/           # AI agents
├── rag/              # RAG (embeddings, vector store, ingestion)
└── commands/         # CLI commands
```

## Key Conventions

- Use `db.flush()` in repositories (not `commit`)
- Services raise domain exceptions (`NotFoundError`, `AlreadyExistsError`)
- Schemas: separate `Create`, `Update`, `Response` models
- Commands auto-discovered from `app/commands/`
- Document ingestion via CLI only (not API)

## Environment Variables

Key variables in `.env`:
```bash
ENVIRONMENT=local
POSTGRES_HOST=localhost
POSTGRES_PASSWORD=secret
SECRET_KEY=change-me-use-openssl-rand-hex-32
LOGFIRE_TOKEN=your-token
MILVUS_HOST=localhost
MILVUS_PORT=19530
```
