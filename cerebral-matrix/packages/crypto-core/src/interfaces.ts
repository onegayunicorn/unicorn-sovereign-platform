// PQC crypto provider interface — NIST standard algorithms only.
// Never invent crypto. Implementations delegate to liboqs / WebCrypto.
export interface PQCProvider {
  readonly algorithm: 'ML-KEM-768' | 'ML-DSA-65' | 'SLH-DSA-SHA2-128s' | 'HYBRID_KEM_ECDSA';
  generateKeyPair(): Promise<{ publicKey: ArrayBuffer; secretKey: ArrayBuffer }>;
  encapsulate(publicKey: ArrayBuffer): Promise<{ ciphertext: ArrayBuffer; sharedSecret: ArrayBuffer }>;
  decapsulate(secretKey: ArrayBuffer, ciphertext: ArrayBuffer): Promise<ArrayBuffer>;
  sign(secretKey: ArrayBuffer, message: ArrayBuffer): Promise<ArrayBuffer>;
  verify(publicKey: ArrayBuffer, message: ArrayBuffer, signature: ArrayBuffer): Promise<boolean>;
}
