import json
import pathlib
import importlib.util


def load_module():
    # Load the script as a module by path so tests don't depend on package layout.
    path = pathlib.Path(__file__).resolve().parents[2] / 'backend' / 'scripts' / 'register_byterover_to_archon.py'
    spec = importlib.util.spec_from_file_location('regmod', str(path))
    assert spec is not None
    reg = importlib.util.module_from_spec(spec)
    assert reg is not None
    assert spec.loader is not None
    spec.loader.exec_module(reg)
    return reg


class DummyResp:
    def __init__(self, data_bytes: bytes):
        self._data = data_bytes

    def read(self):
        return self._data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_call_mcp_and_attach_memory(monkeypatch):
    reg = load_module()

    # Fake response for call_mcp
    expected = {"jsonrpc": "2.0", "id": 1, "result": {"ok": True}}

    def fake_urlopen(req):
        return DummyResp(json.dumps(expected).encode('utf-8'))

    # Patch the module's urlopen (the script imports urlopen at module level)
    monkeypatch.setattr(reg, 'urlopen', fake_urlopen)

    resp = reg.call_mcp('http://example', 'some_method', {'a': 1}, id_=1)
    assert resp == expected

    # Now test attach_memory: server will echo back an object; simulate that
    echo = {"jsonrpc": "2.0", "id": 2, "result": {"received": True}}

    def fake_urlopen2(req):
        # ensure request body includes the task_id and memory id
        body = req.data if hasattr(req, 'data') else None
        assert body is not None
        body_obj = json.loads(body.decode('utf-8'))
        assert body_obj['method'] == 'update_task'
        return DummyResp(json.dumps(echo).encode('utf-8'))

    monkeypatch.setattr(reg, 'urlopen', fake_urlopen2)
    out = reg.attach_memory('http://example', 'mock-task-123', 'byterover-memory-xyz')
    assert out['result']['received'] is True


def test_search_and_persist(monkeypatch, tmp_path):
    reg = load_module()

    # Fake Byterover search returns a list of dicts
    def fake_search_req(req):
        class R:
            def __enter__(self):
                return self

            def __exit__(self, a, b, c):
                return False

            def read(self):
                return json.dumps([{"id": "byterover-foo"}]).encode('utf-8')

        return R()

    monkeypatch.setattr(reg, 'urlopen', fake_search_req)
    mem = reg.search_byterover('http://fake', 'Phase1', 'phase1')
    assert mem == 'byterover-foo'

    # test manifest persistence
    manifest = tmp_path / 'manifest.json'
    reg.persist_manifest(str(manifest), 'proj-1', 'task-1', 'byterover-foo')
    data = json.loads(manifest.read_text())
    assert 'proj-1' in data
    assert 'task-1' in data['proj-1']['tasks']
    assert data['proj-1']['tasks']['task-1'] == ['byterover-foo']
