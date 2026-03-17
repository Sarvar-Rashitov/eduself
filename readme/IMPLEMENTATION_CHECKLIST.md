# Onboarding System Implementation Checklist

## ✅ Already Completed

- [x] Created `UserInterestPreference` model
- [x] Created onboarding views (5 endpoints)
- [x] Created beautiful onboarding UI template
- [x] Created middleware for auto-redirect
- [x] Created template tags for filtering
- [x] Created context processor
- [x] Added admin panel integration
- [x] Created URL routes
- [x] Applied database migrations
- [x] Created documentation files

## 🔧 Required Configuration (You Must Do)

### 1. Add Middleware to Settings

**File**: `eduself/settings.py`

**Action**: Add this line to MIDDLEWARE list:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.LanguageMiddleware',
    'accounts.onboarding_middleware.OnboardingMiddleware',  # ← ADD THIS LINE
]
```

**Status**: ⏳ TODO

---

### 2. Add Context Processor (Optional but Recommended)

**File**: `eduself/settings.py`

**Action**: Add this line to context_processors:

```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
                'accounts.onboarding_context.user_preferences',  # ← ADD THIS LINE
            ],
        },
    },
]
```

**Status**: ⏳ TODO

---

### 3. Update Home Template

**File**: `templates/core/home_desktop.html`

**Actions**:

#### 3.1 Load Template Tags (at top of file)
```django
{% extends 'base_desktop.html' %}
{% load i18n %}
{% load static %}
{% load onboarding_tags %}  <!-- ← ADD THIS LINE -->
```

#### 3.2 Add Personalization Banner (after hero section)
```django
<!-- Hero Section -->
<section class="hero">
    <!-- ... existing content ... -->
</section>

<!-- ← ADD THIS SECTION -->
{% include 'accounts/onboarding_banner.html' %}

<!-- Stats Section -->
<section class="stats">
    <!-- ... existing content ... -->
</section>
```

#### 3.3 Wrap Subjects Section
```django
<!-- ← ADD THIS LINE -->
{% should_show_section user 'subjects' as show_subjects %}
{% if show_subjects %}  <!-- ← ADD THIS LINE -->

<section id="subjects" class="section subjects-section" ...>
    <!-- ... existing subjects content ... -->
</section>

{% endif %}  <!-- ← ADD THIS LINE -->
```

#### 3.4 Wrap Certificates Section
```django
<!-- ← ADD THIS LINE -->
{% should_show_section user 'certificates' as show_certificates %}
{% if show_certificates %}  <!-- ← ADD THIS LINE -->

<section id="certificates" class="section certificate-section" ...>
    <!-- ... existing certificates content ... -->
</section>

{% endif %}  <!-- ← ADD THIS LINE -->
```

#### 3.5 Wrap Mock Exams Section
```django
<!-- ← ADD THIS LINE -->
{% should_show_section user 'mock_exams' as show_mock_exams %}
{% if show_mock_exams %}  <!-- ← ADD THIS LINE -->

<section id="exams" class="section exams-section" ...>
    <!-- ... existing mock exams content ... -->
</section>

{% endif %}  <!-- ← ADD THIS LINE -->
```

#### 3.6 Wrap Courses Section (if exists)
```django
<!-- ← ADD THIS LINE -->
{% should_show_section user 'courses' as show_courses %}
{% if show_courses %}  <!-- ← ADD THIS LINE -->

<section id="courses" class="section courses-section" ...>
    <!-- ... existing courses content ... -->
</section>

{% endif %}  <!-- ← ADD THIS LINE -->
```

**Status**: ⏳ TODO

---

### 4. Add Reset Option to Profile Page (Optional)

**File**: `templates/accounts/profile.html` or similar

**Action**: Add this button somewhere in profile settings:

```django
<div class="settings-section">
    <h3>Shaxsiylashtirish</h3>
    <p>Platformani o'z qiziqishlaringizga moslang</p>
    <a href="{% url 'accounts:reset_onboarding' %}" class="btn btn-secondary">
        <i class="fas fa-redo"></i>
        Shaxsiylashtirish sozlamalarini qayta o'rnatish
    </a>
