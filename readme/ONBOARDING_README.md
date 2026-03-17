# 🎯 EduSelf Onboarding System

> A lightweight personalization system for new users

## Quick Start (3 Steps)

### 1. Add Middleware

`eduself/settings.py`:
```python
MIDDLEWARE = [
    # ... existing ...
    'accounts.onboarding_middleware.OnboardingMiddleware',
]
```

### 2. Add Context Processor

`eduself/settings.py`:
```python
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            # ... existing ...
            'accounts.onboarding_context.user_preferences',
        ],
    },
}]
```

### 3. Update Home Template

`templates/core/home_desktop.html`:
```django
{% load onboarding_tags %}

{% include 'accounts/onboarding_banner.html' %}

{% should_show_section user 'subjects' as show_subjects %}
{% if show_subjects %}
    <!-- Subjects section -->
{% endif %}
```

## What It Does

- Shows 5 questions to new users
- Personalizes home page based on answers
- Never fully restricts platform
- Beautiful, modern UI

## Documentation

- **ONBOARDING_QUICK_START.md** - Quick overview
- **IMPLEMENTATION_CHECKLIST.md** - Step-by-step guide
- **ONBOARDING_SYSTEM_GUIDE.md** - Complete reference
- **ONBOARDING_INTEGRATION_EXAMPLE.md** - Code examples
- **ONBOARDING_SYSTEM_ARCHITECTURE.md** - Technical details
- **ONBOARDING_SUMMARY.md** - Complete summary

## Test It

1. Register new account
2. Should redirect to `/accounts/onboarding/`
3. Answer 5 questions
4. Home page shows only selected sections

## Features

✅ 5-question onboarding flow
✅ Dynamic category loading
✅ Smart section filtering
✅ "Show All Platform" button
✅ One-time experience
✅ Beautiful UI
✅ Mobile responsive
✅ Admin panel integration

## Files Created

- `accounts/onboarding_models.py`
- `accounts/onboarding_views.py`
- `accounts/onboarding_middleware.py`
- `accounts/onboarding_context.py`
- `accounts/templatetags/onboarding_tags.py`
- `templates/accounts/onboarding.html`
- `templates/accounts/onboarding_banner.html`

## Database

Model: `UserInterestPreference`
- Migration: `0020_userinterestpreference` (already applied)

## URLs

- `/accounts/onboarding/` - Main page
- `/accounts/onboarding/save/` - Save preferences
- `/accounts/onboarding/skip/` - Skip onboarding
- `/accounts/onboarding/show-all/` - Show all platform
- `/accounts/onboarding/reset/` - Reset onboarding

## Admin

Access: `/admin/accounts/userinterestpreference/`

## Support

Check documentation files for detailed help.

---

**Setup Time**: 15-30 minutes
**Difficulty**: Easy
**Impact**: High

🚀 Ready to personalize your platform!
