# New model/dataset detection on Hugging Face. Daily 12:00 UTC.
import requests, json
from typing import List, Dict

def search_models(keywords: List[str], limit: int = 20) -> List[Dict]:
    results = []
    for kw in keywords:
        try:
            r = requests.get(f"https://huggingface.co/api/models?search={kw}&limit={limit}", timeout=30)
            if r.ok:
                results.extend(r.json())
        except Exception:
            pass
    return results
