"""Core unit tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from crypto.symmetric import SessionCipher
from crypto.signatures import Signer

def test_aes256_gcm_roundtrip():
    key = SessionCipher.generate_key()
    cipher = SessionCipher(key)
    msg = b"unicorn sovereign test"
    enc = cipher.encrypt(msg, b"ad")
    assert cipher.decrypt(enc) == msg

def test_ed25519_sign_verify():
    signer = Signer()
    msg = b"hello quantum"
    sig = signer.sign(msg)
    assert Signer.verify(signer.public_bytes(), msg, sig)
    assert not Signer.verify(signer.public_bytes(), b"tampered", sig)
