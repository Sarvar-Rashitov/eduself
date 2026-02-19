# Email Sozlash Ko'rsatmasi

## Gmail App Password Olish

Email tasdiqlash funksiyasini ishga tushirish uchun Gmail App Password kerak.

### 1-qadam: Google hisobingizda 2-bosqichli tasdiqlashni yoqing

1. Google hisobingizga kiring: https://myaccount.google.com/
2. "Security" (Xavfsizlik) bo'limiga o'ting
3. "2-Step Verification" (2-bosqichli tasdiqlash) ni yoqing

### 2-qadam: App Password yarating

1. Google hisobingizda: https://myaccount.google.com/apppasswords
2. "Select app" dan "Mail" ni tanlang
3. "Select device" dan "Other" ni tanlang va "EduSelf" deb nomlang
4. "Generate" tugmasini bosing
5. 16 ta belgidan iborat parol paydo bo'ladi (masalan: `abcd efgh ijkl mnop`)

### 3-qadam: .env faylini yangilang

`.env` faylida quyidagi qatorlarni to'ldiring:

```env
EMAIL_HOST_USER=sizning-gmail@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop
DEFAULT_FROM_EMAIL=EduSelf <sizning-gmail@gmail.com>
```

**Muhim:**
- `EMAIL_HOST_PASSWORD` ga App Password ni bo'sh joysiz kiriting
- `EMAIL_HOST_USER` ga o'zingizning Gmail manzilingizni kiriting
- `DEFAULT_FROM_EMAIL` ga ham o'sha Gmail manzilini kiriting

### 4-qadam: Serverni qayta ishga tushiring

```bash
# Agar server ishlab turgan bo'lsa, to'xtating va qayta ishga tushiring
python manage.py runserver
```

## Muqobil: Boshqa Email Provayderlar

### Yandex Mail

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

## Tekshirish

Email sozlamalari to'g'ri ishlayotganini tekshirish uchun:

1. Profilga kiring
2. Email manzilini kiriting (agar kiritilmagan bo'lsa)
3. "Emailni tasdiqlash" tugmasini bosing
4. Emailingizni tekshiring - tasdiqlash havolasi kelishi kerak

Agar xatolik yuz bersa:
- Gmail App Password to'g'ri kiritilganini tekshiring
- 2-bosqichli tasdiqlash yoqilganini tekshiring
- Internet aloqangizni tekshiring
