This folder contains saved MCP handshake responses captured from local and containerized runs of the `mock-archon` server.

Files
- `mcp_response_local.json` - handshake captured from a locally-run `node server.js` instance.
- `mcp_response_container.json` - handshake captured from the dockerized mock started via `docker compose -f docker-compose.mock.yml up`.

Regenerating fixtures
1. Start local mock:
   - PowerShell (preferred):
     ```powershell
     cd mock-archon
     Start-Process node -ArgumentList 'server.js' -PassThru
     # then use Invoke-WebRequest to GET http://127.0.0.1:8054/mcp and save the body
     ```
2. Or start dockerized mock (recommended for CI parity):
   ```powershell
   cd <repo-root>
   docker compose -f docker-compose.mock.yml up --build -d
   Invoke-WebRequest -Uri http://127.0.0.1:8054/mcp -UseBasicParsing | Select-Object -ExpandProperty Content | Out-File tests/fixtures/mcp_response_container.json -Encoding utf8
   docker compose -f docker-compose.mock.yml down --volumes
   ```

Test note: The contract test `tests/test_mcp_contract.py` uses a retry loop and respects `ARCHON_MCP_PORT` and `MCP_START_TIMEOUT` environment variables.
