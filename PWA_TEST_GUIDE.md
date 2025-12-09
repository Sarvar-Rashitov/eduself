# PWA Test Qilish Yo'riqnomasi (Lokal Kompyuterda)

## 1. Serverni Ishga Tushirish

### Windows (PowerShell)
```powershell
# Virtual environment aktivlashtirish
.venv\Scripts\Activate.ps1

# Django serverni ishga tushirish
python manage.py runserver
```

### Yoki oddiy CMD
```cmd
# Virtual environment aktivlashtirish
.venv\Scripts\activate

# Django serverni ishga tushirish
python manage.py runserver
```

Server manzili: `http://127.0.0.1:8000/`

## 2. Chrome DevTools bilan Test Qilish

### A. Manifest Faylni Tekshirish

1. Chrome brauzerda saytni oching: `http://127.0.0.1:8000/`
2. `F12` yoki `Ctrl+Shift+I` bosing (DevTools ochish)
3. **Application** tabiga o'ting
4. Chap tarafda **Manifest** ni tanlang

**Tekshirish kerak:**
- ✅ Name: "EduSelf - Ta'lim Platformasi"
- ✅ Short name: "EduSelf"
- ✅ Start URL: "/"
- ✅ Display: "standalone"
- ✅ Theme color: "#4F46E5"
- ✅ Icons: 8 ta icon (72x72 dan 512x512 gacha)

**Agar xatolik ko'rsatsa:**
- Icon fayllar yo'qligini bildiradi (bu normal, keyinroq qo'shamiz)
- Manifest fayli yuklanganini tekshiring

### B. Service Worker Tekshirish

1. DevTools > **Application** > **Service Workers**
2. Quyidagilarni tekshiring:
   - ✅ Status: **activated and is running**
   - ✅ Source: `/static/sw.js`
   - ✅ Scope: `http://127.0.0.1:8000/`

**Service Worker Boshqaruv:**
- **Unregister** - Service Worker'ni o'chirish
- **Update** - Yangilash
- **Offline** - Offline rejimni simulyatsiya qilish

### C. Cache Storage Tekshirish

1. DevTools > **Application** > **Cache Storage**
2. `eduself-v1` cache'ini toping
3. Ichida quyidagi fayllar bo'lishi kerak:
   - `/`
   - `/static/css/style.css`
   - `/static/manifest.json`

**Cache'ni tozalash:**
- Cache nomini bosing > o'ng tugma > Delete

## 3. Lighthouse Audit (PWA Score)

### Lighthouse Ishga Tushirish

1. Chrome DevTools > **Lighthouse** tab
2. Sozlamalar:
   - ✅ **Progressive Web App** ni belgilang
   - ✅ **Desktop** yoki **Mobile** tanlang
   - ⬜ Boshqa kategoriyalarni o'chirish mumkin (tezroq ishlaydi)
3. **Analyze page load** tugmasini bosing

### PWA Score Talablari

**Minimal Score: 70+**

**Asosiy Tekshiruvlar:**
- ✅ Manifest fayli mavjud
- ✅ Service Worker ro'yxatdan o'tgan
- ✅ HTTPS (localhost uchun shart emas)
- ✅ Viewport meta tag
- ✅ Theme color
- ⚠️ Icons (hozircha yo'q, keyinroq qo'shamiz)

**Agar score past bo'lsa:**
- Icon fayllar yo'qligi sabab bo'lishi mumkin (bu normal)
- Boshqa xatolarni o'qib tuzating

## 4. Install Prompt Test Qilish

### Localhost'da Install Qilish

**Muhim:** Localhost'da PWA install qilish uchun quyidagi shartlar bajarilishi kerak:
- ✅ Manifest fayli to'g'ri
- ✅ Service Worker ro'yxatdan o'tgan
- ✅ HTTPS (localhost uchun avtomatik)
- ⚠️ Kamida 192x192 va 512x512 icon kerak

**Install Tugmasi:**
1. Chrome address bar'da (URL yonida) **Install** icon paydo bo'ladi
2. Yoki Chrome menu > **Install EduSelf...**
3. Install qilgandan keyin Desktop'da shortcut paydo bo'ladi

**Agar Install tugmasi ko'rinmasa:**
- Icon fayllar yo'q (asosiy sabab)
- DevTools > Console'da xatolarni tekshiring
- Manifest va Service Worker to'g'riligini qayta tekshiring

## 5. Offline Rejimni Test Qilish

### Offline Simulyatsiya

1. DevTools > **Network** tab
2. **Throttling** dropdown > **Offline** tanlang
3. Sahifani yangilang (`F5`)

