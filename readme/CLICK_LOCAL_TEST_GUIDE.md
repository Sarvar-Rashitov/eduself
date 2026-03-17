# Click To'lovni Local Muhitda Test Qilish

## Muammo
Click to'lov tizimi faqat **production muhitida** ishlaydi. Local test rejimida Click'ning o'z serverlari sizning local serveringizga (localhost:8000) kirish imkoniga ega emas.

## Yechimlar

### 1. Test Skriptdan Foydalanish (Tavsiya etiladi)
Local muhitda Click API'ni to'liq simulyatsiya qilish:

```bash
python test_click_payment.py
```

Bu skript:
- ✅ Payment yaratadi
- ✅ Click Prepare so'rovini simulyatsiya qiladi
- ✅ Click Complete so'rovini simulyatsiya qiladi
- ✅ Subscription yaratilishini tekshiradi
- ✅ Barcha xatolik ssenarilarini test qiladi

### 2. Ngrok yoki Localtunnel Ishlatish
Local serveringizni internetga ochish:

#### Ngrok bilan:
```bash
# 1. Ngrok o'rnating: https://ngrok.com/download
# 2. Django serverni ishga tushiring
python manage.py runserver

# 3. Boshqa terminalda ngrok ishga tushiring
ngrok http 8000

# 4. Ngrok URL'ini oling (masalan: https://abc123.ngrok.io)
# 5. Click merchant panelda callback URL'larni yangilang:
#    Prepare: https://abc123.ngrok.io/subscriptions/payment/click/prepare/
#    Complete: https://abc123.ngrok.io/subscriptions/payment/click/complete/
```

#### Localtunnel bilan:
```bash
# 1. Localtunnel o'rnating
npm install -g localtunnel

# 2. Django serverni ishga tushiring
python manage.py runserver

# 3. Boshqa terminalda localtunnel ishga tushiring
lt --port 8000

# 4. URL'ni oling va Click panelda sozlang
```

### 3. Production Serverda Test Qilish (Eng ishonchli)
Hozirgi production serveringizda test qilish:

1. **Production URL'lar allaqachon sozlangan:**
   - Prepare: https://eduself.uz/subscriptions/payment/click/prepare/
   - Complete: https://eduself.uz/subscriptions/payment/click/complete/

2. **Test to'lov qilish:**
   - Production saytga kiring: https://eduself.uz
   - EduSelf Pro'ga obuna bo'ling
   - Click to'lov tizimini tanlang
   - Test kartasi bilan to'lov qiling

3. **Click Test Kartasi:**
   ```
   Karta raqami: 8600 0000 0000 0000
   Amal qilish muddati: 03/99
   CVV: 123
   SMS kod: 666666
   ```

### 4. Click Merchant Panelda Sozlamalarni Tekshirish

1. **Kirish:** https://my.click.uz
2. **Merchant ID:** 57452
3. **Service ID:** 97245
4. **Callback URL'lar:**
   - Prepare URL: `https://eduself.uz/subscriptions/payment/click/prepare/`
   - Complete URL: `https://eduself.uz/subscriptions/payment/click/complete/`

5. **Test rejimi:** Click'da alohida test rejimi yo'q, lekin test kartasi bilan haqiqiy to'lovlarni test qilish mumkin.

## Hozirgi Holat

Rasmdan ko'rinib turibdiki:
- ✅ Payment yaratilgan (ID: 54)
- ✅ To'lov URL'i to'g'ri ishlayapti
- ⚠️ Local muhitda Click serverlar sizning localhost'ingizga kirish imkoniga ega emas

## Tavsiyalar

### Local Development uchun:
```bash
# Test skriptdan foydalaning
python test_click_payment.py
```

### Real Test uchun:
1. Production serverda test qiling: https://eduself.uz
2. Yoki ngrok/localtunnel ishlatib local serverni internetga oching

### Debug uchun:
```bash
# Payment holatini tekshirish
python check_payments.py

# Click konfiguratsiyasini tekshirish
python check_click_config.py
```

## Xulosa

Click to'lov tizimi to'g'ri sozlangan va production'da ishlaydi. Local muhitda test qilish uchun:
- **Eng oson:** `python test_click_payment.py` skriptidan foydalaning
- **Real test:** Production serverda (eduself.uz) test qiling
- **Advanced:** Ngrok/localtunnel bilan local serverni internetga oching

## Qo'shimcha Ma'lumot

- Click API dokumentatsiyasi: https://docs.click.uz/
- Click Merchant Panel: https://my.click.uz
- Test kartasi: 8600 0000 0000 0000 (SMS: 666666)
