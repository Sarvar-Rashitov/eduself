# 📊 Haqiqiy Son (Float) Ball Tizimi - Qo'llanma

## ✅ Nima O'zgartirildi?

Savollarga ball berish tizimi **butun sondan** (integer) **haqiqiy songa** (float) o'zgartirildi.

### Oldingi Tizim (Integer)
```python
points = models.PositiveIntegerField(default=1)
# Faqat: 1, 2, 3, 4, 5 ball
```

### Yangi Tizim (Float)
```python
points = models.FloatField(default=1.0)
# Endi: 1.0, 1.5, 2.1, 2.5, 3.3, 4.7 ball
```

## 🎯 Qaysi Modellar O'zgartirildi?

1. **Question** - Oddiy test savollari
2. **CertificateQuestion** - Sertifikat test savollari
3. **MockExamQuestion** - Mock imtihon savollari

## 📝 Qanday Ishlatish?

### Admin Panelda

1. **Savol Qo'shish**
   - Admin panelga kiring: `/nokia/`
   - "Questions" (Savollar) bo'limiga o'ting
   - Yangi savol qo'shing
   - "Ball" maydoniga haqiqiy son kiriting

2. **Ball Misollar**
   ```
   ✅ 1.0   - Oson savol
   ✅ 1.5   - O'rtacha oson
   ✅ 2.0   - O'rtacha
   ✅ 2.1   - O'rtacha qiyin
   ✅ 2.5   - Qiyin
   ✅ 3.0   - Juda qiyin
   ✅ 3.3   - Murakkab
   ✅ 4.5   - Juda murakkab
   ✅ 5.0   - Eng qiyin
   ```

3. **Mavjud Savollarni Tahrirlash**
   - Savolni tanlang
   - "Ball" maydonini o'zgartiring
   - Saqlang

### Kod Orqali

```python
from core.models import Question, Test

# Yangi savol yaratish
question = Question.objects.create(
    test=test,
    text="Bu qanday savol?",
    points=2.5  # Haqiqiy son
)

# Mavjud savolni yangilash
question = Question.objects.get(id=1)
question.points = 3.3
question.save()
```

## 🔢 Ball Hisoblash

### Test Natijasi

Endi test natijalari ham haqiqiy son ko'rinishida:

```python
# Misol: 5 ta savol
# Savol 1: 2.1 ball (to'g'ri)
# Savol 2: 1.5 ball (noto'g'ri)
# Savol 3: 3.0 ball (to'g'ri)
# Savol 4: 2.5 ball (to'g'ri)
# Savol 5: 1.9 ball (noto'g'ri)

# Jami ball: 2.1 + 3.0 + 2.5 = 7.6 ball
# Maksimal ball: 2.1 + 1.5 + 3.0 + 2.5 + 1.9 = 11.0 ball
# Foiz: (7.6 / 11.0) * 100 = 69.09%
```

### Admin Panelda Ko'rinish

Test natijalarida:
- **Earned Points**: 7.6 (olingan ball)
- **Score**: 69.09% (foiz)
- **Correct Answers**: 3 (to'g'ri javoblar soni)
- **Total Questions**: 5 (jami savollar)

## 📊 Misollar

### Misol 1: Matematika Testi

```
Savol 1: "2 + 2 = ?"           → 1.0 ball (oson)
Savol 2: "5 × 7 = ?"           → 1.5 ball (o'rtacha)
Savol 3: "√144 = ?"            → 2.0 ball (qiyin)
Savol 4: "∫x² dx = ?"          → 3.5 ball (juda qiyin)
Savol 5: "lim(x→0) sin(x)/x = ?" → 4.0 ball (eng qiyin)

Jami: 12.0 ball
```

### Misol 2: Ingliz Tili Testi

```
Savol 1: "I ___ a student"     → 1.0 ball (oson)
Savol 2: "Present Perfect"     → 2.1 ball (o'rtacha)
Savol 3: "Passive Voice"       → 2.5 ball (qiyin)
Savol 4: "Conditional III"     → 3.3 ball (juda qiyin)
Savol 5: "Subjunctive Mood"    → 4.1 ball (eng qiyin)

Jami: 13.0 ball
```

