# PWA Deployment Guide - EduSelf

## 🚀 Production'ga Chiqarish

### 1. Pre-Deployment Tayyorgarlik

#### A. Icon Fayllarni Tekshirish
```bash
# Icon fayllar mavjudligini tekshirish
ls -la static/icons/

# Kerakli fayllar:
# icon-16x16.png
# icon-32x32.png
# icon-72x72.png
# icon-96x96.png
# icon-128x128.png
# icon-144x144.png
# icon-152x152.png
# icon-192x192.png
# icon-192x192-maskable.png
# icon-384x384.png
# icon-512x512.png
# icon-512x512-maskable.png
```

#### B. Manifest.json Tekshirish
```bash
# Manifest faylni tekshirish
cat static/manifest.json

# Kerakli maydonlar:
# - name
# - short_name
# - start_url
# - display: "standalone"
# - theme_color
# - background_color
# - icons (kamida 192x192 va 512x512)
```

#### C. Service Worker Versiyasini Yangilash
```javascript
// static/js/service-worker.js
const CACHE_VERSION = 'eduself-v1.0.6'; // Versiyani oshiring
```

#### D. Static Fayllarni To'plash
```bash
python manage.py collectstatic --noinput
```

### 2. Git Commit va Push

```bash
# Barcha o'zgarishlarni qo'shish
git add .

# Commit yaratish
git commit -m "PWA texnologiyasi qo'shildi - v1.0.6

- Progressive Web App qo'llab-quvvatlash
- Offline ishlash imkoniyati
- Native app kabi tajriba
- Push notifications tayyorligi
- iOS va Android optimizatsiyasi
- Dark mode qo'llab-quvvatlash
- Zamonaviy UI/UX
"

# Production branch'ga push
git push origin main
```

### 3. Render.com Deployment

Render.com avtomatik deploy qiladi, lekin quyidagilarni tekshiring:

#### A. Environment Variables
Render.com dashboard'da:
```
HTTPS sozlangan bo'lishi kerak (avtomatik)
ALLOWED_HOSTS = eduself.uz, www.eduself.uz
```

#### B. Build Command
```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
```

#### C. Start Command
```bash
gunicorn eduself.wsgi:application
```

### 4. Post-Deployment Tekshirish

#### A. HTTPS Tekshirish
```bash
# SSL sertifikat tekshirish
curl -I https://eduself.uz

# Expected: HTTP/2 200
```

#### B. Manifest Tekshirish
```bash
# Manifest yuklanishini tekshirish
curl https://eduself.uz/static/manifest.json

# Yoki browser'da:
https://eduself.uz/static/manifest.json
```

#### C. Service Worker Tekshirish
```bash
# Service Worker faylini tekshirish
curl https://eduself.uz/static/js/service-worker.js

# Status: 200 OK bo'lishi kerak
```

#### D. Icons Tekshirish
```bash
# Icon fayllarni tekshirish
curl -I https://eduself.uz/static/icons/icon-192x192.png
curl -I https://eduself.uz/static/icons/icon-512x512.png

# Status: 200 OK bo'lishi kerak
```

### 5. Browser Test

#### A. Chrome DevTools
1. https://eduself.uz ga kiring
2. F12 → Application tab
3. Manifest bo'limini tekshiring
4. Service Workers bo'limini tekshiring
5. Lighthouse audit o'tkazing

#### B. Install Test
1. Address bar'da install icon paydo bo'lishi kerak
2. Install qiling
3. Standalone mode'da ochilishi kerak

### 6. Mobile Test

#### A. Android (Chrome)
1. https://eduself.uz ga kiring
2. "Add to Home screen" banner
3. Install qiling
4. Home screen'dan oching

#### B. iOS (Safari)
1. https://eduself.uz ga kiring
2. Share → "Add to Home Screen"
3. Install qiling
4. Home screen'dan oching

### 7. Performance Monitoring

#### A. Lighthouse CI
```bash
# Lighthouse CLI o'rnatish
npm install -g @lhci/cli

# Audit o'tkazish
lhci autorun --collect.url=https://eduself.uz
```

#### B. Web Vitals
Chrome DevTools → Lighthouse → Performance

**Target Metrics:**
- FCP (First Contentful Paint): < 1.8s
- LCP (Largest Contentful Paint): < 2.5s
- FID (First Input Delay): < 100ms
- CLS (Cumulative Layout Shift): < 0.1
- TTI (Time to Interactive): < 3.8s

### 8. Monitoring va Analytics

#### A. Service Worker Status
```javascript
// Console'da
navigator.serviceWorker.getRegistrations().then(regs => {
  console.log('Active Service Workers:', regs.length);
  regs.forEach(reg => {
    console.log('Scope:', reg.scope);
    console.log('State:', reg.active?.state);
  });
});
```

#### B. Cache Status
```javascript
// Console'da
caches.keys().then(keys => {
  console.log('Cache Names:', keys);
  keys.forEach(key => {
    caches.open(key).then(cache => {
      cache.keys().then(requests => {
        console.log(`${key}: ${requests.length} items`);
      });
    });
  });
});
```

#### C. Install Analytics
Google Analytics yoki boshqa analytics tool'da:
- Install events
- Standalone mode usage
- Offline usage
- Update acceptance rate

### 9. Troubleshooting

