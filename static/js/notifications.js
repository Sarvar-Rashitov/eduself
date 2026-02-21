/**
 * Browser Native Notification System
 * Web Push Notifications for EduSelf Platform
 */

class NotificationManager {
    constructor() {
        this.permission = Notification.permission;
        this.isSupported = 'Notification' in window;
        this.init();
    }

    init() {
        console.log('🔔 NotificationManager init() boshlandi');
        
        if (!this.isSupported) {
            console.warn('❌ Browser notification qo\'llab-quvvatlanmaydi');
            return;
        }
        
        console.log('✅ Browser notification qo\'llab-quvvatlaydi');
        console.log('📊 Permission holati:', this.permission);

        // Sahifa yuklanganda permission tekshirish
        this.checkPermission();
        
        // Notification'larni polling qilish (har 30 soniyada)
        this.startPolling();
        
        console.log('✅ NotificationManager init() tugadi');
    }

    async checkPermission() {
        console.log('🔍 checkPermission() chaqirildi, holat:', this.permission);
        
        if (this.permission === 'default') {
            console.log('⚠️ Permission hali so\'ralmagan, prompt ko\'rsatiladi');
            // Hali so'ralmagan - foydalanuvchiga taklif qilish
            this.showPermissionPrompt();
        } else if (this.permission === 'granted') {
            console.log('✅ Notification permission berilgan');
        } else {
            console.log('❌ Notification permission rad etilgan');
        }
    }

    showPermissionPrompt() {
        // Chiroyli prompt ko'rsatish
        const promptHTML = `
            <div id="notification-prompt" style="
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                z-index: 10000;
                max-width: 350px;
                animation: slideIn 0.3s ease;
            ">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="font-size: 40px;">🔔</div>
                    <div style="flex: 1;">
                        <h4 style="margin: 0 0 5px 0; font-size: 16px;">Bildirishnomalarni yoqing</h4>
                        <p style="margin: 0; font-size: 13px; opacity: 0.9;">Yangi xabarlar haqida darhol xabardor bo'ling</p>
                    </div>
                </div>
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <button id="enable-notifications" style="
                        flex: 1;
                        padding: 10px;
                        background: white;
                        color: #667eea;
                        border: none;
                        border-radius: 8px;
                        font-weight: 600;
                        cursor: pointer;
                    ">Yoqish</button>
                    <button id="dismiss-notifications" style="
                        padding: 10px 15px;
                        background: rgba(255,255,255,0.2);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        cursor: pointer;
                    ">Keyinroq</button>
                </div>
            </div>
            <style>
                @keyframes slideIn {
                    from {
                        transform: translateX(400px);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
            </style>
        `;

        // Agar allaqachon ko'rsatilmagan bo'lsa
        if (!document.getElementById('notification-prompt')) {
            document.body.insertAdjacentHTML('beforeend', promptHTML);

            // Event listener'lar
            document.getElementById('enable-notifications').addEventListener('click', () => {
                this.requestPermission();
                document.getElementById('notification-prompt').remove();
            });

            document.getElementById('dismiss-notifications').addEventListener('click', () => {
                document.getElementById('notification-prompt').remove();
                // 1 kun ichida qayta so'ramaslik
                localStorage.setItem('notification-prompt-dismissed', Date.now());
            });
        }
    }

    async requestPermission() {
        try {
            const permission = await Notification.requestPermission();
            this.permission = permission;

            if (permission === 'granted') {
                console.log('✅ Notification permission berildi');
                this.showWelcomeNotification();
                
                // Server'ga permission berilganini xabar qilish
                this.updateServerPermission(true);
            } else {
                console.log('❌ Notification permission rad etildi');
                this.updateServerPermission(false);
            }
        } catch (error) {
            console.error('Permission so\'rashda xatolik:', error);
        }
    }

