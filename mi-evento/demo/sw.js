// Agenda Ilusión: works offline after the first visit; always tries the network first so updates show right away.
const C = 'agenda-v2';
self.addEventListener('install', e => { self.skipWaiting(); e.waitUntil(caches.open(C).then(c => c.addAll(['./', 'manifest.json', 'icon-seal.webp', 'icon-192.png']))); });
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(fetch(e.request).then(r => { if (r.ok && new URL(e.request.url).origin === location.origin) { const k = r.clone(); caches.open(C).then(c => c.put(e.request, k)); } return r; })
    .catch(() => caches.match(e.request).then(r => r || caches.match('./'))));
});
