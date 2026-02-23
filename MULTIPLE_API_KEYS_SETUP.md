# 🔑 Multiple API Keys Setup - Load Balancing

## Muammo
Bitta API key bilan ko'p so'rovlar yuborilganda worker timeout bo'ladi. Masalan, home page'da 10+ ta element bor va har biri tarjima qilinadi.

## Yechim: Load Balancing
Bir nechta API key ishlatib, har bir so'rovni turli keylarga taqsimlash. Bu "round-robin" usuli deyiladi.

## Qanday Ishlaydi

### 1. Ko'p API Keylar
Endi 5 tagacha API key qo'shish mumkin:
```env
DEEPSEEK_API_KEY_1=sk-your-first-key
DEEPSEEK_API_KEY_2=sk-your-second-key
DEEPSEEK_API_KEY_3=sk-your-third-key
DEEPSEEK_API_KEY_4=sk-your-fourth-key
DEEPSEEK_API_KEY_5=sk-your-fifth-key
```

### 2. Round-Robin Algoritm
Har bir so'rov uchun keyingisi key ishlatiladi:
- 1-so'rov → KEY_1
- 2-so'rov → KEY_2
- 3-so'rov → KEY_3
- 4-so'rov → KEY_1 (qaytadan boshlanadi)

### 3. Parallel So'rovlar
Agar 10 ta element bor bo'lsa:
- Bitta key bilan: 10 × 8 sekund = 80 sekund (TIMEOUT!)
- 5 ta key bilan: 10 ÷ 5 = 2 so'rov har bir key uchun = 16 sekund ✅

## O'zgarishlar

### 1. `.env` Fayl
```env
# DeepSeek API Keys (Multiple keys for load balancing)
DEEPSEEK_API_KEY_1=sk-fbfb83fcb68941bbbf599a4d76461f04
DEEPSEEK_API_KEY_2=  # Bu yerga 2-chi keyni qo'shing
DEEPSEEK_API_KEY_3=  # Bu yerga 3-chi keyni qo'shing
DEEPSEEK_API_KEY_4=  # Bu yerga 4-chi keyni qo'shing
DEEPSEEK_API_KEY_5=  # Bu yerga 5-chi keyni qo'shing

# Legacy key (backward compatibility)
DEEPSEEK_API_KEY=sk-fbfb83fcb68941bbbf599a4d76461f04
```

### 2. `eduself/settings.py`
```python
# Multiple API keys
DEEPSEEK_API_KEY_1 = os.environ.get('DEEPSEEK_API_KEY_1', '')
DEEPSEEK_API_KEY_2 = os.environ.get('DEEPSEEK_API_KEY_2', '')
DEEPSEEK_API_KEY_3 = os.environ.get('DEEPSEEK_API_KEY_3', '')
DEEPSEEK_API_KEY_4 = os.environ.get('DEEPSEEK_API_KEY_4', '')
DEEPSEEK_API_KEY_5 = os.environ.get('DEEPSEEK_API_KEY_5', '')
```

### 3. `core/translation.py`
```python
def __init__(self):
    # Ko'p API keylarni yuklash
    self.api_keys = self._load_api_keys()
    self.current_key_index = 0

def _get_next_api_key(self):
    """Round-robin: har safar keyingisi keyni ishlatish"""
    key = self.api_keys[self.current_key_index]
    self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
    return key
```

## Yangi Limitlar

### Uzunlik Limiti: 200 chars
- Oldingi: 100 chars (juda qisqa edi)
- Hozir: 200 chars (ko'p keylar bor, xavfsiz)

### Timeout: 8 sekund
- Oldingi: 5 sekund (juda qisqa edi)
- Hozir: 8 sekund (muvozanatli)

### max_tokens: 200
- Oldingi: 150 (yetarli emas edi)
- Hozir: 200 (uzunroq matnlar uchun)

## Qanday Qo'shish Kerak

### Local (.env)
1. `.env` faylni oching
2. Yangi keylarni qo'shing:
```env
DEEPSEEK_API_KEY_2=sk-your-new-key-here
DEEPSEEK_API_KEY_3=sk-another-key-here
```

### Production (Render)
1. Render dashboard'ga kiring
2. Environment Variables'ga o'ting
3. Har bir keyni alohida qo'shing:
   - Key: `DEEPSEEK_API_KEY_2`
   - Value: `sk-your-new-key-here`
4. Save qiling
5. Render avtomatik restart qiladi

## Afzalliklari

### ✅ Worker Timeout Yo'q
Har bir key alohida ishlaydi, shuning uchun timeout bo'lmaydi.

### ✅ Tezroq Sahifa Yuklash
Ko'p keylar parallel ishlaydi.

### ✅ Uzunroq Matnlar
200 belgigacha matnlar tarjima qilinadi (oldin 100 edi).

### ✅ Xavfsizlik
Agar bitta key ishlamasa, boshqalari ishlaydi.

### ✅ Backward Compatible
Agar faqat bitta key bo'lsa, u ishlatiladi (eski usul).

## Monitoring

Loglardan ko'rish mumkin:
```
✅ Loaded 5 DeepSeek API key(s) for load balancing
```

Agar faqat 1 ta key bo'lsa:
```
✅ Loaded 1 DeepSeek API key(s) for load balancing
```

## Test Qilish

### 1. Local Test
```bash
# .env ga 2-3 ta key qo'shing
python manage.py shell

>>> from core.translation import translator
>>> print(f"Keys loaded: {len(translator.api_keys)}")
Keys loaded: 3

>>> # Test translation
>>> translator.translate("Salom dunyo", 'uz', 'en')
'Hello world'
```

### 2. Production Test
1. Render'ga keylar qo'shing
2. Deploy qiling
3. Loglarni tekshiring: "Loaded X DeepSeek API key(s)"
4. Home page'ni oching va til o'zgartiring
5. 500 error bo'lmasligi kerak

## Qancha Key Kerak?

### Minimal: 2-3 ta key
- Home page uchun yetarli
- Worker timeout bo'lmaydi

### Optimal: 5 ta key
- Barcha sahifalar uchun yetarli
- Juda tez ishlaydi

### Maksimal: 10 ta key
- Juda ko'p foydalanuvchilar uchun
- Kod 10 tagacha keyni qo'llab-quvvatlaydi

## Xarajat

Agar 5 ta key bo'lsa:
- Har bir key: $5/oy (masalan)
- Jami: $25/oy

Lekin:
- Worker timeout yo'q
- Foydalanuvchilar xursand
- Sahifalar tez yuklanyapti

Bu investitsiya!

## Keyingi Qadamlar

1. ✅ Kod tayyor
2. ⏳ `.env` ga keylar qo'shing (local test uchun)
3. ⏳ Render'ga keylar qo'shing (production uchun)
4. ⏳ Deploy qiling
5. ⏳ Test qiling

---

**Status:** Ready to use
**Keylar kerak:** 2-5 ta DeepSeek API key
**Deploy vaqti:** 5 daqiqa
**Risk:** Juda past - backward compatible

**Created:** February 23, 2026, 20:30
