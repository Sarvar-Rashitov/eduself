# PWA Service Worker Fix - EduSelf

## 🐛 Muammo

Service Worker `/static/js/` papkasida bo'lgani uchun faqat `/static/js/` scope'ida ishlayotgan edi. Butun sayt (`/`) uchun ishlashi kerak edi.

**Xato:**
```
SecurityError: The path of the provided scope ('/') is not under 
the max scope allowed ('/static/js/')
```

## ✅ Yechim

### 1. Service Worker'ni Ko'chirish
```bash
# /static/js/service-worker.js → /static/service-worker.js
```

Service Worker endi root static papkada.

### 2. Django View'lar Yaratish

**core/views.py:**
```python
def service_worker_view(request):
    """Service Worker'ni to'g'ri headers bilan serve qilish"""
    response = FileResponse(...)
    response['Service-Worker-Allowed'] = '/'
    response['Cache-Control'] = 'no-cache'
    return response

def manifest_view(request):
    """Manifest.json'ni to'g'ri Content-Type bilan serve qilish"""
    response = FileResponse(...)
    response['Content-Type'] = 'application/manifest+json'
    return response
```

### 3. URL Routing

**core/urls.py:**
```python
urlpatterns = [
    # ...
    path('service-worker.js', views.service_worker_view, name='service_worker'),
    path('manifest.json', views.manifest_view, name='manifest'),
]
```

### 4. Frontend Yo'llarni Yangilash

**static/js/pwa.js:**
```javascript
// Oldingi: '/static/js/service-worker.js'
// Yangi:
navigator.serviceWorker.register('/service-worker.js', {
  scope: '/'
});
```

**templates/base.html:**
```html
<!-- Oldingi: {% static 'manifest.json' %} -->
<!-- Yangi: -->
<link rel="manifest" href="/manifest.json">
```

### 5. Service Worker Cache Yo'llari

**static/service-worker.js:**
```javascript
const STATIC_ASSETS = [
  '/',
  '/static/css/style.css',
  '/static/css/base-layout.css',
  '/static/css/pwa-styles.css',
  '/static/js/pwa.js',
  '/manifest.json',  // Yangilandi
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
  // ...
];
```

## 📂 O'zgargan Fayllar

1. **static/service-worker.js** - Ko'chirildi (js/ dan chiqarildi)
2. **static/js/pwa.js** - Service Worker yo'li yangilandi
3. **templates/base.html** - Manifest yo'li yangilandi
4. **core/views.py** - Yangi view'lar qo'shildi
5. **core/urls.py** - Yangi URL'lar qo'shildi

## 🎯 Natija

✅ Service Worker endi butun sayt (`/`) uchun ishlaydi  
✅ Offline support barcha sahifalarda  
✅ Cache strategiyasi to'g'ri ishlaydi  
✅ Manifest to'g'ri Content-Type bilan serve bo'ladi  
✅ PWA install prompt ishlaydi  

## 🧪 Test Qilish

### 1. Service Worker Tekshirish
```javascript
// Browser Console'da
navigator.serviceWorker.getRegistrations().then(regs => {
  console.log('Registered:', regs.length);
  regs.forEach(reg => {
    console.log('Scope:', reg.scope);
    console.log('State:', reg.active?.state);
  });
});
```

**Kutilayotgan natija:**
```
Registered: 1
Scope: http://127.0.0.1:8000/
State: activated
```

### 2. Chrome DevTools
1. F12 → Application tab
2. Service Workers bo'limi
3. Status: "activated and is running"
4. Scope: "http://127.0.0.1:8000/"

### 3. Manifest Tekshirish
1. F12 → Application → Manifest
2. Barcha ma'lumotlar to'g'ri ko'rsatilishi kerak
3. Icons yuklanishi kerak

### 4. Offline Test
1. Network tab → Offline
2. Sahifani yangilash
3. Keshlangan sahifa ochilishi kerak

## 🚀 Deployment

### Local Test:
```bash
python manage.py runserver
# http://127.0.0.1:8000
```

### Production:
```bash
# Static fayllarni to'plash
python manage.py collectstatic --noinput

# Git commit
git add .
git commit -m "PWA Service Worker fix - root scope"
git push origin main
```

## 📝 Qo'shimcha Ma'lumotlar

### Service Worker Scope Qoidalari:
- Service Worker faqat o'zi joylashgan papka va uning ichidagi papkalarni boshqarishi mumkin
- `/static/js/service-worker.js` faqat `/static/js/` scope'ida ishlaydi
- `/service-worker.js` butun sayt (`/`) uchun ishlaydi
- `Service-Worker-Allowed` header bilan scope'ni kengaytirish mumkin

### Best Practices:
- ✅ Service Worker'ni root'da saqlash
- ✅ Django view orqali serve qilish (to'g'ri headers)
- ✅ Cache-Control: no-cache (yangilanishlar uchun)
- ✅ Service-Worker-Allowed: / (scope kengaytirish)

## 🔧 Troubleshooting

### Agar Service Worker hali ham ishlamasa:

1. **Browser cache'ni tozalash:**
```javascript
// Console'da
caches.keys().then(keys => {
  keys.forEach(key => caches.delete(key));
});
```

2. **Service Worker'ni unregister qilish:**
```javascript
// Console'da
navigator.serviceWorker.getRegistrations().then(regs => {
  regs.forEach(reg => reg.unregister());
});
```

3. **Hard refresh:**
- Chrome: Ctrl + Shift + R
- Firefox: Ctrl + F5

4. **DevTools'da "Update on reload" yoqish:**
- F12 → Application → Service Workers
- "Update on reload" checkbox'ni belgilash

## ✅ Checklist

- [x] Service Worker root'ga ko'chirildi
- [x] Django view'lar yaratildi
- [x] URL routing qo'shildi
- [x] pwa.js yangilandi
- [x] base.html yangilandi
- [x] service-worker.js cache yo'llari yangilandi
- [x] Local test o'tkazildi
- [x] Hujjatlar yangilandi

---

**Fix Sanasi:** 2025  
**Versiya:** 1.0.6  
**Status:** ✅ Fixed and Tested
