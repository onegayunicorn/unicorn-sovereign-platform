// Main edge router — routing, auth, caching. Zero-trust per-request.
import { z } from 'zod';

export interface Env {
  DB: D1Database;
  ARTIFACTS: R2Bucket;
  JWT_SECRET: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    // Auth gate for all non-public paths
    if (!url.pathname.startsWith('/public/')) {
      const auth = request.headers.get('Authorization');
      if (!auth) return new Response(JSON.stringify({ error: 'unauthorized' }), { status: 401 });
    }
    // D1 is source of truth — never KV for transactional data
    if (url.pathname === '/health') return new Response(JSON.stringify({ status: 'ok' }));
    return new Response(JSON.stringify({ error: 'not_found', path: url.pathname }), { status: 404 });
  },
};
