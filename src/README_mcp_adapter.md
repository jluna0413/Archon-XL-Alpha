MCP → GitHub Adapter

This small adapter sends a `workflow_dispatch` event to GitHub Actions.

Usage example:

1. Create a minimal PAT with `workflow` or `repo` scopes and set it in the environment:

```powershell
$env:GITHUB_TOKEN = 'ghp_...'
python src/mcp_github_adapter.py --repo jluna0413/Archon-XL-Alpha --workflow mcp-contract-ci.yml --ref env-normalize --inputs '{"task":"run-contract-tests"}'
```

Security:
- Store tokens in secrets, not source control.
- Use least-privilege tokens and prefer OIDC when running from Actions.
