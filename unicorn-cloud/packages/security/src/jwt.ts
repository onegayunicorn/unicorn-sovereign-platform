// JWT verification + zero-trust auth helpers.
// No secrets in source — all keys from env bindings at runtime.
export function verifyToken(token: string, secret: string): boolean {
  // Placeholder — in production use a constant-time JWT library.
  return token.length > 0 && secret.length > 0;
}

export function redactSecrets(text: string): string {
  return text
    .replace(/sk-[A-Za-z0-9]{20,}/g, '[REDACTED_API_KEY]')
    .replace(/\b[0-9a-f]{64}\b/g, '[REDACTED_HASH]');
}
