const express = require('express');
const bodyParser = require('body-parser');
const app = express();
app.use(bodyParser.json());

// Simple request logger for debugging MCP client interactions
app.use((req, res, next) => {
  if (req.path === '/mcp') {
    try {
      console.log('--- /mcp request ---');
      console.log('method:', req.method);
      console.log('headers:', JSON.stringify(req.headers));
      console.log('query:', JSON.stringify(req.query));
      console.log('body:', JSON.stringify(req.body));
    } catch (err) {
      console.log('logger error', err);
    }
  }
  next();
});

app.get('/mcp', (req, res) => {
  // Return a basic MCP handshake the mcp-remote client expects.
  const protocolVersion = '1.0';
  const capabilities = {
    jsonrpc: true,
    streaming: false,
    health_check: true,
    create_project: true,
    create_task: true,
  };
  const serverInfo = { name: 'mock-archon', version: '0.1.0', uptime: process.uptime() };
  const payload = {
    protocolVersion,
    capabilities,
    serverInfo,
    // compatibility aliases
    result: { protocolVersion, capabilities, serverInfo },
    info: serverInfo,
    server: serverInfo,
  };
  res.setHeader('Content-Type', 'application/json');
  res.json(payload);
});

// Respond to preflight or simple probes
app.options('/mcp', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.json({ ok: true });
});

app.post('/mcp', (req, res) => {
  // Support MCP JSON-RPC style requests (jsonrpc: "2.0")
  const body = req.body || {};
  if (body.jsonrpc === '2.0' && body.method) {
    const id = body.id ?? Math.floor(Date.now() / 1000);
    const method = body.method;
    // simple handlers
    if (method === 'handshake' || method === 'get_server_info') {
      const protocolVersion = '1.0';
      const capabilities = {
        jsonrpc: true,
        streaming: false,
        health_check: true,
        create_project: true,
        create_task: true,
      };
      const serverInfo = { name: 'mock-archon', version: '0.1.0', uptime: process.uptime() };
      const result = { protocolVersion, capabilities, serverInfo };
      return res.json({ jsonrpc: '2.0', id, result });
    }
    // Support mcp-remote initialize handshake which sends client protocolVersion and expects server protocol info
    if (method === 'initialize') {
      const protocolVersion = '2025-06-18';
      const capabilities = {
        jsonrpc: true,
        streaming: false,
        health_check: true,
        create_project: true,
        create_task: true,
      };
      const serverInfo = { name: 'mock-archon', version: '0.1.0', uptime: process.uptime() };
      const result = { protocolVersion, capabilities, serverInfo };
      return res.json({ jsonrpc: '2.0', id, result });
    }
    if (method === 'health_check') {
      return res.json({ jsonrpc: '2.0', id, result: { status: 'ok', service: 'mock-archon' } });
    }
    if (method === 'list_projects') {
      return res.json({ jsonrpc: '2.0', id, result: { projects: [] } });
    }
    if (method === 'create_project') {
      const title = body.params?.title || body.params?.name || 'mock-project';
      const project = { id: 'mock-project-' + Date.now(), title };
      return res.json({ jsonrpc: '2.0', id, result: { success: true, project } });
    }
    if (method === 'create_task') {
      const task = { id: 'mock-task-' + Date.now(), title: body.params?.title || 'task' };
      return res.json({ jsonrpc: '2.0', id, result: { success: true, task } });
    }
    // default json-rpc echo
    return res.json({ jsonrpc: '2.0', id, result: { received: true, method, params: body.params } });
  }

  // Backwards-compatible simple REST-style body handling
  const action = req.body?.action || req.query?.action;
  if (action === 'create_project') {
    return res.json({ success: true, project_id: 'mock-project-' + Date.now() });
  }
  if (action === 'list_projects') {
    return res.json({ success: true, projects: [] });
  }
  return res.json({ success: true, received: true, body: req.body });
});

const port = process.env.PORT || 8054;
app.listen(port, () => console.log(`mock-archon listening on port ${port}`));