**Natija:**
- Asosiy sahifa (`/`) yuklanishi kerak (cache'dan)
- CSS fayli yuklanishi kerak
- Boshqa sahifalar ishlamasligi mumkin (normal)

**Yoki Service Worker orqali:**
1. DevTools > **Application** > **Service Workers**
2. **Offline** checkbox'ni belgilang
3. Sahifani yangilang

## 6. Standalone Mode Test Qilish

### Desktop'da Standalone

1. PWA'ni install qiling (yuqoridagi 4-qadamga qarang)
2. Desktop shortcut'ni oching
3. Tekshiring:
   - ✅ Alohida oyna ochiladi (brauzer UI'siz)
   - ✅ Theme color ko'rinadi
   - ✅ Icon to'g'ri ko'rinadi

### Mobile Simulyatsiya

1. DevTools > **Toggle Device Toolbar** (`Ctrl+Shift+M`)
2. iPhone yoki Android qurilma tanlang
3. Sahifani yangilang
4. Standalone mode'ni simulyatsiya qilish:
   - DevTools > **Application** > **Manifest**
   - **Add to homescreen** tugmasini bosing

## 7. Icon Fayllarni Qo'shish (Ixtiyoriy)

### Icon Yaratish

**Online Tool'lar:**
- https://www.pwabuilder.com/imageGenerator
- https://realfavicongenerator.net/
- https://favicon.io/

**Qadamlar:**
1. Logo rasmingizni tayyorlang (PNG, 512x512 yoki kattaroq)
2. Yuqoridagi tool'lardan birini oching
3. Logo'ni yuklang
4. Barcha o'lchamdagi iconlarni yuklab oling
5. `static/icons/` papkasiga joylashtiring:
   - icon-72x72.png
   - icon-96x96.png
   - icon-128x128.png
   - icon-144x144.png
   - icon-152x152.png
   - icon-192x192.png
   - icon-384x384.png
   - icon-512x512.png

### Static Fayllarni Yangilash

```powershell
python manage.py collectstatic --noinput
```

### Brauzer Cache'ini Tozalash

1. DevTools > **Application** > **Clear storage**
2. **Clear site data** tugmasini bosing
3. Sahifani yangilang (`Ctrl+Shift+R`)

## 8. Muammolarni Hal Qilish

### Service Worker Ro'yxatdan O'tmayapti

**Sabab:** JavaScript xatosi yoki fayl yo'li noto'g'ri

**Yechim:**
```powershell
# Static fayllarni qayta collect qilish
python manage.py collectstatic --noinput

# Brauzer cache'ini tozalash
Ctrl+Shift+R
```

**Tekshirish:**
- DevTools > **Console** > Xatolarni o'qing
- `/static/sw.js` faylini brauzerda ochib ko'ring: `http://127.0.0.1:8000/static/sw.js`

### Manifest Yuklanmayapti

**Sabab:** Fayl yo'li noto'g'ri yoki static fayllar collect qilinmagan

**Yechim:**
```powershell
python manage.py collectstatic --noinput
```

**Tekshirish:**
- `/static/manifest.json` faylini brauzerda ochib ko'ring: `http://127.0.0.1:8000/static/manifest.json`
- DevTools > **Network** > `manifest.json` so'rovini tekshiring

### Install Tugmasi Ko'rinmayapti

**Sabab:** Icon fayllar yo'q yoki manifest noto'g'ri

**Yechim:**
1. Icon fayllarni qo'shing (yuqoridagi 7-qadamga qarang)
2. Manifest'da icon yo'llarini tekshiring
3. DevTools > **Application** > **Manifest** > Xatolarni o'qing

### Offline Ishlamayapti

**Sabab:** Service Worker cache'ga fayllarni qo'shmagan

**Yechim:**
1. DevTools > **Application** > **Cache Storage**
2. `eduself-v1` cache'ini tekshiring
3. Agar bo'sh bo'lsa, Service Worker'ni qayta ro'yxatdan o'tkazing:
   - **Unregister** > Sahifani yangilang

## 9. Production'da Test Qilish

### HTTPS Talab

**Muhim:** Production'da PWA faqat HTTPS orqali ishlaydi!

**Localhost istisno:**
- `http://localhost` va `http://127.0.0.1` HTTPS sifatida qabul qilinadi
- Boshqa IP manzillar uchun HTTPS kerak

### Deployment Checklist

- [ ] Icon fayllar qo'shilgan
- [ ] `python manage.py collectstatic` bajarilgan
- [ ] HTTPS sozlangan
- [ ] Manifest va Service Worker to'g'ri yo'llar
- [ ] ALLOWED_HOSTS sozlangan
- [ ] CSRF_TRUSTED_ORIGINS sozlangan

## 10. Mobil Qurilmada Test Qilish

### Lokal Networkda Test

1. Kompyuter va telefon bir Wi-Fi'ga ulaning
2. Kompyuteringizning IP manzilini toping:
   ```powershell
   ipconfig
   # IPv4 Address ni toping, masalan: 192.168.1.100
   ```
3. Django serverni barcha IP'larga ochiq qiling:
   ```powershell
   python manage.py runserver 0.0.0.0:8000
   ```
4. Telefondan oching: `http://192.168.1.100:8000`

**Muhim:** `settings.py`da ALLOWED_HOSTS'ga IP'ni qo'shing:
```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.1.100']
```

### Mobil Chrome DevTools

1. Telefonda Chrome'da saytni oching
2. Kompyuterda Chrome > `chrome://inspect`
3. Telefoningizni USB orqali ulang
4. **Remote devices** > Telefoningizni tanlang
5. **Inspect** tugmasini bosing

## Xulosa

PWA lokalda test qilish uchun:
1. ✅ Server ishga tushirish
2. ✅ Chrome DevTools > Application
3. ✅ Manifest va Service Worker tekshirish
4. ✅ Lighthouse audit o'tkazish
5. ⚠️ Icon fayllar qo'shish (ixtiyoriy, lekin tavsiya etiladi)
6. ✅ Offline rejimni sinab ko'rish
7. ✅ Install qilish (icon fayllar bo'lsa)

**Minimal ishlash uchun:**
- Manifest ✅
- Service Worker ✅
- Cache ✅

**To'liq PWA uchun:**
- Yuqoridagilar + Icon fayllar ✅
