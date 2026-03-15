// Toast Notification System - Chiroyli va Zamonaviy

class ToastNotification {
    constructor() {
        this.container = null;
        this.init();
    }

    init() {
        // Toast container yaratish
        if (!document.querySelector('.toast-container')) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        } else {
            this.container = document.querySelector('.toast-container');
        }
    }

    show(message, type = 'info', duration = 5000) {
        const toast = this.createToast(message, type);
        this.container.appendChild(toast);

        // Animatsiya bilan ko'rsatish
        setTimeout(() => {
            toast.classList.add('show');
        }, 10);

        // Avtomatik yopish
        const autoCloseTimeout = setTimeout(() => {
            this.hide(toast);
        }, duration);

        // Close button bosilganda
        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.addEventListener('click', () => {
            clearTimeout(autoCloseTimeout);
            this.hide(toast);
        });

        // Toast bosilganda yopish
        toast.addEventListener('click', (e) => {
            if (!e.target.closest('.toast-close')) {
                clearTimeout(autoCloseTimeout);
                this.hide(toast);
            }
        });
    }

    createToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast-notification ${type}`;

        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };

        const titles = {
            success: 'Muvaffaqiyatli',
            error: 'Xatolik',
            warning: 'Ogohlantirish',
            info: 'Ma\'lumot'
        };

        toast.innerHTML = `
            <div class="toast-icon">${icons[type] || icons.info}</div>
            <div class="toast-content">
                <div class="toast-title">${titles[type] || titles.info}</div>
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close">
                <i class="bi bi-x"></i>
            </button>
            <div class="toast-progress"></div>
        `;

        return toast;
    }

    hide(toast) {
        toast.classList.remove('show');
        toast.classList.add('hide');

        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 400);
    }

    success(message, duration) {
        this.show(message, 'success', duration);
    }

    error(message, duration) {
        this.show(message, 'error', duration);
    }

    warning(message, duration) {
        this.show(message, 'warning', duration);
    }

    info(message, duration) {
        this.show(message, 'info', duration);
    }
}

// Global toast instance
window.toast = new ToastNotification();

// Django messages ni toast ga aylantirish
document.addEventListener('DOMContentLoaded', function() {
    const messagesContainer = document.querySelector('.messages-container');
    
    if (messagesContainer) {
        const alerts = messagesContainer.querySelectorAll('.alert');
        
        alerts.forEach((alert, index) => {
            // Xabar matnini olish
            let message = alert.textContent.trim();
            
            // Agar data-message attributi bo'lsa, uni ishlatish
            if (alert.hasAttribute('data-message')) {
                message = alert.getAttribute('data-message').trim();
            }
            
            // Bo'sh xabarlarni o'tkazib yuborish
            if (!message || message === '') {
                return;
            }
            
            let type = 'info';
            
            // Django message tags ni toast type ga aylantirish
            if (alert.classList.contains('alert-success') || alert.hasAttribute('data-tags') && alert.getAttribute('data-tags').includes('success')) {
                type = 'success';
            } else if (alert.classList.contains('alert-danger') || alert.classList.contains('alert-error') || 
                       (alert.hasAttribute('data-tags') && (alert.getAttribute('data-tags').includes('danger') || alert.getAttribute('data-tags').includes('error')))) {
                type = 'error';
            } else if (alert.classList.contains('alert-warning') || (alert.hasAttribute('data-tags') && alert.getAttribute('data-tags').includes('warning'))) {
                type = 'warning';
            } else if (alert.classList.contains('alert-info') || (alert.hasAttribute('data-tags') && alert.getAttribute('data-tags').includes('info'))) {
                type = 'info';
            }
            
            // Har bir toast uchun kechikish (agar bir nechta xabar bo'lsa)
            setTimeout(() => {
                window.toast.show(message, type, 4000);
            }, index * 200);
        });
        
        // Messages container ni butunlay o'chirish
        messagesContainer.remove();
    }
});

// AJAX so'rovlar uchun helper funksiyalar
window.showToast = function(message, type = 'info', duration = 5000) {
    window.toast.show(message, type, duration);
};

window.showSuccessToast = function(message, duration = 5000) {
    window.toast.success(message, duration);
};

window.showErrorToast = function(message, duration = 5000) {
    window.toast.error(message, duration);
};

window.showWarningToast = function(message, duration = 5000) {
    window.toast.warning(message, duration);
};

window.showInfoToast = function(message, duration = 5000) {
    window.toast.info(message, duration);
};
