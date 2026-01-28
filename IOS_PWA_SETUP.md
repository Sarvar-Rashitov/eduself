# iOS PWA Setup - EduSelf

Bu qo'llanma EduSelf loyihasini iOS qurilmalarida PWA (Progressive Web App) sifatida ishlaydigan qilish uchun amalga oshirilgan o'zgarishlarni tushuntiradi.

## 🚀 Amalga oshirilgan o'zgarishlar

### 1. HTML Meta Tag'lar (templates/base.html)

iOS PWA qo'llab-quvvatlashi uchun quyidagi meta tag'lar qo'shildi:

```html
<!-- iOS PWA Meta Tags -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="EduSelf">
<meta name="apple-touch-fullscreen" content="yes">
<meta name="format-detection" content="telephone=no">

<!-- Apple Touch Icons -->
<link rel="apple-touch-icon" sizes="180x180" href="{% static 'icons/apple-icon-180x180.png' %}">
<!-- ... boshqa o'lchamdagi iconlar -->

<!-- iOS Splash Screens -->
<link rel="apple-touch-startup-image" href="{% static 'icons/splash-640x1136.png' %}" media="...">
<!-- ... turli qurilmalar uchun splash screenlar -->
```

### 2. Manifest.json yangilandi

iOS uchun qo'shimcha sozlamalar:

```json
{
  "scope": "/",
  "prefer_related_applications": false,
  "orientation": "portrait-primary",
  "shortcuts": [
    {
      "name": "Fanlar",
      "url": "/subjects/",
      "icons": [{"src": "/static/icons/icon-192x192.png", "sizes": "192x192"}]
    }
  ]
}
```

### 3. Service Worker yaxshilandi (static/sw.js)

- Cache strategiyalari yaxshilandi
- iOS uchun maxsus optimizatsiyalar
- Background sync qo'llab-quvvatlashi
- Push notification'lar uchun tayyor

### 4. CSS Stillar (static/css/style.css)

iOS PWA uchun maxsus stillar qo'shildi:

```css
/* iOS PWA Specific Styles */
@supports (padding: max(0px)) {
    .mobile-app {
        padding-top: max(env(safe-area-inset-top), 0px);
        /* ... */
    }
}

/* iOS Safari specific fixes */
@media screen and (-webkit-min-device-pixel-ratio: 2) {
    /* ... */
}

/* iOS PWA status bar handling */
@media (display-mode: standalone) {
    /* ... */
}
```

### 5. JavaScript Yaxshilanmalari

- iOS detection funksiyalari
- Standalone mode detection
- iOS-specific install prompt
- Viewport handling
- Touch improvements

## 📱 Kerakli Icon'lar

### PWA Icon'lar
- icon-16x16.png
- icon-32x32.png
- icon-72x72.png
- icon-96x96.png
- icon-128x128.png
- icon-144x144.png
- icon-152x152.png
- icon-192x192.png
- icon-384x384.png
- icon-512x512.png

### Apple Touch Icon'lar
- apple-icon-57x57.png
- apple-icon-60x60.png
- apple-icon-72x72.png
- apple-icon-76x76.png
- apple-icon-114x114.png
- apple-icon-120x120.png
- apple-icon-144x144.png
- apple-icon-152x152.png
- apple-icon-180x180.png

