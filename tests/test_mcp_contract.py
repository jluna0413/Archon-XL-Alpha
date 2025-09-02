import os
import subprocess
import time
import requests

COMPOSE_FILE = 'docker-compose.mock.yml'
PORT = os.environ.get('ARCHON_MCP_PORT', '8054')


def start_compose():
    subprocess.check_call(['docker', 'compose', '-f', COMPOSE_FILE, 'up', '--build', '-d'])


def stop_compose():
    subprocess.check_call(['docker', 'compose', '-f', COMPOSE_FILE, 'down', '--volumes'])


def test_mcp_contract():
    start_compose()
    try:
        # wait for health
        url = f'http://127.0.0.1:{PORT}/mcp'
        for _ in range(20):
            try:
                r = requests.get(url, timeout=2)
                if r.status_code == 200:
                    break
            except Exception:
                time.sleep(0.5)
        else:
            raise RuntimeError('Mock did not become healthy')

        # check handshake
        r = requests.get(url, timeout=2)
        j = r.json()
        assert 'protocolVersion' in j

        # JSON-RPC create_project
        payload = {"jsonrpc": "2.0", "id": 1, "method": "create_project", "params": {"title": "test-proj"}}
        r = requests.post(url, json=payload, timeout=2)
        j = r.json()
        assert j.get('result') and j['result'].get('project')

        # JSON-RPC create_task
        payload = {"jsonrpc": "2.0", "id": 2, "method": "create_task", "params": {"title": "t1"}}
        r = requests.post(url, json=payload, timeout=2)
        j = r.json()
        assert j.get('result') and j['result'].get('task')

    finally:
        stop_compose()
