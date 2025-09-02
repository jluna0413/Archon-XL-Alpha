GitHub MCP Server — quick setup

Priority recommendation: Use the remote GitHub MCP server (https://api.githubcopilot.com/mcp/) when available. It provides OAuth authentication via the IDE, automatic updates, and minimal local setup.

1) Remote (recommended)
- Create a workspace-level file `.mcp.json` (already added to this repo).
- Restart VS Code / Copilot and switch to Agent mode. The IDE should prompt for authentication or use OAuth automatically.

2) Local (Docker) fallback (if remote not available)
- Install Docker Desktop and ensure it's running.
- Generate a GitHub Personal Access Token (PAT) with minimal scopes (repo, workflow if needed).
- Configure a local `.mcp.json` block that runs the GitHub MCP server container with the PAT passed via input or env var.

Example local config (for `.mcp.json`):
{
  "inputs": [
    { "id": "github_pat", "description": "GitHub PAT", "type": "promptString", "password": true }
  ],
  "servers": {
    "github": {
      "type": "stdio",
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${input:github_pat}" }
    }
  }
}

3) VS Code user/global settings note
- Your `cline_mcp_settings.json` is a user-global file (not in repo). It currently references `http://archon-xl:8054/mcp`. Do not overwrite it from the repo. Instead, add a `github` server block in that file pointing to `https://api.githubcopilot.com/mcp/` or to a local command that runs the container.

4) Verification
- Restart IDE, open Copilot Chat, switch to Agent mode, open tool picker and enable `github` tools. Try: "List recent issues in this repository".

5) Security
- Use OAuth via IDE when possible. If using PAT, store it in secret input or OS keychain; avoid committing tokens.

If you want, I can also prepare a safe `cline_mcp_settings.json` snippet you can paste into your user settings to add a `github` entry (I will not modify your user file).
