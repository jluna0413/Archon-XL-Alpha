Phase1 scaffold snapshot for Byterover storage (local fallback)

Phase1 scaffold created in workspace at `a:\dev\Archon-XL-Alpha`.

Files added:
```
README.md
.gitignore
pyproject.toml
requirements.txt
Dockerfile
docker-compose.yml
.github/workflows/ci.yml
.pre-commit-config.yaml
src/backend/app/main.py
src/backend/app/plugins/__init__.py
migrations/create_tables.sql
Phase1_Project_Plan.md (updated)
```

Actions performed:
- Initialized git repo on branch `main` and created initial commit (user: archon-ci).
- Added FastAPI health endpoint (`/health`) and plugin registry endpoints (`/plugins`, `/plugins/register`).
- Created docker-compose with Postgres, Redis, Qdrant, and backend service.

Acceptance criteria status:
- Health endpoint: implemented (FastAPI `/health`) ✅
- Plugin interface scaffold: implemented (`PluginBase`) ✅
- DB schema blueprint: added (`migrations/create_tables.sql`) ✅
- Archon/Byterover persistence: pending (network/auth previously failed) ⚠️

Notes:
- Archon MCP project/task creation and Byterover storage were attempted earlier but failed due to read-timeouts and missing authentication; reattempt requires credentials and available MCP endpoints.
- Next automated steps: run tests/lint, then scaffold RAG memory PoC and plugin adapter.

Context: September 2, 2025. Stored by automated agent after Phase 1 scaffold creation.
