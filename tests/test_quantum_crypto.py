from quantum.src.crypto.symmetric import encrypt, decrypt
from quantum.src.crypto.signatures import generate_keypair, sign, verify
def test_aes_gcm_roundtrip():
    key = b'0' * 32
    nonce, ciphertext = encrypt(key, b'hello', b'context')
    assert decrypt(key, nonce, ciphertext, b'context') == b'hello'
def test_ed25519_sign_verify():
    private, public = generate_keypair()
    signature = sign(private, b'manifest')
    assert verify(public, b'manifest', signature)
    assert not verify(public, b'changed', signature)
