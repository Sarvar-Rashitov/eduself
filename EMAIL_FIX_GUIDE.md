# 📧 Email Muammosini Hal Qilish

## Muammo
Email tasdiqlash va parolni tiklash funksiyalari ishlamayapti. Emailga xat kelmayapti.

## Sabab
Gmail App Password noto'g'ri yoki eskirgan. `.env` faylidagi `EMAIL_HOST_PASSWORD` qiymati Gmail tomonidan qabul qilinmayapti.

## ✅ Yechim (Qadam-baqadam)

### 1-qadam: Gmail App Password yaratish

1. **Google hisobingizga kiring**: https://myaccount.google.com/

2. **2-bosqichli tasdiqlashni yoqing** (agar yoqilmagan bo'lsa):
   - Security → 2-Step Verification
   - Telefon raqamingizni kiriting va tasdiqlang

3. **App Password yarating**:
   - https://myaccount.google.com/apppasswords ga o'ting
   - "Select app" → "Mail" ni tanlang
   - "Select device" → "Other (Custom name)" ni tanlang
   - Nom: "EduSelf" deb yozing
   - "Generate" tugmasini bosing
   - 16 ta belgidan iborat parol paydo bo'ladi
   - Masalan: `abcd efgh ijkl mnop`

4. **Parolni nusxalang** (bo'sh joylar bilan birga)

### 2-qadam: .env faylini yangilash

`.env` faylini oching va quyidagi qatorni toping:

```env
EMAIL_HOST_PASSWORD=fdiptngunqkutpfg
```

Uni yangi App Password bilan almashtiring (BO'SH JOYSIZ!):

```env
EMAIL_HOST_PASSWORD=abcdefghijklmnop
```

**MUHIM**: 
- Bo'sh joylarni olib tashlang!
- Faqat 16 ta harf/raqam bo'lishi kerak
- Katta-kichik harflar farq qiladi

### 3-qadam: Serverni qayta ishga tushirish

Agar server ishlab turgan bo'lsa, to'xtating (Ctrl+C) va qayta ishga tushiring:

```bash
python manage.py runserver
```

### 4-qadam: Test qilish

Email yuborishni test qiling:

```bash
# Oddiy test
python test_email.py

# Barcha template'larni test qilish
python send_test_emails.py
```

Agar "✅ Email muvaffaqiyatli yuborildi!" degan xabar chiqsa, hammasi to'g'ri!

### 5-qadam: Saytda test qilish

1. Saytga kiring: http://127.0.0.1:8000
2. Ro'yxatdan o'ting (email bilan)
3. Emailingizni tekshiring - tasdiqlash havolasi kelishi kerak

Yoki:

1. "Parolni unutdingizmi?" tugmasini bosing
2. Emailingizni kiriting
3. Emailingizni tekshiring - parolni tiklash havolasi kelishi kerak

## 🔍 Muqobil Yechim: Boshqa Email Provayderdan foydalanish

Agar Gmail bilan muammo bo'lsa, boshqa email provayderdan foydalanishingiz mumkin:

### Yandex Mail

1. Yandex hisobingizga kiring
2. Sozlamalar → Pochta → POP va IMAP
3. "IMAP protokolini yoqish" ni belgilang
4. `.env` faylida:

```env
EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=sizning-email@yandex.ru
EMAIL_HOST_PASSWORD=sizning-parolingiz
DEFAULT_FROM_EMAIL=EduSelf <sizning-email@yandex.ru>
```

### Mail.ru

```env
EMAIL_HOST=smtp.mail.ru
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=sizning-email@mail.ru
EMAIL_HOST_PASSWORD=sizning-parolingiz
DEFAULT_FROM_EMAIL=EduSelf <sizning-email@mail.ru>
```

## 🐛 Debug

Agar hali ham ishlamasa:

1. **Parolni tekshiring**: `.env` faylida bo'sh joylar yo'qligiga ishonch hosil qiling
2. **2-bosqichli tasdiqlash**: Google hisobingizda yoqilganligini tekshiring
3. **Internet aloqasi**: Internet aloqangizni tekshiring
4. **Gmail bloklash**: Gmail hisobingiz bloklanmaganligini tekshiring
5. **Firewall**: Firewall 587 portni bloklamaganligini tekshiring

## 📞 Yordam

Agar muammo hal bo'lmasa:
- Google Support: https://support.google.com/mail/?p=BadCredentials
- Gmail App Passwords: https://support.google.com/accounts/answer/185833

---

**Eslatma**: Bu qo'llanma faqat development uchun. Production'da professional email xizmatidan (SendGrid, Mailgun, AWS SES) foydalanish tavsiya etiladi.
