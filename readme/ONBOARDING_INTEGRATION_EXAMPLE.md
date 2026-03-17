# How to Integrate Onboarding into Home Page

## Step 1: Add Middleware to Settings

Edit `eduself/settings.py`:

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
    'accounts.onboarding_middleware.OnboardingMiddleware',  # ADD THIS LINE
]
```

## Step 2: Add Context Processor (Optional)

Edit `eduself/settings.py`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
                'accounts.onboarding_context.user_preferences',  # ADD THIS LINE
            ],
        },
    },
]
```

## Step 3: Update Home Template

Edit `templates/core/home_desktop.html`:

### Add at the top (after extends and load static):

```django
{% extends 'base_desktop.html' %}
{% load i18n %}
{% load static %}
{% load onboarding_tags %}  <!-- ADD THIS LINE -->
```

### Add personalization banner (after hero section):

```django
<!-- Hero Section -->
<section class="hero">
    <!-- ... existing hero content ... -->
</section>

<!-- ADD THIS: Personalization Banner -->
{% include 'accounts/onboarding_banner.html' %}

<!-- Stats Section -->
<section class="stats">
    <!-- ... existing stats content ... -->
</section>
```

### Wrap sections with personalization checks:

#### Subjects Section:

```django
<!-- Subjects Section -->
{% should_show_section user 'subjects' as show_subjects %}
{% if show_subjects %}
<section id="subjects" class="section subjects-section" style="background-image: url('{% static 'images/fanlar.jpg' %}'); ...">
    <!-- ... existing subjects content ... -->
</section>
{% endif %}
```

#### Certificates Section:

```django
<!-- Certificates Section -->
{% should_show_section user 'certificates' as show_certificates %}
{% if show_certificates %}
<section id="certificates" class="section certificate-section" style="background-image: url('{% static 'images/univer.png' %}'); ...">
    <!-- ... existing certificates content ... -->
</section>
{% endif %}
```

#### Mock Exams Section:

```django
<!-- Mock Exams Section -->
{% should_show_section user 'mock_exams' as show_mock_exams %}
{% if show_mock_exams %}
<section id="exams" class="section exams-section" style="background-image: url('{% static 'images/univer.png' %}'); ...">
    <!-- ... existing mock exams content ... -->
</section>
{% endif %}
```

#### Courses Section (if you have one):

```django
<!-- Courses Section -->
{% should_show_section user 'courses' as show_courses %}
{% if show_courses %}
<section id="courses" class="section courses-section">
    <!-- ... courses content ... -->
</section>
{% endif %}
```

#### Institutions Section (always shown):

```django
<!-- Institutions Section - Always shown -->
<section id="institutions" class="section institutions-section">
    <!-- ... existing institutions content ... -->
</section>
```

## Step 4: Test the System

### Test 1: New User Registration

1. Register a new account
2. You should be redirected to `/accounts/onboarding/`
3. Answer the 5 questions
4. Click "Tugatish"
5. You'll be redirected to home page
6. Only selected sections should be visible

### Test 2: Show All Platform

1. After completing onboarding, you'll see a purple banner at the top
2. Click "Barcha bo'limlarni ko'rish" button
3. All sections should now be visible

### Test 3: Existing Users

1. Log in with an existing account
2. If they haven't completed onboarding, they'll be redirected
3. If they have, they'll see their personalized view

### Test 4: Guest Users

1. Visit the site without logging in
2. All sections should be visible
3. No personalization banner

## Step 5: Add Reset Option to Profile Page

Edit `templates/accounts/profile.html` (or wherever your profile settings are):

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

## Complete Example: Minimal Integration

Here's a minimal example showing the key changes:

```django
{% extends 'base_desktop.html' %}
{% load static %}
{% load onboarding_tags %}

{% block content %}

<!-- Personalization Banner -->
{% include 'accounts/onboarding_banner.html' %}

<!-- Hero Section - Always shown -->
<section class="hero">
    <h1>Welcome to EduSelf</h1>
</section>

<!-- Subjects - Conditional -->
{% should_show_section user 'subjects' as show_subjects %}
{% if show_subjects %}
<section id="subjects">
    <h2>Fanlar</h2>
    <!-- subjects content -->
</section>
{% endif %}

<!-- Certificates - Conditional -->
{% should_show_section user 'certificates' as show_certificates %}
{% if show_certificates %}
<section id="certificates">
    <h2>Sertifikatlar</h2>
    <!-- certificates content -->
</section>
{% endif %}

<!-- Mock Exams - Conditional -->
{% should_show_section user 'mock_exams' as show_mock_exams %}
{% if show_mock_exams %}
<section id="exams">
    <h2>Mock Imtihonlar</h2>
    <!-- mock exams content -->
</section>
{% endif %}

<!-- Courses - Conditional -->
{% should_show_section user 'courses' as show_courses %}
{% if show_courses %}
<section id="courses">
    <h2>Kurslar</h2>
    <!-- courses content -->
</section>
{% endif %}

<!-- Institutions - Always shown -->
<section id="institutions">
    <h2>Ta'lim Muassasalari</h2>
    <!-- institutions content -->
</section>

{% endblock %}
```

## Important Notes

1. **Don't break existing functionality**: The system only adds filtering, doesn't remove features
2. **Guest users see everything**: No restrictions for non-authenticated users
3. **Always provide "Show All" option**: Users can always access full platform
4. **Test thoroughly**: Test with new users, existing users, and guests

## Troubleshooting

### Issue: Redirect loop on onboarding page

**Solution**: Make sure middleware exclusions include onboarding URLs:
```python
self.excluded_paths = [
    '/accounts/onboarding/',
    '/accounts/onboarding/save/',
    '/accounts/onboarding/skip/',
    # ... other paths
]
```

### Issue: Sections not filtering

**Solution**: Check that:
1. Template tags are loaded: `{% load onboarding_tags %}`
2. User has completed onboarding
3. Correct section type is used

### Issue: Banner not showing

**Solution**: Check that:
1. User is authenticated
2. User has completed onboarding
3. User has selected at least one interest

## Next Steps

After integration:
1. Test with real users
2. Monitor analytics
3. Gather feedback
4. Adjust questions if needed
5. Add more personalization features