    showWelcomeNotification() {
        this.show({
            title: '🎉 Bildirishnomalar yoqildi!',
            body: 'Endi siz yangi xabarlar haqida darhol xabardor bo\'lasiz.',
            icon: '/static/icons/icon-192x192.png',
            badge: '/static/icons/icon-96x96.png'
        });
    }

    show(options) {
        console.log('📢 show() chaqirildi:', options.title);
        
        if (this.permission !== 'granted') {
            console.warn('⚠️ Notification permission yo\'q, ko\'rsatilmaydi');
            return;
        }

        const defaultOptions = {
            icon: '/static/icons/icon-192x192.png',
            badge: '/static/icons/icon-96x96.png',
            vibrate: [200, 100, 200],
            requireInteraction: false,
            silent: false
        };

        try {
            const notification = new Notification(options.title, {
                ...defaultOptions,
                ...options
            });

            console.log('✅ Notification yaratildi:', options.title);

            // Click event
            notification.onclick = (event) => {
                console.log('🖱️ Notification bosildi');
                event.preventDefault();
                window.focus();
                
                if (options.url) {
                    console.log('🔗 URL ga o\'tilmoqda:', options.url);
                    window.location.href = options.url;
                }
                
                notification.close();
            };

            // Auto close after 10 seconds
            setTimeout(() => {
                console.log('⏰ Notification avtomatik yopildi (10s)');
                notification.close();
            }, 10000);

            return notification;
        } catch (error) {
            console.error('❌ Notification yaratishda xatolik:', error);
        }
    }

    async fetchNotifications() {
        console.log('📡 fetchNotifications() chaqirildi');
        
        try {
            const response = await fetch('/api/notifications/unread/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            console.log('📡 API response status:', response.status);

            if (response.ok) {
                const data = await response.json();
                console.log('📡 API response data:', data);
                return data.notifications || [];
            } else {
                console.error('❌ API xatosi:', response.status, response.statusText);
            }
        } catch (error) {
            console.error('❌ Notification fetch xatolik:', error);
        }
        return [];
    }

    startPolling() {
        console.log('🔄 Polling boshlandi (har 30 soniyada)');
        
        // Har 30 soniyada yangi notification'larni tekshirish
        setInterval(async () => {
            console.log('🔄 Polling: yangi notification\'lar tekshirilmoqda...');
            
            if (this.permission === 'granted' && document.visibilityState === 'visible') {
                console.log('✅ Permission granted va sahifa visible');
                const notifications = await this.fetchNotifications();
                
                console.log('📥 Olingan notification\'lar:', notifications.length);
                
                notifications.forEach(notif => {
                    console.log('📢 Notification ko\'rsatilmoqda:', notif.title);
                    this.show({
                        title: notif.title,
                        body: notif.message,
                        url: notif.link,
                        tag: `notification-${notif.id}`,
                        data: notif
                    });
                });
            } else {
                console.log('⏸️ Polling o\'tkazib yuborildi:', {
                    permission: this.permission,
                    visibility: document.visibilityState
                });
            }
        }, 30000); // 30 soniya
        
        console.log('✅ Polling interval o\'rnatildi');
    }

    async updateServerPermission(granted) {
        try {
            await fetch('/api/notifications/permission/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                },
                body: JSON.stringify({ granted })
            });
        } catch (error) {
            console.error('Server permission update xatolik:', error);
        }
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

// Global instance
let notificationManager;

// DOM yuklanganda ishga tushirish
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 DOM yuklandi, NotificationManager yaratilmoqda...');
    
    notificationManager = new NotificationManager();
    
    console.log('✅ NotificationManager yaratildi:', notificationManager);
    
    // Global funksiya
    window.showNotification = (title, body, url) => {
        console.log('🌐 window.showNotification() chaqirildi');
        if (notificationManager) {
            notificationManager.show({ title, body, url });
        } else {
            console.error('❌ notificationManager mavjud emas');
        }
    };
    
    console.log('✅ window.showNotification() global funksiya o\'rnatildi');
});

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NotificationManager;
}
