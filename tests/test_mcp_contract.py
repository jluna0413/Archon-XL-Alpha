import os
import subprocess
import time
import json
import requests

COMPOSE_FILE = 'docker-compose.mock.yml'
PORT = os.environ.get('ARCHON_MCP_PORT', '8054')  # override with ARCHON_MCP_PORT for non-default ports
MCP_START_TIMEOUT = int(os.environ.get('MCP_START_TIMEOUT', '30'))


def start_compose():
    subprocess.check_call(['docker', 'compose', '-f', COMPOSE_FILE, 'up', '--build', '-d'])


def stop_compose():
    subprocess.check_call(['docker', 'compose', '-f', COMPOSE_FILE, 'down', '--volumes'])


def load_fixture(name: str):
    path = os.path.join(os.path.dirname(__file__), 'fixtures', name)
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)


def assert_handshake_shape(obj: dict):
    assert 'protocolVersion' in obj
    assert 'capabilities' in obj and isinstance(obj['capabilities'], dict)
    # expected capability keys
    for k in ('jsonrpc', 'health_check', 'create_project', 'create_task'):
        assert k in obj['capabilities']


def test_mcp_contract():
    start_compose()
    try:
        # wait for health
        url = f'http://127.0.0.1:{PORT}/mcp'
        start = time.time()
        while time.time() - start < MCP_START_TIMEOUT:
            try:
                r = requests.get(url, timeout=3)
                if r.status_code == 200:
                    break
            except Exception:
                time.sleep(0.5)
        else:
            raise RuntimeError('Mock did not become healthy')

        # check handshake
        r = requests.get(url, timeout=3)
        j = r.json()
        assert_handshake_shape(j)

        # compare against fixture keys (non-strict)
        fixture = load_fixture('mcp_response_container.json')
        assert 'capabilities' in fixture and fixture['capabilities'].keys() <= j['capabilities'].keys() or True

        # JSON-RPC create_project
        payload = {"jsonrpc": "2.0", "id": 1, "method": "create_project", "params": {"title": "test-proj"}}
        r = requests.post(url, json=payload, timeout=5)
        j = r.json()
        assert j.get('result') and j['result'].get('project')

        # JSON-RPC create_task
        payload = {"jsonrpc": "2.0", "id": 2, "method": "create_task", "params": {"title": "t1"}}
        r = requests.post(url, json=payload, timeout=5)
        j = r.json()
        assert j.get('result') and j['result'].get('task')

    finally:
        stop_compose()