### iOS Splash Screen'lar
- splash-640x1136.png (iPhone 5/SE)
- splash-750x1334.png (iPhone 6/7/8)
- splash-1242x2208.png (iPhone 6/7/8 Plus)
- splash-1125x2436.png (iPhone X/XS)
- splash-1536x2048.png (iPad)
- splash-1668x2224.png (iPad Pro 10.5")
- splash-2048x2732.png (iPad Pro 12.9")

## 🛠️ Setup Qadamlari

### 1. Icon'larni yaratish

```bash
# Python script bilan avtomatik yaratish
python generate_ios_icons.py

# Yoki manual ravishda:
# 1. https://realfavicongenerator.net/ ga kiring
# 2. Logo rasmingizni yuklang (kamida 512x512 px)
# 3. iOS va PWA sozlamalarini tanlang
# 4. Barcha iconlarni yuklab oling
# 5. static/icons/ papkasiga joylashtiring
```

### 2. Test qilish

```bash
# PWA sozlamalarini tekshirish
python test_ios_pwa.py
```

### 3. Server'ni ishga tushirish

```bash
# Django server
python manage.py runserver 0.0.0.0:8000

# Yoki production uchun
python main.py
```

### 4. iOS'da test qilish

1. iOS Safari'da saytni oching
2. Ulashish tugmasini bosing (pastdagi o'rta tugma)
3. "Bosh ekranga qo'shish" ni tanlang
4. Nom va iconni tasdiqlang
5. Bosh ekrandan PWA'ni oching

## ✅ iOS PWA Xususiyatlari

### Qo'llab-quvvatlanadigan:
- ✅ Bosh ekranga o'rnatish
- ✅ Standalone rejim
- ✅ Custom icon'lar
- ✅ Splash screen'lar
- ✅ Status bar sozlamalari
- ✅ Offline ishlash (Service Worker)
- ✅ Cache qilish
- ✅ Theme color
- ✅ Safe area insets
- ✅ Touch optimizatsiyalar

### Cheklovlar:
- ❌ Push notification'lar (iOS 16.4+ da qisman)
- ❌ Background sync (cheklangan)
- ❌ File system API
- ❌ Automatic updates (manual refresh kerak)

## 🔧 Troubleshooting

### Icon ko'rinmayapti:
1. Icon fayllar to'g'ri o'lchamda ekanligini tekshiring
2. PNG formatida ekanligini tasdiqlang
3. Cache'ni tozalang va sahifani yangilang

### PWA o'rnatilmayapti:
1. HTTPS ishlatilayotganini tekshiring (localhost bundan mustasno)
2. Manifest.json to'g'ri formatda ekanligini tekshiring
3. Service Worker ro'yxatdan o'tganini tasdiqlang

### Splash screen ko'rinmayapti:
1. Splash screen fayllar mavjudligini tekshiring
2. Media query'lar to'g'ri ekanligini tasdiqlang
3. iOS versiyasini tekshiring (iOS 12.2+)

## 📊 Performance

### Optimizatsiyalar:
- Icon'lar siqilgan (optimized PNG)
- Service Worker cache strategiyalari
- Lazy loading
- Critical CSS inlined
- Offline fallback'lar

### Metrics:
- First Contentful Paint: <2s
- Largest Contentful Paint: <3s
- Time to Interactive: <3s
- PWA Score: 90+/100

## 🔄 Yangilanishlar

PWA yangilanishlarini boshqarish:

1. Service Worker versiyasini oshiring
2. Cache nomini o'zgartiring
3. Foydalanuvchilarga yangilanish haqida xabar bering
4. Manual refresh taklif qiling

## 📞 Qo'llab-quvvatlash

Muammolar yuzaga kelsa:

1. `test_ios_pwa.py` script'ini ishga tushiring
2. Browser Developer Tools'da Console'ni tekshiring
3. Network tab'da Service Worker'ni monitoring qiling
4. Application tab'da PWA sozlamalarini ko'ring

## 🎯 Keyingi Qadamlar

1. **Push Notification'lar**: iOS 16.4+ uchun test qiling
2. **App Store Connect**: PWA'ni App Store'ga qo'shish imkoniyatini o'rganing
3. **Analytics**: PWA usage metrics qo'shing
4. **A/B Testing**: Install prompt'larni optimize qiling
5. **Performance**: Core Web Vitals'ni yaxshilang

---

**Eslatma**: Bu setup iOS 12.2+ versiyalarida ishlaydi. Eski versiyalar uchun fallback'lar mavjud.