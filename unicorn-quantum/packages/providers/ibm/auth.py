"""IAM token auth + auto-refresh."""
from __future__ import annotations
import time, os
from dataclasses import dataclass
from typing import Optional

@dataclass
class IBMAuthToken:
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: float = 0.0
    instance: Optional[str] = None
    channel: str = "ibm_quantum"

    @property
    def expired(self) -> bool:
        return time.time() > self.expires_at - 60  # refresh 60s early

class IBMAuthManager:
    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token or os.environ.get("IBMQ_API_TOKEN", "")
        self._token: Optional[IBMAuthToken] = None

    def get_token(self) -> Optional[str]:
        if not self.api_token:
            return None
        if self._token is None or self._token.expired:
            self._refresh()
        return self._token.access_token if self._token else None

    def _refresh(self) -> None:
        # In production: call IBM IAM endpoint. Here: store api_token directly.
        self._token = IBMAuthToken(
            access_token=self.api_token,
            expires_at=time.time() + 3600,
            instance=os.environ.get("IBMQ_INSTANCE"),
            channel=os.environ.get("IBMQ_CHANNEL", "ibm_quantum"),
        )
