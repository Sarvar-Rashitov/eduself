# Test Checklist - EduSelf Yangilanishlari

## ✅ Test Qilish Kerak Bo'lgan Funksiyalar

### 0. Footer Mobil Dizayni
- [ ] Mobil telefondan saytni ochish
- [ ] Footer matnlari chapdan joylashganini tekshirish
- [ ] Footer logo chapdan joylashganini tekshirish
- [ ] Social linklar chapdan joylashganini tekshirish
- [ ] Footer bottom linklar chapdan joylashganini tekshirish
- [ ] 481px+ ekranda footer 2 ustunda joylashishini tekshirish
- [ ] 768px+ ekranda footer 3 ustunda joylashishini tekshirish
- [ ] Barcha matnlar o'qilishi oson bo'lishini tekshirish

### 1. Mobil Tugmalar (Test Natijasi Sahifasi)
- [ ] Mobil telefondan test natijasi sahifasini ochish
- [ ] "Qayta urinish", "Tahlil", "Ortga" tugmalari vertikal joylashganini tekshirish
- [ ] Tugmalar orasida 12px bo'sh joy borligini tekshirish
- [ ] Katta ekranda (576px+) tugmalar gorizontal joylashishini tekshirish
- [ ] Barcha test turlari uchun tekshirish:
  - [ ] Oddiy test natijasi
  - [ ] Sertifikat test natijasi
  - [ ] Mock exam natijasi

### 2. Username va Email Validatsiyasi
- [ ] Ro'yxatdan o'tish sahifasini ochish
- [ ] Band username kiritib ko'rish
  - [ ] Xatolik xabari: "Bu foydalanuvchi nomi allaqachon band. Boshqa nom tanlang."
- [ ] Band email kiritib ko'rish
  - [ ] Xatolik xabari: "Bu email allaqachon ro'yxatdan o'tgan..."
- [ ] Username ko'rsatmasi ko'rinishini tekshirish
- [ ] Parol ko'rsatmasi ko'rinishini tekshirish
- [ ] Xatolik xabarlarda icon borligini tekshirish

### 3. Login Validatsiyasi
- [ ] Login sahifasini ochish
- [ ] Noto'g'ri username/parol kiritish
  - [ ] Xatolik xabari: "Foydalanuvchi nomi yoki parol noto'g'ri..."
- [ ] Bo'sh maydonlar bilan yuborish
  - [ ] Username: "Foydalanuvchi nomini kiriting."
  - [ ] Parol: "Parolni kiriting."

### 4. Mock Exam Kategoriyalari
- [ ] Admin panelga kirish
- [ ] "Mock imtihon kategoriyalari" bo'limini topish
- [ ] Yangi kategoriya qo'shish:
  - [ ] Nom: "DTM Imtihonlari"
  - [ ] Slug: "dtm-imtihonlari"
  - [ ] Icon: "bi-clipboard-check"
  - [ ] Saqlash
- [ ] Mock Exam qo'shish va kategoriyani tanlash
- [ ] Mock Exam sahifasida kategoriya filterlari ko'rinishini tekshirish
- [ ] Kategoriya bo'yicha filterlash ishlashini tekshirish

### 5. PWA Funksiyalari
- [ ] Chrome DevTools > Application > Manifest
  - [ ] Manifest fayli yuklanganini tekshirish
  - [ ] Barcha ma'lumotlar to'g'riligini tekshirish
- [ ] Service Worker
  - [ ] Service Worker ro'yxatdan o'tganini tekshirish
  - [ ] Status: "activated"
