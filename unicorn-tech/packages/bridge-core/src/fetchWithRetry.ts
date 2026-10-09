// Common fetch with auth + exponential backoff retry.
export async function fetchWithRetry(url: string, opts: RequestInit = {}, retries = 3): Promise<Response> {
  let lastErr: unknown;
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const res = await fetch(url, opts);
      if (res.status < 500 || attempt === retries) return res;
    } catch (e) {
      lastErr = e;
      if (attempt === retries) throw e;
    }
    await new Promise(r => setTimeout(r, Math.pow(2, attempt) * 100));
  }
  throw lastErr;
}
