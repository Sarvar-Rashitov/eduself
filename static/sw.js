// Service Worker for EduSelf PWA
const CACHE_NAME = 'eduself-v2.0';
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
  // Core pages
  '/subjects/',
  '/certificates/',
  '/mock_exams/',
  '/institutions/',
  '/courses/',
  // Offline fallback pages
  '/offline/',
];

// Offline fallback HTML
const OFFLINE_HTML = `
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Offline - EduSelf</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            text-align: center;
            padding: 20px;
        }
        
        .offline-container {
            max-width: 400px;
            animation: fadeInUp 0.6s ease;
        }
        
        .offline-icon {
            font-size: 4rem;
            margin-bottom: 1.5rem;
            opacity: 0.9;
        }
        
        .offline-title {
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .offline-message {
            font-size: 1rem;
            opacity: 0.9;
            line-height: 1.6;
            margin-bottom: 2rem;
        }
        
        .offline-actions {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        .btn {
            padding: 12px 24px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            background: rgba(255, 255, 255, 0.1);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        
        .btn:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.5);
            transform: translateY(-2px);
        }
        
        .btn-primary {
            background: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.4);
        }
        
        .cached-content {
            margin-top: 2rem;
            padding: 1.5rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }
        
        .cached-title {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .cached-links {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .cached-link {
            color: rgba(255, 255, 255, 0.9);
            text-decoration: none;
            padding: 8px 12px;
            border-radius: 6px;
            transition: background 0.3s ease;
        }
        
        .cached-link:hover {
            background: rgba(255, 255, 255, 0.1);
            color: white;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .connection-status {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 8px 16px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            font-size: 0.8rem;
            backdrop-filter: blur(10px);
        }
        
        .status-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 8px;
            background: #ff4757;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="connection-status">
        <span class="status-dot"></span>
        Offline
    </div>
    
    <div class="offline-container">
        <div class="offline-icon">📚</div>
        <h1 class="offline-title">Internet aloqasi yo'q</h1>
        <p class="offline-message">
            Hozirda internet aloqangiz yo'q. Ba'zi sahifalar cache'dan mavjud bo'lishi mumkin.
        </p>
        
        <div class="offline-actions">
            <button class="btn btn-primary" onclick="window.location.reload()">
                🔄 Qayta urinish
            </button>
            <a href="/" class="btn">🏠 Bosh sahifa</a>
        </div>
        
        <div class="cached-content">
            <h3 class="cached-title">Offline mavjud sahifalar:</h3>
            <div class="cached-links">
                <a href="/" class="cached-link">🏠 Bosh sahifa</a>
                <a href="/subjects/" class="cached-link">📖 Fanlar</a>
                <a href="/certificates/" class="cached-link">🏆 Sertifikatlar</a>
                <a href="/institutions/" class="cached-link">🏛️ Muassasalar</a>
                <a href="/courses/" class="cached-link">🎓 Kurslar</a>
            </div>
        </div>
    </div>
    
    <script>
        // Check connection status
        function updateConnectionStatus() {
            const statusDot = document.querySelector('.status-dot');
            const statusText = document.querySelector('.connection-status');
            
            if (navigator.onLine) {
                statusDot.style.background = '#2ed573';
                statusText.innerHTML = '<span class="status-dot"></span>Online';
                // Auto reload when back online
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                statusDot.style.background = '#ff4757';
                statusText.innerHTML = '<span class="status-dot"></span>Offline';
            }
        }
        
        // Listen for connection changes
        window.addEventListener('online', updateConnectionStatus);
        window.addEventListener('offline', updateConnectionStatus);
        
        // Initial check
        updateConnectionStatus();
        
        // Auto-retry connection every 30 seconds
        setInterval(() => {
            if (!navigator.onLine) {
                fetch('/', { method: 'HEAD', cache: 'no-cache' })
                    .then(() => {
                        window.location.reload();
                    })
                    .catch(() => {
                        console.log('Still offline');
                    });
            }
        }, 30000);
    </script>
</body>
</html>
`;

// Install event
self.addEventListener('install', (event) => {
  console.log('Service Worker installing...');
  event.waitUntil(
    Promise.all([
      caches.open(CACHE_NAME).then((cache) => {
        console.log('Caching app shell...');
        return cache.addAll(urlsToCache);
      }),
      caches.open(OFFLINE_CACHE).then((cache) => {
        console.log('Caching offline page...');
        return cache.put('/offline/', new Response(OFFLINE_HTML, {
          headers: { 'Content-Type': 'text/html' }
        }));
      })
    ])
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
            console.log('Network failed, serving offline page');
            // Return offline page for navigation requests
            if (event.request.mode === 'navigate') {
              return caches.match('/offline/');
            }
            
            // Return cached offline assets
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
