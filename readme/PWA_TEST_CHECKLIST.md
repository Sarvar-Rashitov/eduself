# PWA Test Checklist - EduSelf

## 🧪 Test Qilish Bosqichlari

### 1. Local Test (Development)

#### A. Service Worker Test
```bash
# Development server'ni ishga tushiring
python manage.py runserver

# Browser'da ochish
http://127.0.0.1:8000
```

**Chrome DevTools:**
1. F12 → Application tab
2. Service Workers bo'limini tekshiring
3. "Update on reload" ni yoqing
4. Sahifani yangilang
5. Service Worker "activated" holatida bo'lishi kerak

#### B. Manifest Test
**Chrome DevTools:**
1. F12 → Application → Manifest
2. Barcha ma'lumotlar to'g'ri ko'rsatilishi kerak:
   - Name: EduSelf - Ta'lim Platformasi
   - Short name: EduSelf
   - Theme color: #4F46E5
   - Icons: 11 ta icon

#### C. Lighthouse Audit
1. F12 → Lighthouse tab
2. "Progressive Web App" kategoriyasini tanlang
3. "Generate report" bosing
4. 90+ ball olish kerak

**Tekshiriladigan narsalar:**
- ✅ Installable
- ✅ PWA optimized
- ✅ Works offline
- ✅ Configured for custom splash screen
- ✅ Sets a theme color
- ✅ Content sized correctly for viewport
- ✅ Has a `<meta name="viewport">` tag
- ✅ Provides a valid apple-touch-icon

### 2. Offline Test

#### A. Cache Test
1. Saytga kiring va bir necha sahifani oching
2. Chrome DevTools → Application → Cache Storage
3. "eduself-v1.0.5-static" va boshqa cache'lar ko'rinishi kerak

#### B. Offline Mode Test
1. Chrome DevTools → Network tab
2. "Offline" ni tanlang
3. Sahifani yangilang
4. Offline sahifa yoki kesh'langan kontent ko'rinishi kerak

