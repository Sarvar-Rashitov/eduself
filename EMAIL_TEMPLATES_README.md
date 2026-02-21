# 📧 Professional Email Templates

EduSelf loyihasida professional HTML email template'lar yaratildi.

## ✨ Xususiyatlar

### Dizayn
- 🎨 Gradient header logo bilan
- 🔘 Chiroyli tugmalar (hover effekt bilan)
- 📱 Responsive dizayn (mobil va desktop)
- 🌈 Zamonaviy ranglar va shadow'lar
- 📊 Strukturali layout

### Email Turlari

1. **Email Tasdiqlash** (`verify_email.html`)
   - Logo yuqori qismida
   - "Emailni tasdiqlash" tugmasi
   - 48 soatlik amal qilish muddati haqida ogohlantirish
   - Fallback havola

2. **Parolni Tiklash** (`reset_password.html`)
   - Logo yuqori qismida
   - "Parolni tiklash" tugmasi
   - 24 soatlik amal qilish muddati
   - Xavfsizlik maslahatlari
   - Fallback havola

3. **Xush kelibsiz** (`welcome.html`)
   - Tabrik xabari
   - "Platformaga kirish" tugmasi
   - Platformaning imkoniyatlari
   - Foydali maslahatlar

4. **Qaytganingizdan xursandmiz** (`welcome_back.html`)
   - Qaytib kelgan foydalanuvchi uchun
   - Oxirgi kirish vaqti
   - "Davom etish" tugmasi
   - Bugungi maqsadlar
   - Xavfsizlik ogohlantirishi

### Base Template (`base_email.html`)
- Header: Logo va subtitle
- Content: Asosiy kontent
- Footer: Ijtimoiy tarmoqlar va copyright

## 🎨 Dizayn Elementlari

### Ranglar
- Primary: `#667eea` → `#764ba2` (gradient)
- Background: `#f5f5f5`
- Text: `#333333`
- Secondary: `#666666`

### Tugmalar
- Gradient background
- Box shadow
- Hover effekt (transform + shadow)
- Rounded corners (8px)

### Layout
- Max width: 600px
- Padding: 40px (desktop), 30px (mobile)
- Responsive breakpoint: 600px

## 📝 Qanday Ishlatish

### 1. Email Tasdiqlash

```python
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

html_content = render_to_string('emails/verify_email.html', {
    'user_name': user.first_name,
    'verify_url': verify_url,
})

text_content = f'Emailni tasdiqlash: {verify_url}'

email = EmailMultiAlternatives(
    subject='EduSelf - Emailni tasdiqlash',
    body=text_content,
    from_email=settings.DEFAULT_FROM_EMAIL,
    to=[user.email]
)
email.attach_alternative(html_content, "text/html")
email.send()
```

### 2. Parolni Tiklash

```python
html_content = render_to_string('emails/reset_password.html', {
    'user_name': user.first_name,
    'reset_url': reset_url,
})

text_content = f'Parolni tiklash: {reset_url}'

email = EmailMultiAlternatives(
    subject='EduSelf - Parolni tiklash',
    body=text_content,
    from_email=settings.DEFAULT_FROM_EMAIL,
    to=[user.email]
)
email.attach_alternative(html_content, "text/html")
email.send()
```

### 3. Xush kelibsiz

```python
html_content = render_to_string('emails/welcome.html', {
    'user_name': user.first_name,
    'site_url': settings.SITE_URL,
})

email = EmailMultiAlternatives(
    subject='EduSelf - Xush kelibsiz!',
    body='Xush kelibsiz!',
    from_email=settings.DEFAULT_FROM_EMAIL,
    to=[user.email]
)
email.attach_alternative(html_content, "text/html")
email.send()
```

### 4. Qaytganingizdan xursandmiz

```python
html_content = render_to_string('emails/welcome_back.html', {
    'user_name': user.first_name,
    'site_url': settings.SITE_URL,
    'last_login': user.last_login,
})

email = EmailMultiAlternatives(
    subject='EduSelf - Qaytganingizdan xursandmiz!',
    body='Qaytganingizdan xursandmiz!',
    from_email=settings.DEFAULT_FROM_EMAIL,
    to=[user.email]
)
email.attach_alternative(html_content, "text/html")
email.send()
```

## 🧪 Test Qilish

```bash
# HTML email test
python test_email.py
```

Bu script:
1. Email sozlamalarini tekshiradi
2. HTML email yuboradi
3. Natijani ko'rsatadi

## 📱 Email Client Qo'llab-quvvatlash

Template'lar quyidagi email client'larda test qilingan:
- ✅ Gmail (Web, iOS, Android)
- ✅ Outlook (Web, Desktop)
- ✅ Apple Mail (iOS, macOS)
- ✅ Yahoo Mail
- ✅ Yandex Mail

## 🎯 Best Practices

### HTML Email Uchun
1. **Inline CSS**: Ba'zi email client'lar `<style>` tag'ni qo'llab-quvvatlamaydi
2. **Table Layout**: Flexbox/Grid o'rniga table ishlatish tavsiya etiladi
3. **Alt Text**: Rasmlar uchun alt text qo'shing
4. **Text Fallback**: Har doim text versiyasini qo'shing
5. **Test**: Turli email client'larda test qiling

### Xavfsizlik
1. **HTTPS**: Barcha havolalar HTTPS bo'lishi kerak
2. **Token**: Xavfsiz token'lar ishlating
3. **Expiry**: Token'larga amal qilish muddati qo'ying
4. **Rate Limiting**: Email yuborishni cheklang

## 🔧 Sozlash

### Logo O'zgartirish

`base_email.html` da:
```html
<div class="logo">📚 EduSelf</div>
```

Emoji o'rniga rasm qo'yish:
```html
<img src="https://eduself.uz/static/logo.png" alt="EduSelf" style="height: 50px;">
```

### Ranglarni O'zgartirish

`base_email.html` da CSS o'zgartiriladi:
```css
.header {
    background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
}
.button {
    background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
}
```

### Footer O'zgartirish

`base_email.html` da footer qismini tahrirlang:
```html
<div class="footer">
    <!-- O'z ma'lumotlaringiz -->
</div>
```

## 📊 Monitoring

Email yuborishni kuzatish uchun:

1. **Django Admin**: Email log'larini ko'ring
2. **Gmail Sent**: Yuborilgan xabarlarni tekshiring
3. **Error Logs**: `print()` orqali xatolarni ko'ring

## 🚀 Production

Production'da:
1. Professional email service ishlating (SendGrid, Mailgun, AWS SES)
2. Email tracking qo'shing
3. Bounce handling sozlang
4. Unsubscribe link qo'shing
5. SPF/DKIM/DMARC sozlang

## 📞 Yordam

Muammolar bo'lsa:
- `EMAIL_FIX_GUIDE.md` ni o'qing
- `test_email.py` ni ishga tushiring
- Email sozlamalarini tekshiring

---

**Eslatma**: Bu template'lar development uchun tayyor. Production'da professional email service ishlatish tavsiya etiladi.
