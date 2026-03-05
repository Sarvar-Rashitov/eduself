# PWA Setup Guide - EduSelf

## ✅ Nima qilindi?

EduSelf platformasiga zamonaviy Progressive Web App (PWA) texnologiyasi qo'shildi. Endi foydalanuvchilar ilovani Android va iOS qurilmalariga o'rnatib, native ilova kabi ishlatishlari mumkin.

## 📱 PWA Xususiyatlari

### 1. **Offline Ishlash**
- Service Worker orqali kesh boshqaruvi
- Internetga ulanish bo'lmaganda ham asosiy funksiyalar ishlaydi
- Rasmlar va static fayllar avtomatik keshlanadi

### 2. **Native Ilova Tajribasi**
- Standalone mode - brauzer UI'siz ochiladi
- iOS va Android uchun maxsus optimizatsiya
- Safe area insets (notch) qo'llab-quvvatlash
- Status bar rangi dinamik o'zgaradi

### 3. **Push Bildirishnomalar**
- Native push notifications qo'llab-quvvatlash
- Background sync
- Badge API (yangiliklar soni)

### 4. **Install Prompts**
- Avtomatik o'rnatish taklifi
- Floating install button
- Banner notification

### 5. **Zamonaviy UI/UX**
- Skeleton loaders (preloaders)
- Pull-to-refresh
- Smooth animations
- Dark mode qo'llab-quvvatlash

## 📂 Yaratilgan Fayllar

```
static/
├── manifest.json              # PWA konfiguratsiyasi
├── browserconfig.xml          # Windows tiles
├── css/
│   └── pwa-styles.css        # PWA UI stillari
└── js/
    ├── pwa.js                # PWA manager
    └── service-worker.js     # Service worker

templates/
└── base.html                 # PWA integratsiyasi qo'shildi
```

## 🎨 Icon Dizayni

