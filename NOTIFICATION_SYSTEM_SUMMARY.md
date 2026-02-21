# EduSelf Notification System - To'liq Xulosa

## 📧 Email Notification Turlari

### 1. Avtomatik Email Notification'lar (Alohida ishlaydi)

Quyidagi emaillar avtomatik yuboriladi va admin notification'dan **ALOHIDA** ishlaydi:

#### 1.1. Email Tasdiqlash (Verify Email)
- **Qachon:** Yangi foydalanuvchi email bilan ro'yxatdan o'tganda
- **Template:** `templates/emails/verify_email.html`
- **Kod:** `accounts/views.py` - `register_view()`
- **Telegram:** Yo'q

#### 1.2. Xush Kelibsiz (Welcome)
- **Qachon:** Yangi foydalanuvchi ro'yxatdan o'tganda
- **Template:** `templates/emails/welcome.html`
- **Kod:** `accounts/views.py` - `register_view()`
- **Telegram:** Ha (agar telegram_chat_id bo'lsa)

#### 1.3. Qaytganingizdan Xursandmiz (Welcome Back)
- **Qachon:** Foydalanuvchi 7+ kun login qilmagan bo'lsa
- **Template:** `templates/emails/welcome_back.html`
- **Kod:** `accounts/views.py` - `login_view()`
- **Telegram:** Ha (agar telegram_chat_id bo'lsa)

#### 1.4. Yangi Qurilmadan Kirish (New Device Login)
- **Qachon:** Yangi qurilmadan login qilganda
- **Template:** `templates/emails/new_device_login.html`
- **Kod:** `accounts/utils.py` - `send_new_device_email()`
- **Telegram:** Ha (agar telegram_chat_id bo'lsa)

#### 1.5. Parolni Tiklash (Reset Password)
- **Qachon:** Foydalanuvchi parolni unutgan bo'lsa
- **Template:** `templates/emails/reset_password.html`
- **Kod:** `accounts/views.py` - `forgot_password_view()`
- **Telegram:** Yo'q

#### 1.6. Faol Bo'lmagan Foydalanuvchi (Inactive Reminder)
- **Qachon:** 3+ kun faol bo'lmagan foydalanuvchilarga
- **Template:** `templates/emails/inactive_reminder.html`
- **Kod:** `accounts/management/commands/send_inactive_reminders.py`
- **Telegram:** Ha (agar telegram_chat_id bo'lsa)
- **Ishga tushirish:** `python manage.py send_inactive_reminders`

---

### 2. Admin Panel Notification'lar (Alohida ishlaydi)

Admin paneldan yaratilgan notification'lar **ALOHIDA** ishlaydi:

#### 2.1. Shaxsiy Notification
- **Qachon:** Admin bitta foydalanuvchiga notification yaratganda
- **Template:** `templates/emails/notification.html`
- **Kod:** `core/signals.py` - `send_notification_email_and_telegram()`
- **Email:** Ha (agar email_verified=True)
- **Telegram:** Ha (agar telegram_id bo'lsa)

#### 2.2. Global Notification
- **Qachon:** Admin barcha foydalanuvchilarga notification yaratganda
- **Template:** `templates/emails/notification.html`
- **Kod:** `core/signals.py` - `send_notification_email_and_telegram()`
- **Email:** Barcha email tasdiqlangan foydalanuvchilarga (92 ta)
- **Telegram:** Barcha telegram ulangan foydalanuvchilarga (260 ta)

---

## 🔄 Ishlash Mexanizmi

### Avtomatik Email'lar
```
Hodisa (register, login, etc.)
    ↓
Email yuborish funksiyasi chaqiriladi
    ↓
Email template render qilinadi
    ↓
Email yuboriladi
    ↓
Log'lanadi
```

### Admin Notification'lar
```
Admin notification yaratadi
    ↓
Django signal ishga tushadi (post_save)
    ↓
Background thread'da email va telegram yuboriladi
    ↓
Email: barcha email tasdiqlanganlarga
Telegram: barcha telegram ulanganlarga
    ↓
Log'lanadi
```

---

## 📊 Statistika

| Tur | Email | Telegram | Async |
|-----|-------|----------|-------|
| Email tasdiqlash | ✅ | ❌ | ❌ |
| Welcome | ✅ | ✅ | ❌ |
| Welcome back | ✅ | ✅ | ❌ |
| New device login | ✅ | ✅ | ❌ |
| Reset password | ✅ | ❌ | ❌ |
| Inactive reminder | ✅ | ✅ | ❌ |
| Admin notification | ✅ | ✅ | ✅ |

---

## 🎯 Asosiy Farqlar

### Avtomatik Email'lar:
- ✅ Alohida template'lar
- ✅ Alohida funksiyalar
- ✅ Hodisaga bog'liq (register, login, etc.)
- ✅ Faqat tegishli foydalanuvchiga yuboriladi
- ❌ Admin paneldan boshqarilmaydi

### Admin Notification'lar:
- ✅ Bitta template (`notification.html`)
- ✅ Signal orqali ishlaydi
- ✅ Admin paneldan yaratiladi
- ✅ Shaxsiy yoki global bo'lishi mumkin
- ✅ Async yuboriladi (background thread)

---

## 🧪 Test Qilish

### Avtomatik Email'larni Test Qilish
```bash
python test_all_notifications.py
```

### Admin Notification'ni Test Qilish
```bash
python test_signal_working.py
```

### Global Notification'ni Test Qilish
```bash
python send_final_maintenance_notification.py
```

---

## 📝 Logging

Barcha email yuborish jarayoni log'lanadi:

```
✅ Email yuborildi: user@example.com
✅ Telegram yuborildi: username
❌ Email yuborishda xatolik: [xatolik]
📊 Jami yuborildi: X email, Y telegram
```

---

## 🚀 Production Deploy

1. Kodni deploy qiling
2. Server restart qiling
3. Admin paneldan test notification yarating
4. Log'larni kuzating
5. Email va Telegram'ni tekshiring

---

## ✅ Xulosa

Barcha notification turlari **ALOHIDA** ishlaydi:

1. ✅ Email tasdiqlash - alohida
2. ✅ Welcome - alohida
3. ✅ Welcome back - alohida
4. ✅ New device login - alohida
5. ✅ Reset password - alohida
6. ✅ Inactive reminder - alohida
7. ✅ Admin notification - alohida (signal orqali)

Hech qanday konflikt yo'q. Barcha funksiyalar to'g'ri ishlaydi! 🎉

---

**Muallif:** Kiro AI Assistant  
**Sana:** 2026-02-22  
**Versiya:** 1.0
