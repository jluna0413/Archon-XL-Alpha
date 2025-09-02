Memory summary — Archon-XL-Alpha (Phase 1)

This document mirrors structured snapshots stored in Byterover memory. It provides a chronological, local reference for recovery, handoff, or auditing.

Snapshot: Add containerized mock and CI contract test
- timestamp: 2025-09-02T23:15:00Z
- action: Add containerized mock and CI contract test
- why: Remote MCP failed; ensure reproducible local & CI verification of MCP JSON-RPC contract.
- what done:
  - Implemented `mock-archon` with /mcp handshake and JSON-RPC `health_check`, `create_project`, `create_task`.
  - Added `dev-start.ps1` to run the mock detached and validate handshake.
  - Wrote `docker-compose.mock.yml` and `tests/test_mcp_contract.py` to automate contract verification.
  - Added `.github/workflows/mcp-contract.yml` to run compose + pytest in CI.
- outcome: Local pytest contract passed after freeing port 8054; CI workflow file fixed for YAML lint.
- commands:
  - `docker compose -f docker-compose.mock.yml up --build -d`
  - `pytest -q tests/test_mcp_contract.py::test_mcp_contract`
  - `docker compose -f docker-compose.mock.yml down --volumes`
- success sample: GET /mcp returned handshake JSON and `health_check` RPC returned `{"status":"ok","service":"mock-archon"}`
- failure sample: initial remote Archon MCP registration failed due to timeouts and schema mismatch; mitigated by local mock.

Snapshot: Periodic progress memory policy — start
- timestamp: 2025-09-02T23:20:00Z
- action: Start periodic progress memory policy
- why: Keep frequent progress snapshots in Byterover to handle agent/LLM/tool switches or API limits.
- policy summary:
  - Each snapshot will include: timestamp, short action summary, why, what was done, outcome, exact commands used, one sample success, one sample failure.
- outcome: The repo now contains this local reference mirroring Byterover entries.

Notes and next steps
- Consider normalizing `.env` variables to canonical ARCHON_* ports (8054) in a separate branch with backups.
- CI runners may require self-hosted or privileged settings for Docker-in-Docker; adjust `.github/workflows/mcp-contract.yml` if using hosted runners.

End of MemorySummary.md