- [ ] Lighthouse Audit
  - [ ] PWA score tekshirish (70+ bo'lishi kerak)
- [ ] Mobil qurilmada
  - [ ] "Add to Home Screen" tugmasi paydo bo'lishini kutish
  - [ ] Ilovani o'rnatish
  - [ ] Standalone rejimda ochilishini tekshirish
  - [ ] Offline rejimda ishlashini tekshirish (asosiy sahifa)

### 6. Icon Fayllar (Qo'shimcha)
- [ ] `static/icons/` papkasiga icon fayllarni qo'shish
- [ ] Barcha o'lchamlar mavjudligini tekshirish:
  - [ ] icon-72x72.png
  - [ ] icon-96x96.png
  - [ ] icon-128x128.png
  - [ ] icon-144x144.png
  - [ ] icon-152x152.png
  - [ ] icon-192x192.png
  - [ ] icon-384x384.png
  - [ ] icon-512x512.png
- [ ] `python manage.py collectstatic --noinput` ishga tushirish
- [ ] PWA manifest'da iconlar ko'rinishini tekshirish

## Test Qilish Yo'riqnomasi

### Mobil Test Qilish
1. Chrome DevTools > Toggle Device Toolbar (Ctrl+Shift+M)
2. iPhone 12 Pro yoki Samsung Galaxy S20 tanlash
3. Har bir sahifani ochib ko'rish

### Desktop Test Qilish
1. Brauzer oynasini kengaytirish (1920x1080)
2. Responsive dizayn ishlashini tekshirish
3. Tugmalar gorizontal joylashishini tekshirish

### PWA Test Qilish
1. HTTPS orqali saytni ochish (yoki localhost)
2. Chrome DevTools > Application
3. Manifest va Service Worker tekshirish
4. Lighthouse audit o'tkazish

## Muammolar Yuzaga Kelsa

### Tugmalar Hali Ham Yopishib Turibdi
```bash
# Brauzer cache'ini tozalash
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (Mac)

# Yoki
python manage.py collectstatic --noinput
```

### PWA Ishlamayapti
```bash
# Service Worker qayta ro'yxatdan o'tkazish
1. DevTools > Application > Service Workers
2. "Unregister" tugmasini bosing
3. Sahifani yangilang (F5)
```

### Migration Xatolari
```bash
python manage.py migrate
```

### Static Fayllar Yuklanmayapti
```bash
python manage.py collectstatic --noinput
```

## Natijalar

Test qilish sanasi: _______________

| Funksiya | Status | Izoh |
|----------|--------|------|
| Footer mobil dizayni | ⬜ | |
| Mobil tugmalar | ⬜ | |
| Username validatsiyasi | ⬜ | |
| Email validatsiyasi | ⬜ | |
| Login validatsiyasi | ⬜ | |
| Mock Exam kategoriyalari | ⬜ | |
| PWA Manifest | ⬜ | |
| Service Worker | ⬜ | |
| Icon fayllar | ⬜ | |

Legend: ✅ Ishlayapti | ❌ Ishlamayapti | ⬜ Test qilinmagan

### 7. Bosh Sahifa Optimallashtirildi
- [ ] Bosh sahifani ochish
- [ ] Fanlar bo'limida 3 ta fan ko'rinishini tekshirish (oldin 6 ta edi)
- [ ] Sertifikatlar bo'limida 3 ta sertifikat ko'rinishini tekshirish (oldin 4 ta edi)
- [ ] Sahifa tezroq yuklanishini tekshirish

### 8. Qidiruv Funksiyasi (Barcha Bo'limlar)
- [ ] **Fanlar sahifasi:**
  - [ ] Qidiruv maydoniga "Matematika" yozish
  - [ ] Natijalar real-time ko'rinishini tekshirish
  - [ ] "X" tugmasi bilan qidiruvni tozalash
- [ ] **Mavzular sahifasi:**
  - [ ] Biror fanga kirish
  - [ ] Mavzular qidiruvi ishlashini tekshirish
- [ ] **Sertifikatlar sahifasi:**
  - [ ] Sertifikatlar sahifasini ochish
  - [ ] Qidiruv funksiyasi ishlashini tekshirish
- [ ] **Mock Exam sahifasi:**
  - [ ] Mock Exam sahifasini ochish
  - [ ] Imtihonlarni qidirishni tekshirish
- [ ] **Muassasalar sahifasi:**
  - [ ] Muassasalar sahifasini ochish
  - [ ] Muassasa nomi bo'yicha qidirishni tekshirish
  - [ ] Muassasa turi bo'yicha qidirishni tekshirish

### 8. PWA Install Prompt
- [ ] Mobil telefondan saytni ochish (yoki Chrome DevTools'da mobil rejim)
- [ ] 3 soniya kutish
- [ ] Install prompt paydo bo'lishini kutish
- [ ] "O'rnatish" tugmasi ishlashini tekshirish
- [ ] "Keyinroq" tugmasi bosganda prompt yo'qolishini tekshirish
- [ ] Sahifani yangilab, prompt qayta chiqmasligini tekshirish (7 kun davomida)
- [ ] LocalStorage'da `installPromptDismissed` qiymatini tekshirish
- [ ] Animatsiya va dizayn chiroyligi

## Yangi Test Natijalari

| Funksiya | Status | Izoh |
|----------|--------|------|
| Bosh sahifa optimallashtirildi | ⬜ | |
| Fanlar qidiruvi | ⬜ | |
| Mavzular qidiruvi | ⬜ | |
| Sertifikatlar qidiruvi | ⬜ | |
| Mock Exam qidiruvi | ⬜ | |
| Muassasalar qidiruvi | ⬜ | |
| PWA Install Prompt | ⬜ | |