#### Issue: Service Worker not updating
**Solution:**
```javascript
// Force update
navigator.serviceWorker.getRegistrations().then(regs => {
  regs.forEach(reg => reg.update());
});
```

#### Issue: Manifest not loading
**Solution:**
1. Static files to'planganligini tekshiring
2. CORS headers to'g'ri sozlanganligini tekshiring
3. Content-Type: application/manifest+json

#### Issue: Icons not showing
**Solution:**
```bash
# Static files qayta to'plash
python manage.py collectstatic --clear --noinput
```

#### Issue: Install prompt not showing
**Reasons:**
- Avval o'rnatilgan bo'lishi mumkin
- HTTPS ishlatilmayotgan
- Manifest yoki icons yo'q
- Browser PWA criteria'ni qoniqtirmayapti

### 10. Rollback Plan

Agar muammo bo'lsa:

```bash
# Oldingi versiyaga qaytish
git revert HEAD
git push origin main

# Yoki specific commit'ga
git reset --hard <commit-hash>
git push -f origin main
```

### 11. Continuous Deployment

#### A. GitHub Actions (Ixtiyoriy)
`.github/workflows/deploy.yml`:
```yaml
name: Deploy PWA

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Collect static files
        run: |
          python manage.py collectstatic --noinput
      
      - name: Run Lighthouse CI
        run: |
          npm install -g @lhci/cli
          lhci autorun
```

### 12. Security Checklist

- [ ] HTTPS enabled
- [ ] CSP headers configured
- [ ] CORS properly set
- [ ] Service Worker scope limited
- [ ] Sensitive data not cached
- [ ] API keys not exposed in client code

### 13. SEO Optimization

#### A. Meta Tags
```html
<!-- Already in base.html -->
<meta name="description" content="...">
<meta name="keywords" content="...">
<link rel="canonical" href="https://eduself.uz">
```

#### B. Structured Data
```json
{
  "@context": "https://schema.org",
  "@type": "EducationalOrganization",
  "name": "EduSelf",
  "url": "https://eduself.uz",
  "logo": "https://eduself.uz/static/icons/icon-512x512.png"
}
```

#### C. Sitemap
```bash
# Django sitemap yaratish
python manage.py generate_sitemap
```

### 14. User Communication

#### A. Announcement
Foydalanuvchilarga xabar:
```
🎉 Yangilik! EduSelf endi mobil ilova sifatida o'rnatilishi mumkin!

📱 Android va iOS qurilmalaringizga o'rnating
⚡ Tezroq ishlaydi
🔔 Push bildirishnomalar
🌙 Dark mode
📡 Offline ishlash

O'rnatish uchun: eduself.uz ga kiring va "O'rnatish" tugmasini bosing!
```

#### B. Tutorial
Video yoki rasmli qo'llanma yaratish:
1. Saytga kirish
2. Install tugmasini topish
3. O'rnatish jarayoni
4. Ilovadan foydalanish

### 15. Monitoring Dashboard

#### A. Key Metrics
- Install rate
- Daily active users (DAU)
- Retention rate
- Offline usage
- Update acceptance rate
- Performance metrics

#### B. Tools
- Google Analytics
- Firebase Analytics
- Custom dashboard

### 16. Future Enhancements

#### A. Push Notifications Backend
```python
# Keyingi versiyada qo'shiladi
from pywebpush import webpush

def send_notification(user, title, body):
    subscription = user.push_subscription
    webpush(
        subscription_info=subscription,
        data=json.dumps({
            'title': title,
            'body': body,
            'icon': '/static/icons/icon-192x192.png'
        }),
        vapid_private_key=settings.VAPID_PRIVATE_KEY,
        vapid_claims={"sub": "mailto:admin@eduself.uz"}
    )
```

#### B. Background Sync
```javascript
// Offline'da yaratilgan ma'lumotlarni sync qilish
navigator.serviceWorker.ready.then(reg => {
  return reg.sync.register('sync-data');
});
```

#### C. Periodic Background Sync
```javascript
// Har 12 soatda kontent yangilash
navigator.serviceWorker.ready.then(reg => {
  return reg.periodicSync.register('update-content', {
    minInterval: 12 * 60 * 60 * 1000 // 12 hours
  });
});
```

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] Icons barcha o'lchamlarda yaratilgan
- [ ] Manifest.json to'ldirilgan
- [ ] Service Worker versiyasi yangilangan
- [ ] Static files to'plangan
- [ ] Local test o'tkazilgan
- [ ] Lighthouse audit 90+ ball

### Deployment
- [ ] Git commit va push
- [ ] Render.com deploy muvaffaqiyatli
- [ ] HTTPS ishlayapti
- [ ] Static files serve bo'lyapti

### Post-Deployment
- [ ] Manifest yuklanmoqda
- [ ] Service Worker ro'yxatdan o'tgan
- [ ] Icons ko'rinmoqda
- [ ] Install prompt ishlayapti
- [ ] Offline mode ishlayapti
- [ ] Mobile qurilmalarda test qilingan
- [ ] Performance metrics yaxshi

### Communication
- [ ] Foydalanuvchilarga e'lon
- [ ] Social media post
- [ ] Tutorial yaratilgan
- [ ] FAQ yangilangan

---

**Deployment Sanasi:** _____________  
**Versiya:** v1.0.6  
**Deploy qilgan:** _____________  
**Status:** ✅ Success / ❌ Failed  
**Izohlar:** _____________
