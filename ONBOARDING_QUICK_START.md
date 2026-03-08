# Onboarding System - Quick Start

## ✅ What's Been Created

### 1. Models
- `accounts/onboarding_models.py` - UserInterestPreference model
- Stores user role and selected categories (subjects, certificates, courses, mock_exams)

### 2. Views
- `accounts/onboarding_views.py`
  - `onboarding_view()` - Shows 5-question onboarding page
  - `save_onboarding()` - Saves user preferences
  - `skip_onboarding()` - Skip onboarding
  - `show_all_platform()` - Disable personalization
  - `reset_onboarding()` - Reset and start over

### 3. URLs
- `/accounts/onboarding/` - Main onboarding page
- `/accounts/onboarding/save/` - Save preferences (POST)
- `/accounts/onboarding/skip/` - Skip onboarding (POST)
- `/accounts/onboarding/show-all/` - Show all platform
- `/accounts/onboarding/reset/` - Reset onboarding

### 4. Templates
- `templates/accounts/onboarding.html` - Beautiful 5-question onboarding UI
- `templates/accounts/onboarding_banner.html` - Personalization banner

### 5. Middleware
- `accounts/onboarding_middleware.py` - Auto-redirects new users to onboarding

### 6. Template Tags
- `accounts/templatetags/onboarding_tags.py`
  - `{% should_show_section user 'subjects' %}` - Check if section should show
  - `{{ user|has_any_interests }}` - Check if user has interests

### 7. Context Processor
- `accounts/onboarding_context.py` - Makes preferences available in templates

### 8. Admin
- Admin panel integration for managing user preferences

### 9. Documentation
- `ONBOARDING_SYSTEM_GUIDE.md` - Complete system documentation
- `ONBOARDING_INTEGRATION_EXAMPLE.md` - Step-by-step integration guide
- `ONBOARDING_QUICK_START.md` - This file

## 🚀 Quick Setup (3 Steps)

### Step 1: Add Middleware

Edit `eduself/settings.py`:

```python
MIDDLEWARE = [
    # ... existing middleware ...
    'accounts.onboarding_middleware.OnboardingMiddleware',  # ADD THIS
]
```

### Step 2: Add Context Processor (Optional)

Edit `eduself/settings.py`:

```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... existing processors ...
                'accounts.onboarding_context.user_preferences',  # ADD THIS
            ],
        },
    },
]
```

### Step 3: Update Home Template

Edit `templates/core/home_desktop.html`:

```django
{% load onboarding_tags %}  <!-- Add at top -->

<!-- Add banner after hero section -->
{% include 'accounts/onboarding_banner.html' %}

<!-- Wrap sections with checks -->
{% should_show_section user 'subjects' as show_subjects %}
{% if show_subjects %}
    <!-- Subjects section -->
{% endif %}

{% should_show_section user 'certificates' as show_certificates %}
{% if show_certificates %}
    <!-- Certificates section -->
{% endif %}

{% should_show_section user 'mock_exams' as show_mock_exams %}
{% if show_mock_exams %}
    <!-- Mock exams section -->
{% endif %}

{% should_show_section user 'courses' as show_courses %}
{% if show_courses %}
    <!-- Courses section -->
{% endif %}
```

## 📋 The 5 Questions

1. **Role**: Abiturient, Talaba, O'qituvchi, Boshqa
2. **Subjects**: Dynamic from SubjectCategory model
3. **Certificates**: Dynamic from Certificate model
4. **Courses**: Dynamic from CourseCategory model
5. **Mock Exams**: Dynamic from MockExamCategory model

Each question (2-5) includes "Qiziqmaydi" option.

## 🎯 How It Works

### New User Flow
1. User registers → `onboarding_completed = False`
2. Middleware redirects to `/accounts/onboarding/`
3. User answers 5 questions
4. Preferences saved → `onboarding_completed = True`
5. Home page shows only selected sections

### Returning User
- If `onboarding_completed = True` → Personalized view
- If `onboarding_completed = False` → Redirect to onboarding

### Guest Users
- See all sections (no filtering)

## 🔧 Key Features

✅ **One-time experience** - Never shows again after completion
✅ **Dynamic categories** - All options from database
✅ **Multiple choice** - Can select multiple interests
✅ **Never fully restricts** - "Show All" button always available
✅ **Beautiful UI** - Modern, animated, responsive design
✅ **Smart filtering** - Shows only relevant sections
✅ **Easy reset** - Can restart onboarding anytime

## 📊 Database

Migration already applied:
```bash
python manage.py migrate accounts
```

Model: `UserInterestPreference`
- `user` - OneToOne with User
- `role` - CharField (abiturient, student, teacher, other)
- `selected_categories` - JSONField
- `onboarding_completed` - BooleanField

## 🎨 UI Preview

The onboarding page features:
- Purple gradient background
- Progress bar (0-100%)
- Card-based option selection
- Smooth animations
- Mobile responsive
- Icon-based options
- "Qiziqmaydi" option for each question

## 🧪 Testing

### Test New User
```bash
# 1. Create new account
# 2. Should redirect to /accounts/onboarding/
# 3. Answer questions
# 4. Click "Tugatish"
# 5. Home page shows only selected sections
```

### Test Show All
```bash
# 1. Complete onboarding
# 2. Click "Barcha bo'limlarni ko'rish" in banner
# 3. All sections should appear
```

### Test Reset
```bash
# Visit: /accounts/onboarding/reset/
# Should redirect to onboarding page with cleared preferences
```

## 📝 Admin Panel

Access: `/admin/accounts/userinterestpreference/`

Features:
- View all user preferences
- Filter by role, completion status
- See selected categories
- Manually edit preferences

## 🔍 Template Tag Usage

```django
{% load onboarding_tags %}

<!-- Check if section should show -->
{% should_show_section user 'subjects' as show_subjects %}
{% if show_subjects %}
    <!-- Content -->
{% endif %}

<!-- Check if user has any interests -->
{% if user|has_any_interests %}
    <!-- Show personalization banner -->
{% endif %}
```

## 🚨 Important Notes

1. **Middleware must be added** - Without it, onboarding won't auto-show
2. **Don't break existing features** - System only adds filtering
3. **Guest users see everything** - No restrictions for non-authenticated
4. **Always provide "Show All"** - Users can access full platform
5. **Test thoroughly** - Test with new users, existing users, guests

## 📚 Full Documentation

For complete details, see:
- `ONBOARDING_SYSTEM_GUIDE.md` - Complete system documentation
- `ONBOARDING_INTEGRATION_EXAMPLE.md` - Step-by-step integration

## 🎉 You're Done!

The onboarding system is ready to use. Just add the middleware and update your templates!

For questions or issues, check the full documentation files.