### Zamonaviy Dizayn Xususiyatlari:
- **Gradient Background**: Indigo (#667eea) dan Purple (#764ba2) gacha
- **Kitob Belgisi**: Ta'lim platformasini ifodalaydi
- **Graduation Cap**: Oltin rangda magistrlik qalpoqchasi
- **"Edu" Matni**: Branding elementi
- **Shaffoflik**: RGBA format, to'liq shaffof background

### Icon O'lchamlari:
- 16x16px - Browser favicon
- 32x32px - Browser favicon
- 72x72px - iOS va Android
- 96x96px - Android
- 128x128px - Chrome Web Store
- 144x144px - Windows tiles
- 152x152px - iOS
- 192x192px - Android (standard va maskable)
- 384x384px - Android
- 512x512px - Splash screen va maskable

### Maskable Icons:
Android adaptive icons uchun 192x192 va 512x512 o'lchamlarida maskable versiyalar yaratilgan. Bu iconlar har qanday shakl (doira, kvadrat, squircle) ichida yaxshi ko'rinadi.

## 🚀 Deployment

### 1. Static Fayllarni To'plash
```bash
python manage.py collectstatic --noinput
```

### 2. Service Worker URL'ni Sozlash
Service Worker faqat HTTPS yoki localhost'da ishlaydi. Production'da HTTPS majburiy!

### 3. HTTPS Sozlash
Render.com avtomatik HTTPS beradi, qo'shimcha sozlash kerak emas.

### 4. Git Push
```bash
git add .
git commit -m "PWA texnologiyasi qo'shildi"
git push origin main
```

## 📱 Foydalanuvchi Uchun O'rnatish

### Android (Chrome):
1. Saytga kiring: https://eduself.uz
2. "O'rnatish" tugmasi paydo bo'ladi
3. Yoki Chrome menu → "Add to Home screen"
4. Ilova home screen'ga qo'shiladi

### iOS (Safari):
1. Saytga kiring: https://eduself.uz
2. Share tugmasini bosing (pastdagi o'rta tugma)
3. "Add to Home Screen" tanlang
4. "Add" tugmasini bosing

### Desktop (Chrome/Edge):
1. Saytga kiring
2. Address bar'da install icon paydo bo'ladi
3. Yoki Settings → "Install EduSelf"

## 🔧 Sozlamalar

### manifest.json
- `name`: To'liq nom
- `short_name`: Qisqa nom (home screen uchun)
- `theme_color`: Branding rangi
- `background_color`: Splash screen rangi
- `start_url`: Boshlang'ich sahifa

### Service Worker Cache
`static/js/service-worker.js` faylida:
- `CACHE_VERSION`: Har yangilanishda o'zgartiring
- `STATIC_ASSETS`: Keshlanadigan fayllar ro'yxati

## 🎯 Keyingi Qadamlar

### 1. Push Notifications Backend
```python
# core/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def push_subscribe(request):
    if request.method == 'POST':
        subscription = json.loads(request.body)
        # Subscription'ni database'ga saqlash
        # PushSubscription model yaratish kerak
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid method'}, status=400)
```

### 2. VAPID Keys Generatsiya
```bash
pip install py-vapid
vapid --gen
```

### 3. Push Notification Yuborish
```python
from pywebpush import webpush, WebPushException

def send_push_notification(subscription_info, message):
    try:
        webpush(
            subscription_info=subscription_info,
            data=message,
            vapid_private_key="YOUR_PRIVATE_KEY",
            vapid_claims={
                "sub": "mailto:admin@eduself.uz"
            }
        )
    except WebPushException as ex:
        print(f"Push failed: {ex}")
```

### 4. Background Sync
Offline'da yaratilgan ma'lumotlarni online bo'lganda yuklash.

### 5. Periodic Background Sync
Har 12 soatda kontentni yangilash (Chrome 80+).

## 🧪 Test Qilish

### 1. Lighthouse Audit
Chrome DevTools → Lighthouse → PWA kategoriyasini test qiling.

### 2. PWA Checklist
- ✅ HTTPS
- ✅ Service Worker
- ✅ Manifest.json
- ✅ Icons (192px, 512px)
- ✅ Offline fallback
- ✅ Viewport meta tag
- ✅ Theme color

### 3. Qurilmalarda Test
- Android Chrome
- iOS Safari
- Desktop Chrome/Edge

## 📊 Monitoring

### Service Worker Status
```javascript
// Console'da
navigator.serviceWorker.getRegistrations().then(registrations => {
  console.log('Active SWs:', registrations.length);
});
```

### Cache Status
```javascript
// Console'da
caches.keys().then(keys => {
  console.log('Cached:', keys);
});
```

## 🐛 Troubleshooting

### Service Worker Yangilanmayapti
1. Chrome DevTools → Application → Service Workers
2. "Update on reload" ni yoqing
3. "Unregister" → Sahifani yangilang

### Icons Ko'rinmayapti
1. Icon fayllar to'g'ri joyda ekanligini tekshiring
2. `collectstatic` qayta ishga tushiring
3. Browser cache'ni tozalang

### Offline Ishlamayapti
1. Service Worker ro'yxatdan o'tganligini tekshiring
2. HTTPS ishlatilayotganligini tasdiqlang
3. Console'da xatolarni ko'ring

## 📚 Qo'shimcha Resurslar

- [PWA Documentation](https://web.dev/progressive-web-apps/)
- [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Web App Manifest](https://developer.mozilla.org/en-US/docs/Web/Manifest)
- [Push API](https://developer.mozilla.org/en-US/docs/Web/API/Push_API)

## ✨ Xususiyatlar

### Hozirda Mavjud:
- ✅ Offline support
- ✅ Install prompts
- ✅ Native app experience
- ✅ Caching strategy
- ✅ Update notifications
- ✅ iOS/Android optimization
- ✅ Dark mode support
- ✅ Skeleton loaders

### Kelajakda Qo'shiladi:
- ⏳ Push notifications backend
- ⏳ Background sync
- ⏳ Periodic sync
- ⏳ Share target API
- ⏳ File handling
- ⏳ Shortcuts API

---

**Muallif:** Kiro AI Assistant  
**Sana:** 2025  
**Versiya:** 1.0.0
