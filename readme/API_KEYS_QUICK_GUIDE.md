# 🚀 API Keys - Tezkor Qo'llanma

## Nima Qildik?
Bir nechta DeepSeek API key ishlatish imkoniyatini qo'shdik. Bu worker timeout muammosini hal qiladi.

## Qanday Ishlaydi?
Har bir tarjima so'rovi uchun turli API key ishlatiladi (round-robin):
- 1-so'rov → KEY_1
- 2-so'rov → KEY_2  
- 3-so'rov → KEY_3
- 4-so'rov → KEY_1 (qaytadan)

## Nima Qo'shish Kerak?

### Local (.env)
```env
DEEPSEEK_API_KEY_1=sk-fbfb83fcb68941bbbf599a4d76461f04
DEEPSEEK_API_KEY_2=sk-your-second-key-here
DEEPSEEK_API_KEY_3=sk-your-third-key-here
DEEPSEEK_API_KEY_4=sk-your-fourth-key-here
DEEPSEEK_API_KEY_5=sk-your-fifth-key-here
```

### Production (Render)
Render dashboard → Environment Variables:
```
DEEPSEEK_API_KEY_1 = sk-first-key
DEEPSEEK_API_KEY_2 = sk-second-key
DEEPSEEK_API_KEY_3 = sk-third-key
DEEPSEEK_API_KEY_4 = sk-fourth-key
DEEPSEEK_API_KEY_5 = sk-fifth-key
```

## Yangi Limitlar
- ✅ Uzunlik: 200 chars (oldin 100 edi)
- ✅ Timeout: 8 sekund (oldin 5 edi)
- ✅ max_tokens: 200 (oldin 150 edi)

## Natija
- ✅ Worker timeout yo'q
- ✅ Barcha matnlar tarjima qilinadi (200 belgigacha)
- ✅ Tez sahifa yuklash
- ✅ Xavfsiz va barqaror

## Deploy
```bash
git add .
git commit -m "feat: Multiple API keys support for load balancing"
git push origin main
```

Render avtomatik deploy qiladi. Keyin Render'ga keylarni qo'shing!

---
**Minimal:** 2-3 ta key yetarli  
**Optimal:** 5 ta key tavsiya etiladi
