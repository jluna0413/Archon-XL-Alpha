from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Archon Core API")

# Simple in-memory plugin registry (scaffold)
class PluginInfo(BaseModel):
    id: str
    name: str
    enabled: bool = True
    config: Dict = {}

plugin_registry: Dict[str, PluginInfo] = {}

@app.get("/health")
async def health():
    return {"status": "ok", "service": "archon-core"}

@app.get("/plugins")
async def list_plugins():
    return list(plugin_registry.values())

@app.post("/plugins/register")
async def register_plugin(info: PluginInfo):
    plugin_registry[info.id] = info
    return {"result": "registered", "id": info.id}
