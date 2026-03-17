# ⚡ Tezkor Sozlash - Page-Based Load Balancing

## 1️⃣ API Keylarni Qo'shing

### Local (.env):
```env
DEEPSEEK_API_KEY_1=sk-fbfb83fcb68941bbbf599a4d76461f04
DEEPSEEK_API_KEY_2=sk-your-second-key-here
DEEPSEEK_API_KEY_3=sk-your-third-key-here
DEEPSEEK_API_KEY_4=sk-your-fourth-key-here
DEEPSEEK_API_KEY_5=sk-your-fifth-key-here
```

### Production (Render):
```
DEEPSEEK_API_KEY_1 = sk-first-key
DEEPSEEK_API_KEY_2 = sk-second-key
DEEPSEEK_API_KEY_3 = sk-third-key
DEEPSEEK_API_KEY_4 = sk-fourth-key
DEEPSEEK_API_KEY_5 = sk-fifth-key
```

## 2️⃣ Deploy Qiling

```bash
git add .
git commit -m "feat: Page-based load balancing"
git push origin main
```

## 3️⃣ Render'ga Keylarni Qo'shing

1. Render dashboard → Environment Variables
2. Har bir keyni alohida qo'shing
3. Save → Render avtomatik restart qiladi

## 4️⃣ Test Qiling

1. Home page → KEY_1 ishlatadi
2. Institutions → KEY_2 ishlatadi
3. Courses → KEY_3 ishlatadi
4. Mock Exams → KEY_4 ishlatadi
5. Profile → KEY_5 ishlatadi

## ✅ Natija

- Worker timeout yo'q
- Barcha matnlar tarjima qilinadi (200 chars gacha)
- Har sahifa o'z keyidan foydalanadi
- Tez va barqaror!

---

**Minimal:** 2-3 ta key yetarli  
**Optimal:** 5 ta key tavsiya etiladi  
**Maksimal:** 10 tagacha qo'shish mumkin
