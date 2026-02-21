# 📱 Telegram Notification Xususiyati

## Nima Qilindi

Barcha email notification'lar endi Telegram bot orqali ham yuboriladi (agar foydalanuvchi Telegram bilan bog'langan bo'lsa).

## ✨ Xususiyatlar

### Qaysi Notification'lar Yuboriladi?

1. **🎉 Xush kelibsiz** - Ro'yxatdan o'tganda
2. **👋 Qaytganingizdan xursandmiz** - 7+ kun kirmaganidan keyin
3. **🔒 Yangi qurilmadan kirish** - Yangi qurilmadan kirish bo'lganda
4. **📚 Sizni sog'indik** - 3+ kun faol bo'lmaganida

### Qachon Yuboriladi?

Telegram notification faqat quyidagi shartlar bajarilganda yuboriladi:
- ✅ Foydalanuvchi Telegram bot bilan bog'langan
- ✅ `telegram_chat_id` mavjud
- ✅ Email notification ham yuborilgan

## 🔧 Texnik Detalllar

### Telegram Bot Integration

`telegram_bot/notification_sender.py` dan foydalaniladi:

```python
from telegram_bot.notification_sender import send_telegram_notification

send_telegram_notification(
    user_id=user.id,
    title="🎉 Xush kelibsiz!",
    message="Assalomu alaykum! EduSelf platformasiga xush kelibsiz!",
    link="https://eduself.uz"
)
```

### Notification Format

```
🔔 [Title]

[Message]

🔗 [Link]
```

## 📧 Email + Telegram