</div>
```

**Status**: ⏳ TODO (Optional)

---

## 🧪 Testing Checklist

After completing configuration, test these scenarios:

### Test 1: New User Registration
- [ ] Register a new account
- [ ] Should automatically redirect to `/accounts/onboarding/`
- [ ] See 5 questions with progress bar
- [ ] Select options (can select multiple for questions 2-5)
- [ ] Click "Tugatish" button
- [ ] Should redirect to home page
- [ ] Only selected sections should be visible
- [ ] Purple banner should appear at top

### Test 2: Personalization Banner
- [ ] After completing onboarding, see purple banner
- [ ] Banner shows: "Siz tanlagan bo'limlarga asoslangan..."
- [ ] Click "Barcha bo'limlarni ko'rish" button
- [ ] All sections should now appear
- [ ] Banner should disappear

### Test 3: Existing User Login
- [ ] Log in with existing account (that hasn't done onboarding)
- [ ] Should redirect to onboarding
- [ ] Complete onboarding
- [ ] Next login should show personalized view

### Test 4: Guest User
- [ ] Visit site without logging in
- [ ] All sections should be visible
- [ ] No personalization banner
- [ ] No onboarding prompt

### Test 5: Reset Onboarding
- [ ] Go to `/accounts/onboarding/reset/`
- [ ] Should redirect to onboarding page
- [ ] Previous selections should be cleared
- [ ] Can select new preferences

### Test 6: Skip Onboarding
- [ ] Start onboarding
- [ ] Click "Hozir emas, keyinroq" button
- [ ] Should redirect to home
- [ ] All sections visible (no filtering)

### Test 7: Admin Panel
- [ ] Go to `/admin/accounts/userinterestpreference/`
- [ ] See list of user preferences
- [ ] Can filter by role, completion status
- [ ] Can view/edit individual preferences

---

## 📊 Verification Commands

Run these to verify everything is set up:

```bash
# Check migrations
python manage.py showmigrations accounts

# Should show:
# [X] 0020_userinterestpreference

# Check if model exists
python manage.py shell
>>> from accounts.onboarding_models import UserInterestPreference
>>> UserInterestPreference.objects.count()
# Should work without errors

# Check if URLs are registered
python manage.py show_urls | grep onboarding
# Should show onboarding URLs
```

---

## 🚨 Common Issues & Solutions

### Issue 1: Redirect Loop
**Symptom**: Onboarding page keeps redirecting to itself

**Solution**: Check middleware exclusions in `onboarding_middleware.py`:
```python
self.excluded_paths = [
    '/accounts/onboarding/',
    '/accounts/onboarding/save/',
    '/accounts/onboarding/skip/',
    # ... should include all onboarding URLs
]
```

### Issue 2: Sections Not Filtering
**Symptom**: All sections show even after onboarding

**Solution**: 
1. Check template tags are loaded: `{% load onboarding_tags %}`
2. Check user has completed onboarding in admin
3. Check correct section type is used

### Issue 3: Template Tag Not Found
**Symptom**: `TemplateSyntaxError: 'onboarding_tags' is not a registered tag library`

**Solution**:
1. Restart Django server
2. Check `accounts/templatetags/__init__.py` exists
3. Check `accounts/templatetags/onboarding_tags.py` exists

### Issue 4: Middleware Not Working
**Symptom**: New users not redirected to onboarding

**Solution**:
1. Check middleware is added to `settings.py`
2. Check middleware is after `AuthenticationMiddleware`
3. Restart Django server

---

## 📝 Final Checklist

Before deploying to production:

- [ ] Middleware added to settings
- [ ] Context processor added (optional)
- [ ] Home template updated with filtering
- [ ] All 7 test scenarios passed
- [ ] Admin panel accessible
- [ ] Documentation reviewed
- [ ] Code committed to git
- [ ] Tested on staging environment

---

## 📚 Documentation Files

Reference these files for more details:

1. **ONBOARDING_QUICK_START.md** - Quick overview and setup
2. **ONBOARDING_SYSTEM_GUIDE.md** - Complete system documentation
3. **ONBOARDING_INTEGRATION_EXAMPLE.md** - Step-by-step integration guide
4. **IMPLEMENTATION_CHECKLIST.md** - This file

---

## 🎉 You're Ready!

Once all items are checked, the onboarding system is fully functional!

**Estimated Time**: 15-30 minutes for configuration and testing

**Difficulty**: Easy (mostly copy-paste configuration)

Good luck! 🚀
