"""Ed25519 message signing (RFC 8032)."""
from __future__ import annotations
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

class Signer:
    def __init__(self, private_key: Ed25519PrivateKey | None = None):
        self._private_key = private_key or Ed25519PrivateKey.generate()

    @property
    def public_key(self) -> Ed25519PublicKey:
        return self._private_key.public_key()

    def public_bytes(self) -> bytes:
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw)

    def sign(self, message: bytes) -> bytes:
        return self._private_key.sign(message)

    @staticmethod
    def verify(public_key_bytes: bytes, message: bytes, signature: bytes) -> bool:
        try:
            pk = Ed25519PublicKey.from_public_bytes(public_key_bytes)
            pk.verify(signature, message)
            return True
        except Exception:
            return False
