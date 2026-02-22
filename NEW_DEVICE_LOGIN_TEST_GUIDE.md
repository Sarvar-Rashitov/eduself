# Yangi Qurilmadan Kirish Email Testi

## Muammo
Yangi qurilmadan kirish emaili kelmayapti.

## Yechim
Logging qo'shildi va `fail_silently=False` qilindi.

## Test Qilish

### 1. Local Test (Development)
```bash
# Django development server ishga tushiring
python manage.py runserver

# Browser'da login qiling
# Console'da loglarni ko'ring
```

### 2. Production Test (Render.com)

#### A. Yangi Browser'dan Login
1. **Incognito/Private mode** ochingbrowserda
2. https://eduself.uz ga kiring
3. Login qiling (email yoki Google bilan)
4. Emailingizni tekshiring

#### B. Boshqa Qurilmadan Login
1. **Telefon** yoki **boshqa kompyuter**dan kiring
2. https://eduself.uz ga kiring
3. Login qiling
4. Emailingizni tekshiring

#### C. Render Logs Tekshirish
```bash
# Render.com dashboard'da:
1. Your Web Service > Logs
2. "send_new_device_email" deb qidiring
3. Loglarni o'qing:
   - "📧 send_new_device_email chaqirildi"
   - "✅ New device email yuborildi"
   - Yoki xatolik bo'lsa: "❌ New device email yuborishda xatolik"
```

## Yangi Qurilma Qanday Aniqlanadi?

### LoginHistory Model
```python
class LoginHistory(models.Model):
    user = models.ForeignKey(User)
    ip_address = models.CharField()
    user_agent = models.CharField()
    device_type = models.CharField()  # Desktop, Mobile, Tablet
    browser = models.CharField()      # Chrome, Firefox, Safari, etc.
    os = models.CharField()           # Windows, macOS, Android, iOS
    is_new_device = models.BooleanField()
    login_time = models.DateTimeField()
```

### Yangi Qurilma Tekshirish Logikasi
```python
def is_new_device(user, ip_address, user_agent):
    # Oxirgi 30 kundagi kirish tarixini tekshirish
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    # Bir xil IP va user agent bilan kirish bo'lganmi?
    existing_login = LoginHistory.objects.filter(
        user=user,
        ip_address=ip_address,
        user_agent=user_agent,
        login_time__gte=thirty_days_ago
    ).exists()
    
    return not existing_login  # Agar topilmasa, yangi qurilma
```

## Email Yuborilish Sharti

### 1. Email Bor va Tasdiqlangan
```python
if not user.email or not user.email_verified:
    return False  # Email yuborilmaydi
```

### 2. Yangi Qurilma
```python
if login_history.is_new_device:
    send_new_device_email(user, login_history, request)
```

### 3. Email Backend
- **From**: eduselfuz@gmail.com (avtomatik emaillar)
- **Subject**: EduSelf - Yangi qurilmadan kirish
- **Template**: templates/emails/new_device_login.html

## Logging

### Muvaffaqiyatli
```
📧 send_new_device_email chaqirildi: user@example.com
📝 Email template yaratilmoqda...
📧 Email yuborilmoqda: user@example.com
✅ New device email yuborildi: user@example.com
```

### Xatolik
```
❌ Email yo'q yoki tasdiqlanmagan: user@example.com, verified=False
```
yoki
```
❌ New device email yuborishda xatolik: [xatolik matni]
```

## Admin Panel Tekshirish

### LoginHistory
1. Admin panel > Login History
2. Oxirgi kirishlarni ko'ring
3. `is_new_device` ustunini tekshiring
4. Yangi qurilma bo'lsa, `True` bo'lishi kerak

### User
1. Admin panel > Users
2. Foydalanuvchini toping
3. `email_verified` ustunini tekshiring
4. `True` bo'lishi kerak

## Muammolarni Hal Qilish

### Email kelmayapti
1. **Email tasdiqlangan**mi? → Admin panelda tekshiring
2. **Yangi qurilma**mi? → LoginHistory'da `is_new_device=True` bo'lishi kerak
3. **Render logs**ni tekshiring → Xatolik bormi?
4. **Spam papka**ni tekshiring
5. **Gmail'da qidiring** → "EduSelf" yoki "eduselfuz"

### is_new_device = False
Agar bir xil qurilmadan kirgan bo'lsangiz:
1. **Boshqa browser** ishlatib ko'ring (Chrome → Firefox)
2. **Incognito mode** ishlatib ko'ring
3. **Boshqa qurilma** ishlatib ko'ring (telefon, boshqa kompyuter)
4. **30 kun kutib ko'ring** (eski login history o'chadi)

### Email tasdiqlangan emas
```bash
# Django shell'da:
python manage.py shell

from accounts.models import User
user = User.objects.get(email='user@example.com')
user.email_verified = True
user.save()
```

## Test Natijasi

Agar barcha shart bajarilsa:
- ✅ LoginHistory yaratiladi
- ✅ is_new_device = True
- ✅ Email yuboriladi (eduselfuz@gmail.com dan)
- ✅ Telegram notification yuboriladi (agar telegram_chat_id bor bo'lsa)

## Qo'shimcha Ma'lumot

### Email Template
- **Location**: templates/emails/new_device_login.html
- **Variables**: user_name, login_time, device_type, browser, os, ip_address, reset_password_url

### Telegram Notification
Agar foydalanuvchida `telegram_chat_id` bo'lsa, Telegram botga ham notification yuboriladi.

### Xavfsizlik
- Foydalanuvchiga parolni tiklash havolasi yuboriladi
- IP manzil va qurilma ma'lumotlari ko'rsatiladi
- Agar bu foydalanuvchi bo'lmasa, darhol parolni o'zgartirish tavsiya etiladi
