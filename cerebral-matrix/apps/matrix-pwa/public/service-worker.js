/* Offline service worker — cache-first for app shell, network-only for opt-in telemetry.
   No telemetry by default. Every outbound request is opt-in. */
const CACHE_NAME = 'matrix-os-v1';
const APP_SHELL = ['/', '/index.html', '/manifest.webmanifest'];

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(APP_SHELL)));
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
    ))
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // Opt-in telemetry: never cache or intercept /telemetry unless explicitly enabled
  if (event.request.url.includes('/telemetry')) {
    event.respondWith(fetch(event.request).catch(() => new Response('offline', {status: 503})));
    return;
  }
  // Cache-first for everything else (offline-first)
  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request).then(resp => {
      const clone = resp.clone();
      caches.open(CACHE_NAME).then(c => c.put(event.request, clone));
      return resp;
    }).catch(() => caches.match('/index.html')))
  );
});
