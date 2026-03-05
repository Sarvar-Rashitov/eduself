// PWA Installation va Yangilanishlar
class PWAManager {
  constructor() {
    this.deferredPrompt = null;
    this.swRegistration = null;
    this.init();
  }

  async init() {
    // Service Worker ro'yxatdan o'tkazish
    if ('serviceWorker' in navigator) {
      try {
        this.swRegistration = await navigator.serviceWorker.register('/service-worker.js', {
          scope: '/'
        });
        console.log('[PWA] Service Worker registered:', this.swRegistration);
        
        // Yangilanishlarni tekshirish
        this.checkForUpdates();
        
        // Har 60 daqiqada yangilanishni tekshirish
        setInterval(() => this.checkForUpdates(), 60 * 60 * 1000);
      } catch (error) {
        console.error('[PWA] Service Worker registration failed:', error);
      }
    }

    // iOS uchun maxsus install prompt
    if (this.isIOS() && !this.isInStandaloneMode()) {
      // 3 soniya kutib, iOS install prompt'ni ko'rsatish
      setTimeout(() => {
        if (!localStorage.getItem('pwa-install-dismissed')) {
          this.showInstallButton();
        }
      }, 3000);
    }

    // Install prompt'ni ushlab qolish (Android/Desktop)
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      this.deferredPrompt = e;
      this.showInstallButton();
    });

    // O'rnatilganini tekshirish
    window.addEventListener('appinstalled', () => {
      console.log('[PWA] App installed');
      this.hideInstallButton();
      this.showToast('✅ EduSelf muvaffaqiyatli o\'rnatildi!', 'success');
    });

    // Push bildirishnomalar
    this.setupPushNotifications();
  }

  async checkForUpdates() {
    if (!this.swRegistration) return;
    
    try {
      await this.swRegistration.update();
      
      if (this.swRegistration.waiting) {
        this.showUpdateNotification();
      }
      
      this.swRegistration.addEventListener('updatefound', () => {
        const newWorker = this.swRegistration.installing;
        
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            this.showUpdateNotification();
          }
        });
      });
    } catch (error) {
      console.error('[PWA] Update check failed:', error);
    }
  }

  showUpdateNotification() {
    const updateBanner = document.createElement('div');
    updateBanner.className = 'pwa-update-banner';
    updateBanner.innerHTML = `
      <div class="pwa-update-content">
        <div class="pwa-update-icon">🔄</div>
        <div class="pwa-update-text">
          <strong>Yangilanish mavjud!</strong>
          <p>EduSelf'ning yangi versiyasi tayyor</p>
        </div>
        <button class="pwa-update-btn" onclick="pwaManager.applyUpdate()">
          Yangilash
        </button>
        <button class="pwa-update-close" onclick="this.parentElement.parentElement.remove()">
          ✕
        </button>
      </div>
    `;
    document.body.appendChild(updateBanner);
    
    // 3 soniyadan keyin animatsiya bilan ko'rsatish
    setTimeout(() => updateBanner.classList.add('show'), 100);
  }

  applyUpdate() {
    if (this.swRegistration && this.swRegistration.waiting) {
      this.swRegistration.waiting.postMessage({ action: 'skipWaiting' });
      
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        window.location.reload();
      });
    }
  }

  showInstallButton() {
    // Install button'ni ko'rsatish
    const installBtn = document.getElementById('pwaInstallBtn');
    if (installBtn) {
      installBtn.style.display = 'flex';
      installBtn.addEventListener('click', () => this.promptInstall());
    }
    
    // iOS uchun darhol banner ko'rsatish
    if (this.isIOS() && !this.isInStandaloneMode()) {
      // 2 soniya kutib, keyin ko'rsatish
      setTimeout(() => {
        if (!localStorage.getItem('pwa-install-dismissed')) {
          this.showInstallBanner();
        }
      }, 2000);
    } else {
      // Boshqa platformalar uchun banner
      this.showInstallBanner();
    }
  }

  hideInstallButton() {
    const installBtn = document.getElementById('pwaInstallBtn');
    if (installBtn) {
      installBtn.style.display = 'none';
    }
    
    const banner = document.querySelector('.pwa-install-banner');
    if (banner) {
      banner.remove();
    }
  }

  showInstallBanner() {
    // Agar avval yopilgan bo'lsa, ko'rsatmaslik
    if (localStorage.getItem('pwa-install-dismissed')) {
      return;
    }
    
    // iOS uchun maxsus banner
    if (this.isIOS() && !this.isInStandaloneMode()) {
      this.showIOSInstallPrompt();
      return;
    }
    
    const banner = document.createElement('div');
    banner.className = 'pwa-install-banner';
    banner.innerHTML = `
      <div class="pwa-install-content">
        <div class="pwa-install-icon">
          <img src="/static/icons/icon-72x72.png" alt="EduSelf">
        </div>
        <div class="pwa-install-text">
          <strong>EduSelf ilovasini o'rnating</strong>
          <p>Tezroq kirish va offline ishlash</p>
        </div>
        <button class="pwa-install-btn" onclick="pwaManager.promptInstall()">
          O'rnatish
        </button>
        <button class="pwa-install-close" onclick="pwaManager.dismissInstallBanner()">
          ✕
        </button>
      </div>
    `;
    document.body.appendChild(banner);
    
    setTimeout(() => banner.classList.add('show'), 500);
  }

  isIOS() {
    return /iPhone|iPad|iPod/.test(navigator.userAgent) && !window.MSStream;
  }

  isInStandaloneMode() {
    return window.matchMedia('(display-mode: standalone)').matches || 
           window.navigator.standalone === true;
  }

  showIOSInstallPrompt() {
    const prompt = document.createElement('div');
    prompt.className = 'ios-install-prompt';
    prompt.innerHTML = `
      <div class="ios-install-content">
        <button class="ios-install-close" onclick="pwaManager.dismissIOSPrompt()">✕</button>
        <div class="ios-install-icon">
          <img src="/static/icons/icon-192x192.png" alt="EduSelf">
        </div>
        <h3>EduSelf ilovasini o'rnating</h3>
        <p>Bu ilovani bosh ekranga qo'shish uchun:</p>
        <ol class="ios-install-steps">
          <li>
            <span class="step-icon">📤</span>
            <span>Safari'ning pastki qismidagi <strong>Ulashish</strong> tugmasini bosing</span>
          </li>
          <li>
            <span class="step-icon">➕</span>
            <span><strong>"Bosh ekranga qo'shish"</strong> ni tanlang</span>
          </li>
          <li>
            <span class="step-icon">✅</span>
            <span>Yuqori o'ng burchakdagi <strong>"Qo'shish"</strong> ni bosing</span>
          </li>
        </ol>
        <div class="ios-install-arrow">
          <svg width="30" height="40" viewBox="0 0 30 40" fill="currentColor">
            <path d="M15 0 L15 30 M15 30 L5 20 M15 30 L25 20" stroke="currentColor" stroke-width="3" fill="none"/>
          </svg>
        </div>
      </div>
    `;
    document.body.appendChild(prompt);
    
    setTimeout(() => prompt.classList.add('show'), 100);
  }

  dismissIOSPrompt() {
    const prompt = document.querySelector('.ios-install-prompt');
    if (prompt) {
      prompt.classList.remove('show');
      setTimeout(() => prompt.remove(), 300);
    }
    localStorage.setItem('pwa-install-dismissed', 'true');
  }

  dismissInstallBanner() {
    const banner = document.querySelector('.pwa-install-banner');
    if (banner) {
      banner.classList.remove('show');
      setTimeout(() => banner.remove(), 300);
    }
    localStorage.setItem('pwa-install-dismissed', 'true');
  }

  async promptInstall() {
    if (!this.deferredPrompt) {
      this.showToast('⚠️ O\'rnatish hozircha mavjud emas', 'warning');
      return;
    }

    this.deferredPrompt.prompt();
    const { outcome } = await this.deferredPrompt.userChoice;
    
    console.log('[PWA] Install prompt outcome:', outcome);
    
    if (outcome === 'accepted') {
      this.showToast('✅ O\'rnatish boshlandi...', 'success');
    }
    
    this.deferredPrompt = null;
    this.hideInstallButton();
  }

  async setupPushNotifications() {
    if (!('Notification' in window) || !('PushManager' in window)) {
      console.log('[PWA] Push notifications not supported');
      return;
    }

    // Agar allaqachon ruxsat berilgan bo'lsa, subscribe qilish
    if (Notification.permission === 'granted') {
      await this.subscribeToPush();
    }
    
    // Notification permission button'ni qo'shish
    this.addNotificationPermissionButton();
  }

  addNotificationPermissionButton() {
    // Agar ruxsat berilmagan bo'lsa, button ko'rsatish
    if (Notification.permission === 'default') {
      const notifBtn = document.createElement('button');
      notifBtn.className = 'notification-permission-btn';
      notifBtn.innerHTML = `
        <i class="bi bi-bell"></i>
        <span>Bildirishnomalarni yoqish</span>
      `;
      notifBtn.onclick = () => this.requestNotificationPermission();
      
      // Header'ga qo'shish
      const headerActions = document.querySelector('.page-header-actions');
      if (headerActions && Notification.permission !== 'granted') {
        headerActions.insertBefore(notifBtn, headerActions.firstChild);
      }
    }
  }

  async requestNotificationPermission() {
    if (!('Notification' in window)) {
      this.showToast('⚠️ Bildirishnomalar qo\'llab-quvvatlanmaydi', 'warning');
      return false;
    }

    try {
      const permission = await Notification.requestPermission();
      
      if (permission === 'granted') {
        console.log('[PWA] Notification permission granted');
        this.showToast('✅ Bildirishnomalar yoqildi!', 'success');
        await this.subscribeToPush();
        
        // Test notification
        this.showTestNotification();
        
        // Button'ni olib tashlash
        const btn = document.querySelector('.notification-permission-btn');
        if (btn) btn.remove();
        
        return true;
      } else {
        console.log('[PWA] Notification permission denied');
        this.showToast('❌ Bildirishnomalar rad etildi', 'warning');
        return false;
      }
    } catch (error) {
      console.error('[PWA] Notification permission error:', error);
      return false;
    }
  }

  showTestNotification() {
    if (Notification.permission === 'granted') {
      new Notification('EduSelf', {
        body: 'Bildirishnomalar muvaffaqiyatli yoqildi! 🎉',
        icon: '/static/icons/icon-192x192.png',
        badge: '/static/icons/icon-72x72.png',
        vibrate: [200, 100, 200],
        tag: 'test-notification',
        requireInteraction: false
      });
    }
  }

  async subscribeToPush() {
    if (!this.swRegistration) return;

    try {
      const subscription = await this.swRegistration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: this.urlBase64ToUint8Array(
          // VAPID public key (serverdan olish kerak)
          'YOUR_VAPID_PUBLIC_KEY'
        )
      });

      // Subscription'ni serverga yuborish
      await this.sendSubscriptionToServer(subscription);
      
      console.log('[PWA] Push subscription successful');
    } catch (error) {
      console.error('[PWA] Push subscription failed:', error);
    }
  }

  async sendSubscriptionToServer(subscription) {
    // Subscription'ni serverga yuborish
    try {
      const response = await fetch('/api/push-subscribe/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': window.csrfToken
        },
        body: JSON.stringify(subscription)
      });
      
      if (response.ok) {
        console.log('[PWA] Subscription sent to server');
      }
    } catch (error) {
      console.error('[PWA] Failed to send subscription:', error);
    }
  }

  urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
      .replace(/\-/g, '+')
      .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }

  showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `pwa-toast pwa-toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 100);
    
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }

  // Offline/Online holatini kuzatish
  setupConnectionMonitoring() {
    window.addEventListener('online', () => {
      this.showToast('✅ Internet aloqasi tiklandi', 'success');
      this.syncOfflineData();
    });

    window.addEventListener('offline', () => {
      this.showToast('⚠️ Internet aloqasi yo\'q', 'warning');
    });
  }

  async syncOfflineData() {
    if ('sync' in this.swRegistration) {
      try {
        await this.swRegistration.sync.register('sync-data');
        console.log('[PWA] Background sync registered');
      } catch (error) {
        console.error('[PWA] Background sync failed:', error);
      }
    }
  }

  // App badge (Chrome 81+)
  setBadge(count) {
    if ('setAppBadge' in navigator) {
      navigator.setAppBadge(count).catch(err => {
        console.error('[PWA] Badge set failed:', err);
      });
    }
  }

  clearBadge() {
    if ('clearAppBadge' in navigator) {
      navigator.clearAppBadge().catch(err => {
        console.error('[PWA] Badge clear failed:', err);
      });
    }
  }
}

// PWA Manager'ni ishga tushirish
const pwaManager = new PWAManager();

// Connection monitoring
pwaManager.setupConnectionMonitoring();

// Standalone mode'ni aniqlash
if (window.matchMedia('(display-mode: standalone)').matches || 
    window.navigator.standalone === true) {
  console.log('[PWA] Running in standalone mode');
  document.body.classList.add('pwa-standalone');
}

// iOS Safari uchun
if (/iPhone|iPad|iPod/.test(navigator.userAgent) && !window.MSStream) {
  document.body.classList.add('pwa-ios');
}

// Android uchun
if (/Android/.test(navigator.userAgent)) {
  document.body.classList.add('pwa-android');
}
