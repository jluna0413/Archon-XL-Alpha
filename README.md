# Archon-XL-Alpha

Phase 1 artifacts and repo scaffold for Archon-XL-Alpha.

This repository contains a minimal scaffold to validate Phase 1 acceptance criteria:

- Health endpoint for Archon Core API
- Plugin interface scaffold
- Database schema (Postgres) blueprint
- Docker Compose for local dev (Postgres, Redis, Qdrant)
- CI template (GitHub Actions) for lint checks

Quickstart (Windows PowerShell)

```powershell
Set-Location A:\dev\Archon-XL-Alpha
# Start local services
docker compose up -d
# Run the API (from workspace root)
python -m uvicorn src.backend.app.main:app --reload --host 0.0.0.0 --port 8000
# Health: http://localhost:8000/health
```

Next steps

- Approve Phase 1 plan in `Phase1_Project_Plan.md` (already created).
- Provide Archon/Byterover credentials to persist plan and create Archon project/tasks via MCP (optional).
- I will continue by implementing the plugin scaffolds, a minimal workflow runner, and RAG memory proof-of-concept.
