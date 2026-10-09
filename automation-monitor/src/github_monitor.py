# Commit/release detection per repo. Hourly cron + push/release events.
import requests, json, os, time
from typing import List, Dict

def check_repo(repo: str, since_hours: int = 1) -> Dict:
    # repo format: owner/name
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"Authorization": f"token {token}"} if token else {}
    since = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - since_hours * 3600))
    commits = requests.get(f"https://api.github.com/repos/{repo}/commits?since={since}",
                           headers=headers, timeout=30).json()
    releases = requests.get(f"https://api.github.com/repos/{repo}/releases?per_page=5",
                            headers=headers, timeout=30).json()
    return {"repo": repo, "new_commits": len(commits) if isinstance(commits, list) else 0,
            "recent_releases": [r.get("tag_name") for r in releases[:3]] if isinstance(releases, list) else []}

def monitor_all(repos: List[str]) -> List[Dict]:
    return [check_repo(r) for r in repos]
