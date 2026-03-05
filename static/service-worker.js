const CACHE_VERSION = 'eduself-v1.0.5';
const STATIC_CACHE = `${CACHE_VERSION}-static`;
const DYNAMIC_CACHE = `${CACHE_VERSION}-dynamic`;
const IMAGE_CACHE = `${CACHE_VERSION}-images`;

// Cache qilinadigan static fayllar
const STATIC_ASSETS = [
  '/',
  '/static/css/style.css',
  '/static/css/base-layout.css',
  '/static/css/pwa-styles.css',
  '/static/js/pwa.js',
  '/manifest.json',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
];

// Service Worker o'rnatish
self.addEventListener('install', (event) => {
  console.log('[SW] Installing Service Worker...', CACHE_VERSION);
  
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      console.log('[SW] Caching static assets');
      return cache.addAll(STATIC_ASSETS).catch(err => {
        console.error('[SW] Failed to cache some assets:', err);
      });
    })
  );
  
  // Yangi SW ni darhol faollashtirish
  self.skipWaiting();
});

// Service Worker faollashtirish
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating Service Worker...', CACHE_VERSION);
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          // Eski cache'larni o'chirish
          if (cacheName !== STATIC_CACHE && 
              cacheName !== DYNAMIC_CACHE && 
              cacheName !== IMAGE_CACHE) {
            console.log('[SW] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  
  // Barcha clientlarni darhol boshqarish
  return self.clients.claim();
});

// Fetch hodisalari - Network First strategiyasi
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Faqat GET so'rovlarini cache qilish
  if (request.method !== 'GET') {
    return;
  }
  
  // API so'rovlari uchun Network First
  if (url.pathname.startsWith('/api/') || 
      url.pathname.includes('/accounts/') ||
      url.pathname.includes('/subscriptions/')) {
    event.respondWith(networkFirst(request));
    return;
  }
  
  // Rasmlar uchun Cache First
  if (request.destination === 'image') {
    event.respondWith(cacheFirstImages(request));
    return;
  }
  
  // Static fayllar uchun Cache First
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(cacheFirst(request));
    return;
  }
  
  // Boshqa barcha so'rovlar uchun Network First
  event.respondWith(networkFirst(request));
});

// Cache First strategiyasi (static fayllar uchun)
async function cacheFirst(request) {
  const cache = await caches.open(STATIC_CACHE);
  const cached = await cache.match(request);
  
  if (cached) {
    return cached;
  }
  
  try {
    const response = await fetch(request);
    if (response.ok) {
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    console.error('[SW] Fetch failed:', error);
    return new Response('Offline', { status: 503 });
  }
}

// Cache First strategiyasi (rasmlar uchun)
async function cacheFirstImages(request) {
  const cache = await caches.open(IMAGE_CACHE);
  const cached = await cache.match(request);
  
  if (cached) {
    return cached;
  }
  
  try {
    const response = await fetch(request);
    if (response.ok) {
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    // Offline placeholder rasm
    return new Response(
      '<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg"><rect fill="#f0f0f0" width="400" height="300"/><text x="50%" y="50%" text-anchor="middle" fill="#999">Offline</text></svg>',
      { headers: { 'Content-Type': 'image/svg+xml' } }
    );
  }
}

// Network First strategiyasi (dinamik kontent uchun)
async function networkFirst(request) {
  const cache = await caches.open(DYNAMIC_CACHE);
  
  try {
    const response = await fetch(request);
    if (response.ok) {
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    const cached = await cache.match(request);
    if (cached) {
      return cached;
    }
    
    // Offline sahifa
    if (request.mode === 'navigate') {
      return caches.match('/offline.html') || new Response(
        `<!DOCTYPE html>
        <html lang="uz">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Offline - EduSelf</title>
          <style>
            body {
              font-family: 'Inter', sans-serif;
              display: flex;
              align-items: center;
              justify-content: center;
              min-height: 100vh;
              margin: 0;
              background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
              color: white;
              text-align: center;
              padding: 20px;
            }
            .offline-container {
              max-width: 400px;
            }
            .offline-icon {
              font-size: 80px;
              margin-bottom: 20px;
            }
            h1 {
              font-size: 28px;
              margin-bottom: 16px;
            }
            p {
              font-size: 16px;
              opacity: 0.9;
              line-height: 1.6;
            }
            .retry-btn {
              margin-top: 24px;
              padding: 12px 32px;
              background: white;
              color: #667eea;
              border: none;
              border-radius: 8px;
              font-size: 16px;
              font-weight: 600;
              cursor: pointer;
              transition: transform 0.2s;
            }
            .retry-btn:hover {
              transform: scale(1.05);
            }
          </style>
        </head>
        <body>
          <div class="offline-container">
            <div class="offline-icon">📡</div>
            <h1>Internet aloqasi yo'q</h1>
            <p>Hozirda internetga ulanish imkoniyati yo'q. Iltimos, internet aloqangizni tekshiring va qaytadan urinib ko'ring.</p>
            <button class="retry-btn" onclick="window.location.reload()">Qayta urinish</button>
          </div>
        </body>
        </html>`,
        { headers: { 'Content-Type': 'text/html' } }
      );
    }
    
    return new Response('Offline', { status: 503 });
  }
}

// Push bildirishnomalar
self.addEventListener('push', (event) => {
  console.log('[SW] Push notification received');
  
  const options = {
    body: event.data ? event.data.text() : 'Yangi bildirishnoma',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-72x72.png',
    vibrate: [200, 100, 200],
    tag: 'eduself-notification',
    requireInteraction: false,
    actions: [
      {
        action: 'open',
        title: 'Ochish',
        icon: '/static/icons/icon-72x72.png'
      },
      {
        action: 'close',
        title: 'Yopish',
        icon: '/static/icons/icon-72x72.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('EduSelf', options)
  );
});

// Bildirishnoma bosilganda
self.addEventListener('notificationclick', (event) => {
  console.log('[SW] Notification clicked:', event.action);
  
  event.notification.close();
  
  if (event.action === 'open') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Background Sync
self.addEventListener('sync', (event) => {
  console.log('[SW] Background sync:', event.tag);
  
  if (event.tag === 'sync-data') {
    event.waitUntil(syncData());
  }
});

async function syncData() {
  // Ma'lumotlarni sinxronlash logikasi
  console.log('[SW] Syncing data...');
}

// Periodic Background Sync (Chrome 80+)
self.addEventListener('periodicsync', (event) => {
  console.log('[SW] Periodic sync:', event.tag);
  
  if (event.tag === 'update-content') {
    event.waitUntil(updateContent());
  }
});

async function updateContent() {
  // Kontentni yangilash
  console.log('[SW] Updating content...');
}

// Message handler (client bilan aloqa)
self.addEventListener('message', (event) => {
  console.log('[SW] Message received:', event.data);
  
  if (event.data.action === 'skipWaiting') {
    self.skipWaiting();
  }
  
  if (event.data.action === 'clearCache') {
    event.waitUntil(
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => caches.delete(cacheName))
        );
      })
    );
  }
});
