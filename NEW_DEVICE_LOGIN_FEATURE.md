# 🔒 Yangi Qurilmadan Kirish Xavfsizlik Xususiyati

## Nima Qilindi

Foydalanuvchi yangi qurilmadan kirganida, unga xavfsizlik ogohlantirish email yuboriladi.

## ✨ Xususiyatlar

### Qachon Email Yuboriladi?

Email faqat **yangi qurilmadan kirish** bo'lganda yuboriladi:
- Yangi IP manzil
- Yangi brauzer
- Yangi qurilma turi (Desktop, Mobile, Tablet)
- Oxirgi 30 kun ichida bunday kirish bo'lmagan

### Nima Uchun Bu Muhim?

1. **Xavfsizlik**: Agar kimdir ruxsatsiz kirgan bo'lsa, foydalanuvchi darhol bilib oladi
2. **Ogohlantirish**: Shubhali faoliyatni tezda aniqlash
3. **Himoya**: Parolni tezda o'zgartirish imkoniyati
4. **Ishonch**: Foydalanuvchi hisobining xavfsizligini his qiladi

## 📧 Email Tarkibi

**"Yangi qurilmadan kirish" email:**
- 🔔 Xavfsizlik ogohlantirishi
- 📅 Kirish vaqti
- 📱 Qurilma turi (Desktop, Mobile, Tablet)
- 🌐 Brauzer (Chrome, Firefox, Safari, etc.)
- 💻 Operatsion tizim (Windows, macOS, Android, iOS, etc.)
- 🌍 IP manzil
- 📍 Joylashuv (agar mavjud bo'lsa)
- 🔒 "Parolni o'zgartirish" tugmasi
- 💡 Xavfsizlik maslahatlari

## 🔧 Texnik Detalllar

### Database Model (`LoginHistory`)

```python
class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device_type = models.CharField(max_length=50)  # Desktop, Mobile, Tablet
    browser = models.CharField(max_length=100)     # Chrome, Firefox, etc.
    os = models.CharField(max_length=100)          # Windows, macOS, etc.
    location = models.CharField(max_length=255)
    is_new_device = models.BooleanField(default=False)
    login_time = models.DateTimeField(auto_now_add=True)
```

### Helper Functions (`accounts/utils.py`)

1. **get_client_ip(request)** - IP manzilni olish
2. **parse_user_agent(user_agent_string)** - User agent'dan ma'lumot ajratish
3. **is_new_device(user, ip_address, user_agent)** - Yangi qurilmani aniqlash
4. **create_login_history(user, request)** - Kirish tarixini saqlash
5. **send_new_device_email(user, login_history, request)** - Email yuborish

### Login Flow

```python
def login_view(request):
    # 1. Login form validation
    user = form.get_user()
    
    # 2. Kirish tarixini yaratish
    login_history = create_login_history(user, request)
    
    # 3. Login qilish
    login(request, user)
    
    # 4. Yangi qurilma bo'lsa, email yuborish
    if login_history.is_new_device:
        send_new_device_email(user, login_history, request)
```

## 🎯 Foydalanish Stsenariylari

### Stsenariy 1: Birinchi Marta Kirish
```
1. Foydalanuvchi ro'yxatdan o'tadi
2. Birinchi marta login qiladi
3. ✅ Yangi qurilma email keladi
```

### Stsenariy 2: Bir Xil Qurilmadan Kirish
```
1. Foydalanuvchi har kuni bir xil kompyuterdan kiradi
2. ❌ Email kelmaydi (bir xil qurilma)
```

### Stsenariy 3: Yangi Brauzerdan Kirish
```
1. Foydalanuvchi Chrome o'rniga Firefox'dan kiradi
2. ✅ Yangi qurilma email keladi
```

### Stsenariy 4: Boshqa Kompyuterdan Kirish
```
1. Foydalanuvchi uydan o'rniga ishdan kiradi
2. ✅ Yangi qurilma email keladi (yangi IP)
```

### Stsenariy 5: Mobildan Kirish
```
1. Foydalanuvchi desktop o'rniga mobildan kiradi
2. ✅ Yangi qurilma email keladi
```

## 🔍 Qurilma Aniqlash Logikasi

Qurilma "yangi" hisoblanadi agar:
- IP manzil + User Agent kombinatsiyasi oxirgi 30 kun ichida ishlatilmagan bo'lsa

Qurilma "eski" hisoblanadi agar:
- Bir xil IP manzil va User Agent bilan oxirgi 30 kun ichida kirish bo'lgan bo'lsa

## 📊 Kirish Tarixi

Admin panelda barcha kirish tarixi ko'rinadi:
- Foydalanuvchi
- Qurilma turi
- Brauzer
- OS
- IP manzil
- Yangi qurilma (ha/yo'q)
- Kirish vaqti

## 🔒 Xavfsizlik

### Email'da:
- Kirish ma'lumotlari batafsil ko'rsatiladi
- "Parolni o'zgartirish" tugmasi
- Xavfsizlik maslahatlari
- Yordam uchun kontaktlar

### Database'da:
- Barcha kirish tarixi saqlanadi
- Shubhali faoliyatni aniqlash mumkin
- Admin monitoring

## 🧪 Test Qilish

### Manual Test

1. Birinchi marta login qiling
2. Email inbox'ni tekshiring
3. Boshqa brauzerdan login qiling
4. Yana email kelishini tekshiring

### Automated Test

```bash
python send_test_emails.py
```

Bu script yangi qurilma email'ni ham test qiladi.

## 🎨 Customization

### Email Yuborish Shartini O'zgartirish

`accounts/utils.py` da:
```python
# 30 kundan 60 kunga o'zgartirish
thirty_days_ago = timezone.now() - timezone.timedelta(days=60)
```

### Email Matnini O'zgartirish

`templates/emails/new_device_login.html` ni tahrirlang.

### Qurilma Aniqlash Logikasini O'zgartirish

`accounts/utils.py` da `is_new_device()` funksiyasini o'zgartiring.

## 💡 Kelajakdagi Yaxshilanishlar

1. **Geolocation**: IP'dan joylashuvni aniqlash (GeoIP2)
2. **Device Fingerprinting**: Aniqroq qurilma identifikatsiyasi
3. **Suspicious Activity Detection**: Shubhali faoliyatni avtomatik aniqlash
4. **Two-Factor Authentication**: Yangi qurilmadan 2FA talab qilish
5. **Device Management**: Foydalanuvchi o'z qurilmalarini boshqarishi
6. **Session Management**: Barcha sessiyalarni ko'rish va o'chirish
7. **Login Notifications**: Real-time push notification'lar

## 📈 Statistika

### Email Yuborilish Shartlari:
- ✅ Email mavjud
- ✅ Email tasdiqlangan
- ✅ Yangi qurilma (IP + User Agent)
- ✅ Oxirgi 30 kun ichida bunday kirish bo'lmagan

### Qurilma Turlari:
- Desktop (Windows, macOS, Linux)
- Mobile (Android, iOS)
- Tablet (iPad, Android Tablet)

### Brauzerlar:
- Google Chrome
- Mozilla Firefox
- Safari
- Microsoft Edge
- Opera

## 🛡️ Best Practices

1. **Email Verification**: Faqat tasdiqlangan email'larga yuborish
2. **Rate Limiting**: Bir xil email'ni ko'p marta yubormaslik
3. **Clear Instructions**: Aniq ko'rsatmalar berish
4. **Quick Action**: Tez harakat qilish imkoniyati
5. **Privacy**: Foydalanuvchi ma'lumotlarini himoya qilish

## 📞 Yordam

Muammolar bo'lsa:
- `EMAIL_FIX_GUIDE.md` ni o'qing
- `EMAIL_TEMPLATES_README.md` ni ko'ring
- `send_test_emails.py` ni ishga tushiring
- Admin panelda kirish tarixini tekshiring

## 🎓 Foydalanuvchi Uchun

Agar yangi qurilma email kelsa:

### Bu siz bo'lsa:
- Hech narsa qilishingiz shart emas
- Hisobingiz xavfsiz

### Bu siz bo'lmasa:
1. Darhol parolni o'zgartiring
2. Email'dagi "Parolni o'zgartirish" tugmasini bosing
3. Kuchli parol o'rnating
4. Agar yordam kerak bo'lsa, support@eduself.uz ga murojaat qiling

---

**Eslatma**: Bu xususiyat foydalanuvchi hisobining xavfsizligini oshirish uchun qo'shildi. Barcha kirish tarixi saqlanadi va admin panelda ko'rinadi.