## 🎓 Ball Berish Tavsiyalari

### Qiyinlik Darajasi Bo'yicha

| Daraja | Ball Oralig'i | Tavsif |
|--------|--------------|--------|
| Juda Oson | 0.5 - 1.0 | Asosiy bilim |
| Oson | 1.1 - 1.5 | Oddiy tushuncha |
| O'rtacha | 1.6 - 2.5 | O'rtacha bilim |
| Qiyin | 2.6 - 3.5 | Chuqur bilim |
| Juda Qiyin | 3.6 - 5.0 | Murakkab masala |

### Savol Turi Bo'yicha

| Turi | Ball | Sabab |
|------|------|-------|
| Ko'p tanlov (4 variant) | 1.0 - 2.0 | Taxmin qilish mumkin |
| To'g'ri/Noto'g'ri | 0.5 - 1.0 | 50% ehtimollik |
| Qisqa javob | 2.0 - 3.0 | Bilish kerak |
| Hisoblash | 2.5 - 4.0 | Qo'llash kerak |
| Tahlil | 3.0 - 5.0 | Chuqur tushunish |

## 🔧 Texnik Ma'lumotlar

### Database O'zgarishi

```sql
-- Oldingi
points INTEGER NOT NULL DEFAULT 1

-- Yangi
points REAL NOT NULL DEFAULT 1.0
```

### Migration

```bash
# Migration yaratildi
python manage.py makemigrations core
# Output: 0024_alter_certificatequestion_points_and_more.py

# Migration qo'llandi
python manage.py migrate core
# Output: Applying core.0024... OK
```

### Model O'zgarishi

```python
# Oldingi
class Question(models.Model):
    points = models.PositiveIntegerField(default=1, verbose_name="Ball")

# Yangi
class Question(models.Model):
    points = models.FloatField(default=1.0, verbose_name="Ball")
```

## ⚠️ Muhim Eslatmalar

1. **Mavjud Ma'lumotlar**
   - Barcha mavjud savollar avtomatik 1.0, 2.0, 3.0 ga aylanadi
   - Hech qanday ma'lumot yo'qolmaydi

2. **Admin Panelda**
   - Ball maydoniga faqat raqam kiriting
   - Vergul (,) emas, nuqta (.) ishlating
   - Misol: 2.5 ✅, 2,5 ❌

3. **Foiz Hisoblash**
   - Foiz avtomatik hisoblanadi
   - Haqiqiy son ko'rinishida: 85.67%

4. **Rounding (Yaxlitlash)**
   - Ball: 2 xona (2.15)
   - Foiz: 2 xona (85.67%)

## 📱 Frontend Ko'rinish

Test natijalarida:

```
╔════════════════════════════════════╗
║  Test Natijasi                     ║
╠════════════════════════════════════╣
║  Olingan ball: 7.6 / 11.0         ║
║  Foiz: 69.09%                      ║
║  To'g'ri javoblar: 3 / 5          ║
║  Holat: ❌ O'tmadi (60% kerak)    ║
╚════════════════════════════════════╝
```

## 🎯 Foydalanish Stsenariylari

### Ssenariy 1: Oddiy Test
```
5 ta savol, har biri 1.0 ball
Jami: 5.0 ball
O'tish: 60% (3.0 ball)
```

### Ssenariy 2: Aralash Test
```
3 ta oson savol: 1.0 ball (jami 3.0)
2 ta qiyin savol: 2.5 ball (jami 5.0)
Jami: 8.0 ball
O'tish: 60% (4.8 ball)
```

### Ssenariy 3: Murakkab Test
```
2 ta oson: 1.0 ball (2.0)
3 ta o'rtacha: 2.0 ball (6.0)
2 ta qiyin: 3.0 ball (6.0)
1 ta juda qiyin: 5.0 ball (5.0)
Jami: 19.0 ball
O'tish: 70% (13.3 ball)
```

## 🤝 Yordam

Savollar bo'lsa:
- Email: support@eduself.uz
- Telegram: @eduself_uz

---

**Yaratilgan**: 2024-12-17
**Versiya**: 1.0
**Status**: ✅ Ishga Tayyor!
