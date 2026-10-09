"""Authenticated control interface for nodes."""
from __future__ import annotations
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .registry.model import NodeRecord
from .registry.enrollment import NodeEnroller
import os, hmac, hashlib, time

app = FastAPI(title="Unicorn Quantum Node API", version="1.0.0")
security = HTTPBearer(auto_error=False)
enroller = NodeEnroller()

API_KEY = os.environ.get("NODE_API_KEY", "local-dev-only-key")

def verify_auth(credentials: HTTPAuthorizationCredentials | None = Depends(security)):
    if credentials is None or not hmac.compare_digest(credentials.credentials, API_KEY):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@app.post("/nodes/register")
def register_node(node: NodeRecord, auth: bool = Depends(verify_auth)):
    enroller.register(node)
    return {"status": "registered", "node_id": node.node_id}

@app.get("/nodes/{node_id}")
def get_node(node_id: str, auth: bool = Depends(verify_auth)):
    node = enroller.get(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": time.time()}
