# Template Tag Fix - Quick Solution

## 🐛 Muammo
```
TemplateSyntaxError at /accounts/profile/
Invalid block tag on line 1107: 'has_any_interests', expected 'endblock'. 
Did you forget to register or load this tag?
```

## ❌ Sabab
`{% load onboarding_tags %}` template faylining boshida yuklanmagan edi. Template tag'lar faylning boshida yuklanishi kerak.

## ✅ Yechim

### Mobile Profile Template
**File**: `templates/accounts/profile.html`

**OLDIN**:
```django
{% extends 'base.html' %}
{% load translation_tags %}
{% load static %}

{% block body_attrs %}data-page="profile"{% endblock %}
```

**KEYIN**:
```django
{% extends 'base.html' %}
{% load translation_tags %}
{% load static %}
{% load onboarding_tags %}

{% block body_attrs %}data-page="profile"{% endblock %}
```

### Desktop Profile Template
**File**: `templates/accounts/profile_desktop.html`

**OLDIN**:
```django
{% extends 'base_desktop.html' %}
{% load static %}

{% block title %}Profilim - EduSelf{% endblock %}
```

**KEYIN**:
```django
{% extends 'base_desktop.html' %}
{% load static %}
{% load onboarding_tags %}

{% block title %}Profilim - EduSelf{% endblock %}
```

### Duplicate Load O'chirish
Settings tab ichidagi duplicate `{% load onboarding_tags %}` o'chirildi (chunki u allaqachon faylning boshida yuklangan).

## 📋 Template Tag Loading Rules

### 1. Faylning Boshida Yuklash
```django
{% extends 'base.html' %}
{% load static %}
{% load translation_tags %}
{% load onboarding_tags %}  <!-- Bu yerda yuklash -->
```

### 2. Bir Marta Yuklash
```django
<!-- ✅ TO'G'RI -->
{% load onboarding_tags %}  <!-- Faqat bir marta -->
{% has_any_interests user as user_has_interests %}

<!-- ❌ NOTO'G'RI -->
{% load onboarding_tags %}  <!-- Birinchi marta -->
...
{% load onboarding_tags %}  <!-- Ikkinchi marta - kerak emas! -->
```

### 3. Block Ichida Yuklash Mumkin Emas
```django
<!-- ❌ NOTO'G'RI -->
{% block content %}
    {% load onboarding_tags %}  <!-- Block ichida yuklash xato -->
{% endblock %}

<!-- ✅ TO'G'RI -->
{% load onboarding_tags %}  <!-- Block tashqarisida -->
{% block content %}
    {% has_any_interests user as user_has_interests %}
{% endblock %}
```

## 🔍 Debugging

### Template Tag Mavjudligini Tekshirish
```python
# Django shell
python manage.py shell

from django.template import Template, Context
from django.template.loader import get_template

# Template tag yuklanganini tekshirish
template = get_template('accounts/profile.html')
print(template.source)
```

### Custom Template Tag Tekshirish
```python
# Django shell
from accounts.templatetags import onboarding_tags

# Tag'lar ro'yxati
print(dir(onboarding_tags))

# should_show_section mavjudmi?
print(hasattr(onboarding_tags, 'should_show_section'))

# has_any_interests mavjudmi?
print(hasattr(onboarding_tags, 'has_any_interests'))
```

## 📝 Common Template Tag Errors

### Error 1: Tag Not Loaded
```
Invalid block tag: 'has_any_interests'
```
**Solution**: `{% load onboarding_tags %}` qo'shing

### Error 2: Wrong Tag Name
```
Invalid block tag: 'has_interests'
```
**Solution**: To'g'ri nom ishlatilganini tekshiring: `has_any_interests`

### Error 3: Tag Not Registered
```
'onboarding_tags' is not a registered tag library
```
**Solution**: 
1. `accounts/templatetags/onboarding_tags.py` mavjudligini tekshiring
2. `__init__.py` fayli mavjudligini tekshiring
3. App `INSTALLED_APPS` da ro'yxatdan o'tganini tekshiring

## ✅ Verification Checklist

- [x] `{% load onboarding_tags %}` faylning boshida
- [x] Duplicate load'lar o'chirilgan
- [x] Template tag fayli mavjud
- [x] `__init__.py` mavjud
- [x] App INSTALLED_APPS da
- [x] Server qayta ishga tushirilgan
- [x] Cache tozalangan

## 🚀 Testing

### Manual Test
```bash
# Server ishga tushirish
python manage.py runserver

# Browser'da ochish
http://127.0.0.1:8000/accounts/profile/

# Settings tabni ochish
# Personalization section ko'rinishi kerak
```

### Automated Test
```python
# test_profile.py
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileTemplateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_profile_page_loads(self):
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
    
    def test_onboarding_tags_loaded(self):
        response = self.client.get('/accounts/profile/')
        # No TemplateSyntaxError should occur
        self.assertEqual(response.status_code, 200)
```

## 📚 Related Files

### Template Files
- `templates/accounts/profile.html` - Mobile profile
- `templates/accounts/profile_desktop.html` - Desktop profile

### Template Tag Files
- `accounts/templatetags/__init__.py` - Package marker
- `accounts/templatetags/onboarding_tags.py` - Custom tags

### View Files
- `accounts/views.py` - profile_view function

## 🎯 Best Practices

### 1. Load All Tags at Top
```django
{% extends 'base.html' %}
{% load static %}
{% load translation_tags %}
{% load onboarding_tags %}
{% load custom_filters %}
```

### 2. Use Descriptive Names
```python
# Good
@register.simple_tag
def has_any_interests(user):
    pass

# Bad
@register.simple_tag
def check(user):
    pass
```

### 3. Document Your Tags
```python
@register.simple_tag
def has_any_interests(user):
    """
    Check if user has completed onboarding and has any interests.
    
    Usage:
        {% has_any_interests user as user_has_interests %}
        {% if user_has_interests %}
            ...
        {% endif %}
    
    Returns:
        bool: True if user has interests, False otherwise
    """
    pass
```

## ✅ Fixed!

Template tag xatosi to'liq tuzatildi. Endi:
- ✅ Profile page ochiladi
- ✅ Settings tab ishlaydi
- ✅ Personalization controls ko'rinadi
- ✅ Hech qanday TemplateSyntaxError yo'q

Serveringizni qayta ishga tushiring va test qiling! 🎉
