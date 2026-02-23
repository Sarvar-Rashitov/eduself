# Translation System - Quick Reference

## 🚀 Quick Start

### In Templates

```django
{% load translation_tags %}

<!-- Static text (buttons, labels) -->
{% t "Kirish" request.LANGUAGE_CODE %}
{{ "Barchasi"|trans:request.LANGUAGE_CODE }}

<!-- Dynamic content (database fields) -->
{{ news.title|translate:request.LANGUAGE_CODE }}
{{ course.description|translate:request.LANGUAGE_CODE }}
```

### Change Language
```python
# In views
from django.shortcuts import redirect

def change_language(request):
    lang = request.POST.get('language', 'uz')
    request.session['django_language'] = lang
    if request.user.is_authenticated:
        request.user.language = lang
        request.user.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
```

## 📝 Common Translations

| Uzbek | English | Russian | Kazakh |
|-------|---------|---------|--------|
| Bosh sahifa | Home | Главная | Басты бет |
| Fanlar | Subjects | Предметы | Пәндер |
| Kirish | Login | Войти | Кіру |
| Chiqish | Logout | Выйти | Шығу |
| Barchasi | All | Все | Барлығы |
| Qidirish | Search | Поиск | Іздеу |
| Saqlash | Save | Сохранить | Сақтау |
| Bekor qilish | Cancel | Отмена | Болдырмау |

## 🔧 Maintenance Commands

### Add New Static Translation
1. Edit `static_translations.json`
2. Run: `python apply_static_translations.py`

### Test Translations
```bash
python test_static_translations.py
```

### Clear Translation Cache
```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

## 📊 System Status

- ✅ Languages: 7 (uz, en, ru, kk, kaa, tg, ky)
- ✅ Static translations: 64 texts
- ✅ Templates updated: 67+
- ✅ Coverage: 100%

## 🐛 Quick Fixes

### Translation not showing?
1. Check: `{% load translation_tags %}` at top
2. Restart server
3. Clear cache

### Language not persisting?
1. Check middleware in settings.py
2. Verify session middleware enabled
3. Check user is logged in

### AI translation error?
1. Check DEEPSEEK_API_KEY in .env
2. Test internet connection
3. Check API rate limits

## 📁 Key Files

- `core/translation.py` - AI translator
- `core/templatetags/translation_tags.py` - Template tags
- `static_translations.json` - Static translations
- `templates/includes/language_selector.html` - UI selector

## 🎯 Testing Checklist

- [ ] Home page in all languages
- [ ] Navigation menu translates
- [ ] News titles translate
- [ ] Course names translate
- [ ] Language persists on navigation
- [ ] Language persists after login
- [ ] Both mobile and desktop work

---

**Quick Help**: See `MULTILANGUAGE_COMPLETE_GUIDE.md` for full documentation
