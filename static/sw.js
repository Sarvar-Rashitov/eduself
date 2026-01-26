// Service Worker for EduSelf PWA
const CACHE_NAME = 'eduself-v2.1';
const OFFLINE_CACHE = 'eduself-offline-v1';

// URLs to cache for offline functionality
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/css/desktop.css',
  '/static/js/desktop.js',
  '/static/manifest.json',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
  // Core pages - cache actual content
  '/subjects/',
  '/certificates/',
  '/mock_exams/',
  '/institutions/',
  '/courses/',
  '/news/',
];

// Install event
self.addEventListener('install', (event) => {
  console.log('Service Worker installing...');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('Caching app shell...');
      return cache.addAll(urlsToCache);
    })
  );
  self.skipWaiting();
});

// Activate event
self.addEventListener('activate', (event) => {
  console.log('Service Worker activating...');
  const cacheWhitelist = [CACHE_NAME, OFFLINE_CACHE];
  
  event.waitUntil(
    Promise.all([
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheWhitelist.indexOf(cacheName) === -1) {
              console.log('Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      }),
      self.clients.claim()
    ])
  );
});

// Fetch event with offline support
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }
  
  // Skip chrome-extension and other non-http requests
  if (!event.request.url.startsWith('http')) {
    return;
  }
  
  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        // Return cached version if available
        if (cachedResponse) {
          console.log('Serving from cache:', event.request.url);
          return cachedResponse;
        }
        
        // Try to fetch from network
        return fetch(event.request)
          .then((response) => {
            // Don't cache non-successful responses
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            
            // Clone the response
            const responseToCache = response.clone();
            
            // Cache successful responses
            caches.open(CACHE_NAME)
              .then((cache) => {
                cache.put(event.request, responseToCache);
              });
            
            return response;
          })
          .catch(() => {
            console.log('Network failed for:', event.request.url);
            
            // For navigation requests, return cached page if available
            if (event.request.mode === 'navigate') {
              // Try to return cached version of the same page
              return caches.match(event.request.url)
                .then((cachedPage) => {
                  if (cachedPage) {
                    return cachedPage;
                  }
                  // If no cached version, return home page
                  return caches.match('/');
                });
            }
            
            // For other requests, try to return a cached asset
            return caches.match('/static/icons/icon-192x192.png');
          });
      })
  );
});

// Background sync for when connection is restored
self.addEventListener('sync', (event) => {
  console.log('Background sync triggered:', event.tag);
  
  if (event.tag === 'background-sync') {
    event.waitUntil(
      // Perform background sync tasks
      syncData()
    );
  }
});

// Push notification support
self.addEventListener('push', (event) => {
  console.log('Push notification received');
  
  const options = {
    body: event.data ? event.data.text() : 'Yangi xabar mavjud!',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Ko\'rish',
        icon: '/static/icons/icon-192x192.png'
      },
      {
        action: 'close',
        title: 'Yopish',
        icon: '/static/icons/icon-192x192.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('EduSelf', options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
  console.log('Notification clicked:', event.action);
  
  event.notification.close();
  
  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Helper function for background sync
async function syncData() {
  try {
    // Sync cached data when connection is restored
    console.log('Syncing data...');
    
    // You can add specific sync logic here
    // For example, sync user progress, test results, etc.
    
    return Promise.resolve();
  } catch (error) {
    console.error('Sync failed:', error);
    return Promise.reject(error);
  }
}

// Network status monitoring
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({ version: CACHE_NAME });
  }
});