Har bir notification uchun:
1. Email yuboriladi (HTML + text)
2. Telegram notification yuboriladi (agar mavjud bo'lsa)

### 1. Xush Kelibsiz (Register)

**Email**: `emails/welcome.html`
**Telegram**:
```
🎉 Xush kelibsiz!

Assalomu alaykum, [Name]!

EduSelf platformasiga xush kelibsiz! 
Endi siz platformaning barcha imkoniyatlaridan foydalanishingiz mumkin.

🔗 https://eduself.uz
```

### 2. Qaytganingizdan Xursandmiz (Login)

**Email**: `emails/welcome_back.html`
**Telegram**:
```
👋 Qaytganingizdan xursandmiz!

Assalomu alaykum, [Name]!

Siz EduSelf platformasiga qaytib keldingiz. 
Davom eting va bilimingizni oshiring!

🔗 https://eduself.uz
```

### 3. Yangi Qurilmadan Kirish (Security)

**Email**: `emails/new_device_login.html`
**Telegram**:
```
🔒 Yangi qurilmadan kirish

Sizning hisobingizga yangi qurilmadan kirish amalga oshirildi.

📅 Vaqt: 21.02.2026 16:30
📱 Qurilma: Desktop
🌐 Brauzer: Google Chrome
💻 OS: Windows 10

Bu siz bo'lmasa, darhol parolingizni o'zgartiring!

🔗 https://eduself.uz/accounts/forgot-password/
```

### 4. Sizni Sog'indik (Inactive)

**Email**: `emails/inactive_reminder.html`
**Telegram**:
```
📚 Sizni sog'indik!

Assalomu alaykum, [Name]!

Siz 5 kun faol bo'lmadingiz.

📊 Natijalaringiz:
• Jami testlar: 25
• O'tgan testlar: 18
• Umumiy ball: 450
• Progress: 72%

Qaytib kelib, o'qishni davom ettiring!

🔗 https://eduself.uz
```

## 🎯 Foydalanish Stsenariylari

### Stsenariy 1: Telegram Bilan Bog'langan

```
1. Foydalanuvchi Telegram bot orqali ro'yxatdan o'tadi
2. telegram_chat_id saqlanadi
3. Har qanday notification:
   ✅ Email yuboriladi
   ✅ Telegram notification yuboriladi
```

### Stsenariy 2: Telegram Bilan Bog'lanmagan

```
1. Foydalanuvchi email bilan ro'yxatdan o'tadi
2. telegram_chat_id yo'q
3. Har qanday notification:
   ✅ Email yuboriladi
   ❌ Telegram notification yuborilmaydi
```

### Stsenariy 3: Keyinchalik Telegram Bog'lash

```
1. Foydalanuvchi email bilan ro'yxatdan o'tadi
2. Keyinchalik Telegram bot orqali login qiladi
3. telegram_chat_id saqlanadi
4. Keyingi notification'lar:
   ✅ Email yuboriladi
   ✅ Telegram notification yuboriladi
```

## 🔒 Xavfsizlik

### Telegram Chat ID

- Faqat Telegram bot orqali login qilganda saqlanadi
- Xavfsiz saqlash (database'da)
- Faqat o'sha foydalanuvchiga notification yuborish

### Rate Limiting

- Telegram API rate limit: 30 message/second
- Bizning kod: 0.1 soniya kutish har bir xabar orasida
- Global notification uchun: batch processing

## 📊 Monitoring

### Logs

```python
# Success
logger.info(f"Telegram notification yuborildi: {user.username}")

# Error
logger.error(f"Telegram notification xatolik: {e}")
```

### Admin Panel

Admin panelda `telegram_chat_id` ko'rinadi:
- User model → telegram_chat_id field
- Qaysi foydalanuvchilar Telegram bilan bog'langan

## 🧪 Test Qilish

### Manual Test

1. Telegram bot orqali login qiling
2. `telegram_chat_id` saqlanganini tekshiring
3. Logout qiling va qayta login qiling
4. Telegram'da notification kelishini tekshiring

### Code Test

```python
from telegram_bot.notification_sender import send_telegram_notification

# Test notification
send_telegram_notification(
    user_id=1,
    title="Test",
    message="Bu test xabari",
    link="https://eduself.uz"
)
```

## 💡 Best Practices

1. **Fallback**: Agar Telegram xatolik bersa, email hali ham yuboriladi
2. **Async**: Telegram notification async ravishda yuboriladi (blocking yo'q)
3. **Error Handling**: Xatolar log'ga yoziladi, lekin asosiy flow to'xtamaydi
4. **User Choice**: Foydalanuvchi Telegram notification'larni o'chirishi mumkin (kelajakda)

## 🔄 Workflow

```
1. Event yuz beradi (register, login, etc.)
   ↓
2. Email notification yuboriladi
   ↓
3. telegram_chat_id tekshiriladi
   ↓
4. Agar mavjud bo'lsa:
   → Telegram notification yuboriladi (async)
   ↓
5. Xatolik bo'lsa:
   → Log'ga yoziladi
   → Asosiy flow davom etadi
```

## 🎨 Customization

### Notification Matnini O'zgartirish

`accounts/views.py` yoki `accounts/utils.py` da:

```python
send_telegram_notification(
    user_id=user.id,
    title="O'z sarlavhangiz",
    message="O'z xabaringiz",
    link="O'z havolangiz"
)
```

### Emoji Qo'shish

```python
title="🎉 Xush kelibsiz!"
message="📚 Yangi darslar mavjud!\n🔥 Testlarni yeching!"
```

### Link O'zgartirish

```python
# Specific page
link=f"{settings.SITE_URL}/courses/"

# With parameters
link=f"{settings.SITE_URL}/profile/?tab=stats"
```

## 🚀 Kelajakdagi Yaxshilanishlar

1. **Rich Notifications**: Inline buttons, images
2. **User Preferences**: Notification sozlamalari
3. **Notification History**: Yuborilgan notification'lar tarixi
4. **Analytics**: Notification ochilish statistikasi
5. **Custom Templates**: Har xil template'lar
6. **Scheduled Notifications**: Vaqt bo'yicha yuborish
7. **Group Notifications**: Guruh notification'lari

## 📞 Yordam

Muammolar bo'lsa:

1. **Telegram bot ishlamayapti**:
   - `TELEGRAM_BOT_TOKEN` ni tekshiring
   - Bot ishga tushganini tekshiring

2. **Notification kelmayapti**:
   - `telegram_chat_id` mavjudligini tekshiring
   - Log'larni ko'ring
   - Bot'ni restart qiling

3. **Xatolik**:
   - Log fayllarni tekshiring
   - Telegram API status'ni tekshiring

## 🎓 Foydalanuvchi Uchun

### Telegram Notification Olish

1. Telegram bot'ni oching: @edu_self_bot
2. `/start` ni bosing
3. "Login" tugmasini bosing
4. Hisobingizga kiring
5. Endi barcha notification'lar Telegram'ga ham keladi

### Notification O'chirish (Kelajakda)

1. Profilga kiring
2. Sozlamalar → Notification'lar
3. "Telegram notification'lar" ni o'chiring

---

**Eslatma**: Telegram notification'lar email notification'larga qo'shimcha ravishda yuboriladi. Email hali ham asosiy notification kanali hisoblanadi.
