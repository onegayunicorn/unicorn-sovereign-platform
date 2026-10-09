"""AES-256-GCM session encryption. NIST-standard AEAD."""
from __future__ import annotations
import os
from dataclasses import dataclass
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

@dataclass
class EncryptedMessage:
    nonce: bytes
    ciphertext: bytes  # includes tag
    associated_data: bytes = b""

class SessionCipher:
    KEY_SIZE = 32  # AES-256
    NONCE_SIZE = 12

    def __init__(self, key: bytes):
        if len(key) != self.KEY_SIZE:
            raise ValueError(f"AES-256 key must be {self.KEY_SIZE} bytes")
        self._aesgcm = AESGCM(key)

    @classmethod
    def generate_key(cls) -> bytes:
        return os.urandom(cls.KEY_SIZE)

    def encrypt(self, plaintext: bytes, associated_data: bytes = b"") -> EncryptedMessage:
        nonce = os.urandom(self.NONCE_SIZE)
        ct = self._aesgcm.encrypt(nonce, plaintext, associated_data)
        return EncryptedMessage(nonce, ct, associated_data)

    def decrypt(self, msg: EncryptedMessage) -> bytes:
        return self._aesgcm.decrypt(msg.nonce, msg.ciphertext, msg.associated_data)
