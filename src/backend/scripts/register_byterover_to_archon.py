"""
Small utility to attach Byterover memory metadata to an Archon task via MCP JSON-RPC.
Usage:
    # Explicit MCP URL
    python register_byterover_to_archon.py --mcp http://127.0.0.1:8054/mcp --task-id <task_id> --memory-id <memory_id>

    # Or rely on environment variables (recommended):
    set ARCHON_MCP_PORT=8054
    python register_byterover_to_archon.py --task-id <task_id> --memory-id <memory_id>

This is intentionally minimal: it performs a JSON-RPC `create_task` or `update_task` call to add a `memories` field on the task. If `--mcp` is omitted, the script will read `ARCHON_MCP_URL` or build the URL from `ARCHON_MCP_PORT`.
"""
"""
usage: python register_byterover_to_archon.py --mcp http://127.0.0.1:8054/mcp --task-id <task_id> --memory-id <memory_id>

You can omit --mcp and instead set environment variables:
    ARCHON_MCP_URL  - full MCP URL (e.g. http://127.0.0.1:8054/mcp)
    ARCHON_MCP_PORT - port to construct default URL (default: 8054)
"""
import argparse
import json
import sys
import os
import urllib.parse
from urllib.request import Request, urlopen
from pathlib import Path
from typing import Optional


def call_mcp(url, method, params=None, id_=None):
    payload = {"jsonrpc": "2.0", "method": method, "params": params or {}, "id": id_ or 1}
    data = json.dumps(payload).encode("utf-8")
    req = Request(url, data=data, headers={"Content-Type": "application/json"})
    with urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def search_byterover(byterover_api: Optional[str], title: Optional[str] = None, tags: Optional[str] = None):
    """Search a Byterover HTTP endpoint for a memory matching title or tags.

    This function assumes the Byterover service exposes a simple search GET
    endpoint at {byterover_api}/search?q=<query> that returns a JSON array of
    objects with at least an `id` field. If no API URL is provided or the
    response is unexpected, returns None.
    """
    if not byterover_api:
        return None
    q = ''
    if title:
        q = title
    if tags:
        if q:
            q += ' '
        q += tags.replace(',', ' ')
    if not q:
        return None
    url = byterover_api.rstrip('/') + '/search?q=' + urllib.parse.quote(q)
    try:
        req = Request(url, headers={"Accept": "application/json"})
        with urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                return data[0].get('id')
    except Exception:
        return None
    return None


def persist_manifest(manifest_path: str, project_id: str, task_id: str, memory_id: str):
    path = Path(manifest_path)
    obj = {}
    if path.exists():
        try:
            obj = json.loads(path.read_text())
        except Exception:
            obj = {}
    proj = obj.setdefault(project_id, {})
    tasks = proj.setdefault('tasks', {})
    tasks[task_id] = tasks.get(task_id, [])
    if memory_id not in tasks[task_id]:
        tasks[task_id].append(memory_id)
    path.write_text(json.dumps(obj, indent=2))


def attach_memory(mcp_url, task_id, memory_id):
    # For mock we call create_task with a link; in real Archon you'd call update_task
    params = {
        "task_id": task_id,
        "updates": {"memories": [{"id": memory_id, "source": "byterover"}]}
    }
    return call_mcp(mcp_url, "update_task", params, id_=int(task_id.split('-')[-1]) if '-' in task_id else 2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mcp', required=False, help='MCP URL (e.g. http://archon-xl:8054/mcp). If omitted, will read ARCHON_MCP_URL or construct from ARCHON_MCP_PORT')
    parser.add_argument('--task-id', required=True)
    parser.add_argument('--memory-id', required=False, help='Byterover memory id to attach')
    parser.add_argument('--byterover-api', required=False, help='Optional Byterover HTTP API base URL for searching memories')
    parser.add_argument('--search-title', required=False, help='Optional title to search in Byterover')
    parser.add_argument('--search-tags', required=False, help='Optional comma-separated tags to search in Byterover')
    parser.add_argument('--manifest-path', required=False, default='byterover_manifest.json', help='Path to JSON manifest to persist links')
    args = parser.parse_args()
    mem_id = args.memory_id
    # If memory id not provided, optionally search Byterover
    if not mem_id and (args.search_title or args.search_tags):
        byterover_api = args.byterover_api or os.environ.get('BYTEROVER_API')
        if byterover_api:
            mem_id = search_byterover(byterover_api, args.search_title, args.search_tags)
        else:
            mem_id = None
        if mem_id:
            print('Found Byterover memory id:', mem_id)

    if not mem_id:
        print('No memory id provided or found. Use --memory-id or --search-title/--search-tags with --byterover-api', file=sys.stderr)
        sys.exit(2)

    # Determine MCP URL from args or environment
    mcp_url = args.mcp or os.environ.get('ARCHON_MCP_URL')
    if not mcp_url:
        port = os.environ.get('ARCHON_MCP_PORT', '8054')
        mcp_url = f'http://127.0.0.1:{port}/mcp'

    try:
        resp = attach_memory(mcp_url, args.task_id, mem_id)
        print(json.dumps(resp, indent=2))
        # persist mapping
        try:
            persist_manifest(args.manifest_path, resp.get('result', {}).get('project', args.task_id.split('-')[0] if '-' in args.task_id else 'project'), args.task_id, mem_id)
            print('Persisted manifest to', args.manifest_path)
        except Exception as e:
            print('manifest persist error:', e, file=sys.stderr)
    except Exception as e:
        print('error:', e, file=sys.stderr)
        sys.exit(1)
