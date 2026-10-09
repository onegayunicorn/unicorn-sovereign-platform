# Discord/Slack/email webhook alerts.
import requests, os, json
from typing import Optional

def notify_discord(message: str, webhook: Optional[str] = None) -> bool:
    url = webhook or os.environ.get("DISCORD_WEBHOOK", "")
    if not url:
        return False
    try:
        requests.post(url, json={"content": message}, timeout=10)
        return True
    except Exception:
        return False

def notify_slack(message: str, webhook: Optional[str] = None) -> bool:
    url = webhook or os.environ.get("SLACK_WEBHOOK", "")
    if not url:
        return False
    try:
        requests.post(url, json={"text": message}, timeout=10)
        return True
    except Exception:
        return False