#### C. Network Throttling
1. Network tab → "Slow 3G" ni tanlang
2. Sahifa tez yuklanishi kerak (cache'dan)

### 3. Install Test

#### A. Desktop Install (Chrome)
1. Address bar'da install icon paydo bo'lishi kerak
2. Icon'ga bosing
3. "Install" tugmasini bosing
4. Ilova yangi oynada ochilishi kerak

**Yoki:**
1. Chrome menu (⋮) → "Install EduSelf"
2. Confirm qiling

#### B. Mobile Install (Android Chrome)
1. Saytga kiring
2. "Add to Home screen" banner paydo bo'lishi kerak
3. Yoki Chrome menu → "Add to Home screen"
4. Home screen'da icon paydo bo'lishi kerak
5. Icon'ga bosib ochganda standalone mode'da ochilishi kerak

#### C. iOS Install (Safari)
1. Safari'da saytga kiring
2. Share button (pastdagi o'rta tugma)
3. "Add to Home Screen"
4. "Add" tugmasini bosing
5. Home screen'da icon paydo bo'lishi kerak

### 4. Standalone Mode Test

**Desktop:**
1. O'rnatilgan ilovani oching
2. Browser UI (address bar, tabs) ko'rinmasligi kerak
3. Faqat ilova kontenti ko'rinishi kerak

**Mobile:**
1. Home screen'dan ilovani oching
2. Status bar rangi theme color bilan mos kelishi kerak
3. Browser UI ko'rinmasligi kerak
4. Native ilova kabi ko'rinishi kerak

### 5. Update Test

#### A. Service Worker Update
1. `service-worker.js` faylida `CACHE_VERSION` ni o'zgartiring
2. Faylni saqlang va server'ni restart qiling
3. Saytga kiring
4. Update banner paydo bo'lishi kerak
5. "Yangilash" tugmasini bosing
6. Sahifa yangilanishi kerak

#### B. Force Update
```javascript
// Console'da
navigator.serviceWorker.getRegistrations().then(registrations => {
  registrations.forEach(reg => reg.unregister());
});
location.reload();
```

### 6. Push Notification Test (Keyinchalik)

**Hozircha backend yo'q, lekin test qilish:**
1. Chrome DevTools → Application → Notifications
2. "Push" tugmasini bosing
3. Test notification ko'rinishi kerak

### 7. Performance Test

#### A. Load Time
1. Chrome DevTools → Network tab
2. "Disable cache" ni o'chiring
3. Sahifani yangilang
4. Load time 2 soniyadan kam bo'lishi kerak

#### B. First Contentful Paint (FCP)
- Target: < 1.8s
- Good: < 1.0s

#### C. Largest Contentful Paint (LCP)
- Target: < 2.5s
- Good: < 1.2s

#### D. Time to Interactive (TTI)
- Target: < 3.8s
- Good: < 2.5s

### 8. Responsive Test

**Test qilinadigan qurilmalar:**
- iPhone SE (375x667)
- iPhone 12 Pro (390x844)
- iPad (768x1024)
- Android Phone (360x640)
- Desktop (1920x1080)

**Chrome DevTools:**
1. F12 → Toggle device toolbar (Ctrl+Shift+M)
2. Har bir qurilmani tanlang
3. Barcha elementlar to'g'ri ko'rinishi kerak

### 9. Dark Mode Test

1. Sidebar'dan "Qora rejim" ni yoqing
2. Barcha elementlar dark mode'da to'g'ri ko'rinishi kerak
3. PWA elementlari (banner, toast) ham dark bo'lishi kerak

### 10. Cross-Browser Test

#### Chrome/Edge (Chromium)
- ✅ Full PWA support
- ✅ Install prompt
- ✅ Service Worker
- ✅ Push notifications

#### Firefox
- ⚠️ Limited PWA support
- ✅ Service Worker
- ❌ Install prompt yo'q

#### Safari (iOS)
- ⚠️ Partial PWA support
- ✅ Add to Home Screen
- ✅ Service Worker (iOS 11.3+)
- ❌ Push notifications yo'q (hozircha)

## 📊 Expected Results

### Lighthouse Scores (Target)
- Performance: 90+
- Accessibility: 90+
- Best Practices: 90+
- SEO: 90+
- PWA: 90+

### PWA Checklist
- ✅ Registers a service worker
- ✅ Responds with 200 when offline
- ✅ Contains a web app manifest
- ✅ Configured for a custom splash screen
- ✅ Sets a theme color
- ✅ Content sized correctly
- ✅ Has a viewport meta tag
- ✅ Provides valid icons
- ✅ Provides apple-touch-icon

## 🐛 Common Issues

### Issue 1: Service Worker not registering
**Solution:**
- HTTPS ishlatilayotganligini tekshiring (yoki localhost)
- Console'da xatolarni ko'ring
- Browser cache'ni tozalang

### Issue 2: Icons not showing
**Solution:**
```bash
python manage.py collectstatic --noinput
```

### Issue 3: Install prompt not showing
**Solution:**
- Manifest.json to'g'ri yuklanganligini tekshiring
- Icons mavjudligini tasdiqlang
- HTTPS ishlatilayotganligini tekshiring
- Avval o'rnatilmagan bo'lishi kerak

### Issue 4: Offline not working
**Solution:**
- Service Worker activated ekanligini tekshiring
- Cache'da fayllar borligini ko'ring
- Network tab'da "Offline" rejimini test qiling

### Issue 5: Update not showing
**Solution:**
- CACHE_VERSION o'zgartirilganligini tekshiring
- Service Worker yangilanganligini tasdiqlang
- "Update on reload" yoqilganligini ko'ring

## 🚀 Production Test

### Pre-deployment Checklist
- [ ] Icons barcha o'lchamlarda mavjud
- [ ] manifest.json to'g'ri sozlangan
- [ ] Service Worker cache version yangilangan
- [ ] HTTPS sozlangan
- [ ] Static files to'plangan
- [ ] Lighthouse audit o'tkazilgan

### Post-deployment Test
1. Production URL'ga kiring
2. Barcha yuqoridagi testlarni qaytadan o'tkazing
3. Real qurilmalarda test qiling
4. Har xil tarmoq sharoitlarida test qiling

## 📱 Real Device Testing

### Android
1. Chrome browser'da saytga kiring
2. Install prompt'ni qabul qiling
3. Home screen'dan oching
4. Offline rejimda test qiling

### iOS
1. Safari'da saytga kiring
2. Add to Home Screen
3. Home screen'dan oching
4. Offline rejimda test qiling

## ✅ Final Checklist

- [ ] Service Worker ro'yxatdan o'tgan
- [ ] Manifest.json yuklanmoqda
- [ ] Icons barcha o'lchamlarda mavjud
- [ ] Offline ishlayapti
- [ ] Install prompt ko'rsatilmoqda
- [ ] Standalone mode ishlayapti
- [ ] Update mechanism ishlayapti
- [ ] Dark mode qo'llab-quvvatlanmoqda
- [ ] Responsive barcha qurilmalarda
- [ ] Performance yaxshi (Lighthouse 90+)
- [ ] Real qurilmalarda test qilingan

---

**Test Sanasi:** _____________  
**Tester:** _____________  
**Natija:** ✅ Pass / ❌ Fail  
**Izohlar:** _____________
