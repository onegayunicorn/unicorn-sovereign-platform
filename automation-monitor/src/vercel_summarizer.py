# Vercel deployment status summarizer. Daily 13:00 UTC + webhook.
import requests, os
from typing import Dict

def get_deployments(project: str) -> Dict:
    token = os.environ.get("VERCEL_TOKEN", "")
    if not token:
        return {"project": project, "status": "no_token", "deployments": []}
    r = requests.get(f"https://api.vercel.com/v6/deployments?project={project}&limit=10",
                     headers={"Authorization": f"Bearer {token}"}, timeout=30)
    return {"project": project, "status": "ok", "deployments": r.json().get("deployments", []) if r.ok else []}
