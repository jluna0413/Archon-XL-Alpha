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
Use the helper script to attach a Byterover memory ID to an Archon task (calls `update_task` via JSON-RPC). The script will read `ARCHON_MCP_URL` or construct the URL from `ARCHON_MCP_PORT` if `--mcp` is omitted.

```powershell
# Example: attach memory id to mock task (explicit URL)
python ./src/backend/scripts/register_byterover_to_archon.py --mcp http://127.0.0.1:8054/mcp --task-id mock-task-1756838776560 --memory-id byterover-memory-12345

# Or rely on environment variables:
set ARCHON_MCP_PORT=8054
python ./src/backend/scripts/register_byterover_to_archon.py --task-id mock-task-1756838776560 --memory-id byterover-memory-12345
Utilities

- `src/utils/quicksort.js` — in-place iterative quicksort implementation exported as `{ quicksort }`.

Register Byterover memory to Archon tasks

Use the helper script to attach a Byterover memory ID to an Archon task (calls `update_task` via JSON-RPC):

```powershell
# Example: attach memory id to mock task
python ./src/backend/scripts/register_byterover_to_archon.py --mcp http://archon-xl:8054/mcp --task-id mock-task-1756838776560 --memory-id byterover-memory-12345

Local dev helper
----------------
Run `dev-start.ps1` from the repo root to start the local mock-archon, verify the MCP handshake, and run a health_check. Example:

PowerShell:

```powershell
.\dev-start.ps1
```

To add a hosts entry for `archon-xl` (requires Administrator):

```powershell
.\dev-start.ps1 -AddHosts
```
```

Run unit tests (from workspace root):

```powershell
pip install -r requirements.txt
pytest -q src/backend/tests/test_register_byterover.py
```

Environment variables and CI notes
---------------------------------

- `ARCHON_MCP_PORT` — canonical MCP port used by local mock and tests (default: `8054`).
- `ARCHON_MCP_URL` — full MCP URL (overrides `ARCHON_MCP_PORT` if set), e.g. `http://127.0.0.1:8054/mcp`.

CI runner note:
- The included GitHub Actions workflow runs Docker Compose. GitHub-hosted runners may require additional setup for Docker-in-Docker or use of self-hosted runners with privileged access. If your CI fails when starting the compose stack, prefer a self-hosted runner or adjust the runner permissions to allow Docker-in-Docker.
