// StockWise Service Worker for Performance & Offline Capability
const CACHE_NAME = 'stockwise-v1';
const API_CACHE_NAME = 'stockwise-api-v1';

// Assets to cache on install
const STATIC_ASSETS = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json'
];

// API patterns to cache
const API_PATTERNS = [
  new RegExp('/api/analyze/'),
  new RegExp('/api/screener/'),
  new RegExp('/api/market/')
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('StockWise SW: Installing...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('StockWise SW: Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('StockWise SW: Installation complete');
        return self.skipWaiting();
      })
  );
});

// Activate event - cleanup old caches
self.addEventListener('activate', (event) => {
  console.log('StockWise SW: Activating...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => name.startsWith('stockwise-') && name !== CACHE_NAME && name !== API_CACHE_NAME)
            .map((name) => {
              console.log('StockWise SW: Deleting old cache:', name);
              return caches.delete(name);
            })
        );
      })
      .then(() => {
        console.log('StockWise SW: Activation complete');
        return self.clients.claim();
      })
  );
});

// Fetch event - handle requests with caching strategies
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Handle API requests with cache-first strategy (for demo data)
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(handleAPIRequest(request));
    return;
  }

  // Handle static assets with cache-first strategy
  if (request.destination === 'script' || 
      request.destination === 'style' || 
      request.destination === 'image') {
    event.respondWith(handleStaticAsset(request));
    return;
  }

  // Handle navigation requests with network-first strategy
  if (request.mode === 'navigate') {
    event.respondWith(handleNavigation(request));
    return;
  }

  // Default: network first, cache fallback
  event.respondWith(
    fetch(request)
      .then((response) => {
        // Cache successful responses
        if (response.ok) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME)
            .then((cache) => cache.put(request, responseClone));
        }
        return response;
      })
      .catch(() => {
        return caches.match(request);
      })
  );
});

// Handle API requests (cache-first for demo data, network-first for real data)
async function handleAPIRequest(request) {
  const url = new URL(request.url);
  
  try {
    // For screener and analysis endpoints, try cache first (demo data is consistent)
    if (url.pathname.includes('/screener/') || url.pathname.includes('/analyze/')) {
      const cachedResponse = await caches.match(request);
      
      if (cachedResponse) {
        console.log('StockWise SW: Serving API from cache:', url.pathname);
        
        // Fetch fresh data in background for next time
        fetch(request)
          .then((response) => {
            if (response.ok) {
              caches.open(API_CACHE_NAME)
                .then((cache) => cache.put(request, response.clone()));
            }
          })
          .catch(() => {/* Ignore background fetch errors */});
        
        return cachedResponse;
      }
    }

    // Network first for other API requests
    const response = await fetch(request);
    
    if (response.ok) {
      // Cache API responses for offline access
      const responseClone = response.clone();
      const cache = await caches.open(API_CACHE_NAME);
      
      // Set cache expiry based on endpoint
      const headers = new Headers(responseClone.headers);
      if (url.pathname.includes('/screener/') || url.pathname.includes('/analyze/')) {
        headers.set('sw-cache-expires', Date.now() + (5 * 60 * 1000)); // 5 minutes for analysis data
      } else {
        headers.set('sw-cache-expires', Date.now() + (30 * 60 * 1000)); // 30 minutes for other data
      }
      
      const modifiedResponse = new Response(responseClone.body, {
        status: responseClone.status,
        statusText: responseClone.statusText,
        headers: headers
      });
      
      cache.put(request, modifiedResponse);
    }
    
    return response;
  } catch (error) {
    console.log('StockWise SW: Network failed, trying cache for:', url.pathname);
    
    // Network failed, try cache
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      // Check if cached response is expired
      const cacheExpires = cachedResponse.headers.get('sw-cache-expires');
      if (cacheExpires && Date.now() > parseInt(cacheExpires)) {
        console.log('StockWise SW: Cached API response expired:', url.pathname);
      }
      return cachedResponse;
    }
    
    // Return offline fallback for API requests
    return new Response(JSON.stringify({
      error: 'Offline',
      message: 'This feature requires an internet connection. Please check your connection and try again.',
      offline: true
    }), {
      status: 503,
      statusText: 'Service Unavailable',
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Handle static assets (cache-first)
async function handleStaticAsset(request) {
  try {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    throw error;
  }
}

// Handle navigation requests (network-first with offline fallback)
async function handleNavigation(request) {
  try {
    const response = await fetch(request);
    
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    
    return response;
  } catch (error) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return offline page fallback
    return caches.match('/') || new Response(`
      <!DOCTYPE html>
      <html>
        <head>
          <title>StockWise - Offline</title>
          <style>
            body { font-family: system-ui, sans-serif; text-align: center; padding: 50px; }
            .offline-message { max-width: 400px; margin: 0 auto; }
            .retry-btn { background: #3b82f6; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; margin-top: 20px; }
          </style>
        </head>
        <body>
          <div class="offline-message">
            <h1>📊 StockWise</h1>
            <h2>You're Offline</h2>
            <p>Please check your internet connection and try again.</p>
            <button class="retry-btn" onclick="window.location.reload()">Retry</button>
          </div>
        </body>
      </html>
    `, {
      headers: { 'Content-Type': 'text/html' }
    });
  }
}

// Background sync for when connection is restored
self.addEventListener('sync', (event) => {
  console.log('StockWise SW: Background sync triggered:', event.tag);
  
  if (event.tag === 'stockwise-sync') {
    event.waitUntil(
      // Refresh critical data when connection is restored
      refreshCriticalData()
    );
  }
});

async function refreshCriticalData() {
  try {
    // Clear expired cache entries
    const apiCache = await caches.open(API_CACHE_NAME);
    const keys = await apiCache.keys();
    
    for (const request of keys) {
      const response = await apiCache.match(request);
      const expires = response.headers.get('sw-cache-expires');
      if (expires && Date.now() > parseInt(expires)) {
        await apiCache.delete(request);
      }
    }
    
    console.log('StockWise SW: Critical data refresh completed');
  } catch (error) {
    console.error('StockWise SW: Critical data refresh failed:', error);
  }
}

// Message handling for cache management
self.addEventListener('message', (event) => {
  const { type, payload } = event.data;
  
  switch (type) {
    case 'SKIP_WAITING':
      self.skipWaiting();
      break;
      
    case 'GET_CACHE_STATUS':
      getCacheStatus().then((status) => {
        event.ports[0].postMessage({ type: 'CACHE_STATUS', payload: status });
      });
      break;
      
    case 'CLEAR_CACHE':
      clearCache().then(() => {
        event.ports[0].postMessage({ type: 'CACHE_CLEARED' });
      });
      break;
  }
});

async function getCacheStatus() {
  const cacheNames = await caches.keys();
  const status = {};
  
  for (const name of cacheNames) {
    const cache = await caches.open(name);
    const keys = await cache.keys();
    status[name] = keys.length;
  }
  
  return status;
}

async function clearCache() {
  const cacheNames = await caches.keys();
  await Promise.all(
    cacheNames
      .filter((name) => name.startsWith('stockwise-'))
      .map((name) => caches.delete(name))
  );
}