# 📢 Admin Notification Email Xususiyati

## Nima Qilindi

Admin paneldan yaratilgan bildirishnomalar endi email orqali ham yuboriladi (Telegram bilan birga).

## ✨ Xususiyatlar

### Notification Turlari

Admin panelda 6 xil notification turi mavjud:
1. **📰 Yangilik** - Platformadagi yangiliklar
2. **📝 Yangi test** - Yangi test qo'shilganda
3. **🎓 Yangi sertifikat** - Yangi sertifikat mavjud
4. **📊 Yangi mock exam** - Yangi mock imtihon
5. **🎬 Yangi kurs** - Yangi video kurs
6. **⚙️ Tizim xabari** - Muhim tizim xabarlari

### Yuborish Turlari

1. **Shaxsiy Notification**
   - Bitta foydalanuvchiga
   - Email + Telegram

2. **Global Notification**
   - Barcha foydalanuvchilarga
   - Email (tasdiqlangan email'larga)
   - Telegram (bog'langan foydalanuvchilarga)

## 🔧 Texnik Detalllar

### Django Signal

`core/signals.py` da `post_save` signal:

```python
@receiver(post_save, sender=Notification)
def send_notification_email(sender, instance, created, **kwargs):
    if not created:
        return  # Faqat yangi notification
    
    if instance.is_global:
        # Barcha foydalanuvchilarga
        users = User.objects.filter(
            is_active=True,
            email__isnull=False,
            email_verified=True
        )
        for user in users:
            send_email_to_user(user)
    else:
        # Shaxsiy notification
        send_email_to_user(instance.user)
```

### Email Template

`templates/emails/notification.html`:
- Base template'dan extends
- Logo va header
- Notification title va message
- "Batafsil ko'rish" tugmasi (agar link bo'lsa)
- Footer

### Admin Panel

`core/admin.py` da `NotificationAdmin`:
- Notification yaratilganda success message
- Email va Telegram yuborilish haqida ma'lumot
- Global/Shaxsiy farqi

## 📧 Email Tarkibi

```
┌─────────────────────────────────┐
│   📚 EduSelf (gradient header)  │
│      Ta'lim platformasi         │
├─────────────────────────────────┤
│                                 │
│  Assalomu alaykum, User! 👋     │
│                                 │
│  [Notification Type]            │
│  [Title]                        │
│                                 │
│  [Message]                      │
│                                 │
│  ┌─────────────────────┐        │
│  │  🔗 Batafsil ko'rish│        │
│  └─────────────────────┘        │
│                                 │
│  📱 EduSelf platformasi         │
│  • Yangi testlar                │
│  • Video darslar                │
│  • Sertifikatlar                │
│                                 │
├─────────────────────────────────┤
│  EduSelf - Ta'lim platformasi   │
│  📱 Telegram  🌐 Sayt           │
│  © 2024 EduSelf                 │
└─────────────────────────────────┘
```

## 🎯 Foydalanish

### Admin Panelda

1. Django admin'ga kiring
2. "Bildirishnomalar" bo'limiga o'ting
3. "Bildirishnoma qo'shish" ni bosing
4. Formani to'ldiring:
   - **Turi**: Notification turini tanlang
   - **Sarlavha**: Qisqa sarlavha
   - **Xabar**: Batafsil xabar (ko'p qatorli)
   - **Havola**: Qo'shimcha havola (ixtiyoriy)
   - **Icon**: Bootstrap icon klassi
   - **Foydalanuvchi**: Shaxsiy notification uchun
   - **Barcha foydalanuvchilar uchun**: Global notification
5. "Saqlash" ni bosing
6. ✅ Email va Telegram avtomatik yuboriladi!

### Shaxsiy Notification

```
Turi: Tizim xabari
Sarlavha: Sizning hisobingiz yangilandi
Xabar: Hisobingizda yangi xususiyatlar mavjud.
Havola: https://eduself.uz/profile/
Foydalanuvchi: [Tanlang]
Barcha foydalanuvchilar uchun: ❌
```

**Natija:**
- ✅ 1 ta email yuboriladi
- ✅ 1 ta Telegram notification (agar mavjud)

### Global Notification

```
Turi: Yangilik
Sarlavha: Platformada yangi xususiyatlar!
Xabar: Endi email va Telegram notification'lar mavjud!
Havola: https://eduself.uz
Barcha foydalanuvchilar uchun: ✅
```

**Natija:**
- ✅ 92 ta email yuboriladi (tasdiqlangan email'lar)
- ✅ 258 ta Telegram notification (bog'langan foydalanuvchilar)

## 📊 Monitoring

### Admin Panel Message

Notification yaratilganda admin panelda success message:

**Shaxsiy:**
```
✅ Shaxsiy bildirishnoma yaratildi!
👤 Foydalanuvchi: John (john@example.com)
📧 Email va 📱 Telegram orqali yuborilmoqda
```

**Global:**
```
✅ Global bildirishnoma yaratildi!
📧 Email: 92 ta foydalanuvchiga yuborilmoqda
📱 Telegram: 258 ta foydalanuvchiga yuborilmoqda
```

### Logs

```python
# core/signals.py
logger.info(f"Notification email yuborildi: {user.email}")
logger.info(f"Global notification: {users.count()} ta foydalanuvchiga")
logger.error(f"Notification email yuborishda xatolik: {e}")
```

## 🧪 Test Qilish

### Manual Test

```bash
# Test script
python test_admin_notification.py

# Yoki admin panelda
# 1. Admin'ga kiring
# 2. Notification yarating
# 3. Email inbox'ni tekshiring
```

### Test Script Natijalari

```
======================================================================
ADMIN NOTIFICATION EMAIL TEST
======================================================================
📧 Email tasdiqlangan foydalanuvchilar: 92

======================================================================
TEST NOTIFICATION YARATISH
======================================================================
Foydalanuvchi: EduSelf (sarvarrashitov4321@gmail.com)
======================================================================

1️⃣  Shaxsiy notification yaratish...
   ✅ Yaratildi! ID: 43
   📧 Email yuborilmoqda: sarvarrashitov4321@gmail.com

2️⃣  Global notification yaratish (test)...
   ⚠️  Bu haqiqiy global notification yaratadi!
   ⚠️  Barcha foydalanuvchilarga email yuboriladi!
```

## 💡 Best Practices

### Shaxsiy Notification

**Qachon ishlatish:**
- Foydalanuvchiga maxsus xabar
- Shaxsiy taklif yoki eslatma
- Hisobga oid xabarlar

**Misol:**
```
Sarlavha: Sizning sertifikatingiz tayyor!
Xabar: Tabriklaymiz! Siz "Python Asoslari" kursini muvaffaqiyatli tugatdingiz.
Havola: https://eduself.uz/certificates/123
```

### Global Notification

**Qachon ishlatish:**
- Platformadagi yangiliklar
- Yangi xususiyatlar
- Muhim tizim xabarlari
- Tadbirlar va aksiyalar

**Misol:**
```
Sarlavha: Yangi video kurslar qo'shildi!
Xabar: Endi platformada 50+ yangi video kurs mavjud. Bepul ko'ring!
Havola: https://eduself.uz/courses/
```

## ⚠️ Ehtiyot Bo'lish

### Global Notification

- ⚠️ Barcha foydalanuvchilarga yuboriladi
- ⚠️ Juda ko'p email (spam bo'lishi mumkin)
- ⚠️ Faqat muhim xabarlar uchun
- ⚠️ Tez-tez yubormaslik

### Email Limit

- Gmail: 500 email/kun (free)
- Professional service tavsiya etiladi (SendGrid, Mailgun)

## 🔄 Workflow

```
1. Admin notification yaratadi
   ↓
2. Django signal ishga tushadi (post_save)
   ↓
3. Email yuborish funksiyasi chaqiriladi
   ↓
4. Agar global:
   → Barcha foydalanuvchilarga email
   → Barcha foydalanuvchilarga Telegram
   ↓
5. Agar shaxsiy:
   → Bitta foydalanuvchiga email
   → Bitta foydalanuvchiga Telegram
   ↓
6. Log'lash va monitoring
```

## 🎨 Customization

### Email Template O'zgartirish

`templates/emails/notification.html` ni tahrirlang:

```html
{% extends "emails/base_email.html" %}

{% block content %}
<!-- O'z dizayningiz -->
{% endblock %}
```

### Signal O'zgartirish

`core/signals.py` da:

```python
# Qo'shimcha shartlar
if notification.notification_type == NotificationType.NEWS:
    # Faqat yangiliklar uchun email yuborish
    send_email_to_user(user)
```

## 📞 Yordam

Muammolar bo'lsa:

1. **Email yuborilmayapti**:
   - Email sozlamalarini tekshiring
   - Signal ishlab turganini tekshiring
   - Log'larni ko'ring

2. **Telegram yuborilmayapti**:
   - Telegram bot ishlab turganini tekshiring
   - telegram_chat_id mavjudligini tekshiring

3. **Global notification juda ko'p vaqt oladi**:
   - Bu normal (ko'p foydalanuvchi)
   - Background task ishlatish tavsiya etiladi (Celery)

## 🚀 Kelajakdagi Yaxshilanishlar

1. **Background Tasks**: Celery bilan async yuborish
2. **Email Queue**: Email queue management
3. **Scheduling**: Vaqt bo'yicha yuborish
4. **Templates**: Turli template'lar
5. **Analytics**: Email ochilish statistikasi
6. **Segmentation**: Foydalanuvchi guruhlariga yuborish

---

**Eslatma**: Admin paneldan yaratilgan har bir notification avtomatik ravishda email va Telegram orqali yuboriladi. Signal orqali ishlaydi.
