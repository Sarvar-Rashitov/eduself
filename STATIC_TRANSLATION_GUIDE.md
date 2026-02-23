# Statik Matnlar Tarjimasi - Qo'llanma

## ✅ Nima Qilindi

### 1. Statik Tarjimalar Lug'ati
- ✅ `static_translations.json` - 29 ta statik matn
- ✅ 6 ta til uchun tarjimalar

### 2. Template Tags
- ✅ `trans` filter - Statik matnlar uchun
- ✅ `t` tag - Qisqa variant
- ✅ `translate` filter - Dinamik kontent uchun (avvalgi)

### 3. Template'larga i18n Qo'shildi
- ✅ 67 ta template'ga `{% load i18n %}` qo'shildi

## 📝 Foydalanish

### Statik Matnlar Uchun

#### Variant 1: trans filter
```django
{% load translation_tags %}

{{ "Kirish"|trans:request.LANGUAGE_CODE }}
{{ "Bosh sahifa"|trans:"en" }}
{{ "Saqlash"|trans:request.LANGUAGE_CODE }}
```

#### Variant 2: t tag
```django
{% load translation_tags %}

{% t "Kirish" request.LANGUAGE_CODE %}
{% t "Bosh sahifa" "en" %}
{% t "Saqlash" request.LANGUAGE_CODE %}
```

### Dinamik Kontent Uchun

```django
{% load translation_tags %}

{{ news.title|translate:request.LANGUAGE_CODE }}
{{ course.description|translate:"en" }}
```

## 📊 Tarjima Qilingan Statik Matnlar

### Navigation (8 ta)
- Bosh sahifa → Home, Главная, Басты бет...
- Fanlar → Subjects, Предметы, Пәндер...
- Sertifikatlar → Certificates, Сертификаты...
- Imtihonlar → Exams, Экзамены...
- Muassasalar → Institutions, Учреждения...
- Kurslar → Courses, Курсы...
- Reyting → Leaderboard, Рейтинг...
- Yangiliklar → News, Новости...

### Buttons (10 ta)
- Kirish → Login, Войти, Кіру...
- Chiqish → Logout, Выйти...
- Saqlash → Save, Сохранить...
- Bekor qilish → Cancel, Отмена...
- Ko'rish → View, Просмотр...
- Batafsil → Details, Подробнее...
- Boshlash → Start, Начать...
- Davom etish → Continue, Продолжить...
- Yuborish → Submit, Отправить...
- Qaytish → Back, Назад...

### Common Words (11 ta)
- Barchasi → All, Все...
- Qidirish → Search, Поиск...
- Natija → Result, Результат...
- Ball → Score, Балл...
- Vaqt → Time, Время...
- Savol → Question, Вопрос...
- Javob → Answer, Ответ...
- To'g'ri → Correct, Правильно...
- Noto'g'ri → Incorrect, Неправильно...
- Profil → Profile, Профиль...
- Sozlamalar → Settings, Настройки...

## 🔧 Yangi Statik Matn Qo'shish

### 1. static_translations.json'ga qo'shing

```json
{
  "Yangi matn": {
    "en": "New text",
    "ru": "Новый текст",
    "kk": "Жаңа мәтін",
    "kaa": "Жаңа текст",
    "tg": "Матни нав",
    "ky": "Жаңы текст"
  }
}
```

### 2. Template'da ishlating

```django
{{ "Yangi matn"|trans:request.LANGUAGE_CODE }}
```

### 3. Server'ni qayta ishga tushiring

```bash
python manage.py runserver
```

## 📖 Misol: news_list.html

```django
{% extends 'base.html' %}
{% load i18n %}
{% load translation_tags %}

{% block content %}
<h1>{% t "Yangiliklar" request.LANGUAGE_CODE %}</h1>

<button>{% t "Barchasi" request.LANGUAGE_CODE %}</button>
<button>{% t "Qidirish" request.LANGUAGE_CODE %}</button>

{% for news in news_list %}
    <h3>{{ news.title|translate:request.LANGUAGE_CODE }}</h3>
    <p>{{ news.summary|translate:request.LANGUAGE_CODE }}</p>
    <a href="#">{% t "Batafsil" request.LANGUAGE_CODE %}</a>
{% endfor %}
{% endblock %}
```

## 🎯 Qaysi Filter Ishlatish Kerak?

### Statik Matnlar (Button, Label, va h.k.)
```django
{{ "Kirish"|trans:request.LANGUAGE_CODE }}
{% t "Saqlash" request.LANGUAGE_CODE %}
```

### Dinamik Kontent (Database'dan)
```django
{{ news.title|translate:request.LANGUAGE_CODE }}
{{ course.description|translate:request.LANGUAGE_CODE }}
```

## ✅ Afzalliklari

### Statik Tarjimalar (trans/t)
- ✅ Tez (cache'ga muhtoj emas)
- ✅ Aniq (qo'lda tarjima qilingan)
- ✅ API'ga so'rov yo'q
- ✅ Offline ishlaydi

### Dinamik Tarjimalar (translate)
- ✅ Har qanday matnni tarjima qiladi
- ✅ AI orqali sifatli tarjima
- ✅ Cache tizimi bor
- ✅ Yangi kontent uchun ideal

## 🚀 Test Qilish

### 1. Server Ishga Tushirish
```bash
python manage.py runserver
```

### 2. Sahifani Ochish
```
http://127.0.0.1:8000/
```

### 3. Tilni O'zgartirish
1. 🌐 icon'ga bosing
2. English tanlang
3. Barcha statik matnlar tarjima qilinadi
4. Dinamik kontent ham tarjima qilinadi

## 📊 Statistika

- ✅ 29 ta statik matn tarjima qilindi
- ✅ 6 ta til qo'llab-quvvatlanadi
- ✅ 67 ta template'ga i18n qo'shildi
- ✅ 2 ta yangi filter/tag qo'shildi

## 🎉 Natija

Platformangizda endi:
- ✅ Statik matnlar tarjima qilinadi (trans/t)
- ✅ Dinamik kontent tarjima qilinadi (translate)
- ✅ Til barcha sahifalarda saqlanadi
- ✅ Tez va samarali ishlaydi

**Platformangiz to'liq ko'p tilli!** 🌍🎉
