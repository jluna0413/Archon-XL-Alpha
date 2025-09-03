#!/usr/bin/env python3
"""Small MCP -> GitHub adapter to trigger GitHub workflow_dispatch events.

Usage:
  export GITHUB_TOKEN=ghp_...
  python src/mcp_github_adapter.py --repo owner/repo --workflow filename.yml --ref main --inputs '{"task":"run-contract-tests"}'

This script is intentionally minimal: it performs a single authenticated POST to the Actions API.
It accepts JSON inputs and returns the HTTP response code.
"""
import argparse
import json
import os
import sys
from typing import Dict, Optional

import requests


GITHUB_API = "https://api.github.com"


def github_token() -> str:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN environment variable is required")
    return token


def trigger_workflow(repo: str, workflow: str, ref: str, inputs: Optional[Dict] = None) -> int:
    """Trigger a workflow_dispatch for the given workflow file.

    Args:
      repo: 'owner/repo'
      workflow: filename of the workflow (e.g., 'mcp-trigger.yml')
      ref: branch or tag name to run the workflow on
      inputs: optional dict of inputs to pass to the workflow

    Returns: HTTP status code (201 expected for accepted dispatch)
    """
    token = github_token()
    url = f"{GITHUB_API}/repos/{repo}/actions/workflows/{workflow}/dispatches"
    payload = {"ref": ref}
    if inputs:
        payload["inputs"] = inputs
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    return resp.status_code


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True, help="owner/repo")
    p.add_argument("--workflow", required=True, help="workflow filename in .github/workflows/")
    p.add_argument("--ref", default="main", help="branch or tag to run on")
    p.add_argument("--inputs", default="", help="JSON string of inputs")
    args = p.parse_args(argv)

    inputs = None
    if args.inputs:
        try:
            inputs = json.loads(args.inputs)
        except Exception as e:
            print(f"Invalid inputs JSON: {e}")
            sys.exit(2)

    code = trigger_workflow(args.repo, args.workflow, args.ref, inputs)
    if code in (200, 201, 202):
        print(f"Dispatched workflow {args.workflow} on {args.repo}@{args.ref} (status {code})")
        sys.exit(0)
    print(f"Failed to dispatch workflow: HTTP {code}")
    sys.exit(3)


if __name__ == '__main__':
    main()
