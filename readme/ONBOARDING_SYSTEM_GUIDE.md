# EduSelf Onboarding & Personalization System

## Overview

The onboarding system helps new users personalize their EduSelf experience by selecting their interests. Based on their choices, the platform shows relevant sections and hides unrelated content.

## Features

✅ **5-Question Onboarding Flow**
- Question 1: User role (Abiturient, Student, Teacher, Other)
- Question 2: Subject categories interest
- Question 3: Certificate exam interest
- Question 4: Online course interest
- Question 5: Mock exam interest

✅ **Dynamic Category Loading**
- All options are loaded from existing database categories
- No hardcoded values
- Multiple choice enabled for questions 2-5

✅ **Smart Navigation Filtering**
- Shows only relevant sections based on user preferences
- Never fully restricts platform access
- "Show All Platform" button available

✅ **One-Time Experience**
- Shows only for newly registered users
- Never appears again after completion
- Can be reset from profile settings

## Installation

### 1. Models Already Created

The system uses `UserInterestPreference` model in `accounts/onboarding_models.py`:

```python
class UserInterestPreference(models.Model):
    user = OneToOneField(User)
    role = CharField(choices=ROLE_CHOICES)
    selected_categories = JSONField()  # Stores: {'subjects': [ids], 'certificates': [ids], ...}
    onboarding_completed = BooleanField(default=False)
```

### 2. Middleware Configuration

Add the middleware to `settings.py`:

```python
MIDDLEWARE = [
    # ... other middleware
    'accounts.onboarding_middleware.OnboardingMiddleware',  # Add this
]
```

### 3. Context Processor (Optional)

Add to `settings.py` for template access:

```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... other processors
                'accounts.onboarding_context.user_preferences',  # Add this
            ],
        },
    },
]
```

### 4. Migrations

Already applied:
```bash
python manage.py makemigrations accounts
python manage.py migrate accounts
```

## Usage in Templates

### Load Template Tags

```django
{% load onboarding_tags %}
```

### Check if Section Should Be Shown

```django
{% should_show_section user 'subjects' as show_subjects %}
{% if show_subjects %}
    <!-- Subjects section content -->
{% endif %}
```

### Available Section Types

- `'subjects'` - Fan kategoriyalari
- `'certificates'` - Sertifikat imtihonlari
- `'courses'` - Online kurslar
- `'mock_exams'` - Mock imtihonlar
- `'institutions'` - Ta'lim muassasalari (always shown)

### Example: Filtering Home Page Sections

```django
{% load onboarding_tags %}

<!-- Subjects Section -->
{% should_show_section user 'subjects' as show_subjects %}
{% if show_subjects %}
<section id="subjects" class="section subjects-section">
    <!-- Subjects content -->
</section>
{% endif %}

<!-- Certificates Section -->
{% should_show_section user 'certificates' as show_certificates %}
{% if show_certificates %}
<section id="certificates" class="section certificate-section">
    <!-- Certificates content -->
</section>
{% endif %}

<!-- Courses Section -->
{% should_show_section user 'courses' as show_courses %}
{% if show_courses %}
<section id="courses" class="section courses-section">
    <!-- Courses content -->
</section>
{% endif %}

<!-- Mock Exams Section -->
{% should_show_section user 'mock_exams' as show_mock_exams %}
{% if show_mock_exams %}
<section id="exams" class="section exams-section">
    <!-- Mock exams content -->
</section>
{% endif %}
```

### Show Personalization Banner

```django
{% include 'accounts/onboarding_banner.html' %}
```

This banner shows:
- Only for authenticated users who completed onboarding
- Message: "Showing personalized recommendations"
- Button: "Show All Platform" to disable filtering

## User Flow

### New User Registration

1. User registers → `onboarding_completed = False`
2. Middleware redirects to `/accounts/onboarding/`
3. User answers 5 questions
4. Preferences saved → `onboarding_completed = True`
5. Redirected to home page with personalized view

### Returning User

1. User logs in
2. Middleware checks `onboarding_completed`
3. If `True` → Normal home page (personalized)
4. If `False` → Redirect to onboarding

### Guest Users

- See all sections (no filtering)
- No onboarding prompt

## API Endpoints

### GET `/accounts/onboarding/`
Shows onboarding page with 5 questions

### POST `/accounts/onboarding/save/`
Saves user preferences
```json
{
    "role": "student",
    "subjects": [1, 2, 3],
    "certificates": [1],
    "courses": [2, 3],
    "mock_exams": []
}
```

### POST `/accounts/onboarding/skip/`
Marks onboarding as completed without saving preferences

### GET `/accounts/onboarding/show-all/`
Clears preferences to show all platform sections

### GET `/accounts/onboarding/reset/`
Resets onboarding to start over

## Admin Panel

Access at `/admin/accounts/userinterestpreference/`

Features:
- View all user preferences
- See selected categories
- Filter by role, completion status
- Manually edit preferences

## Customization

### Add New Question

1. Update `onboarding.html` template
2. Add new question container
3. Update JavaScript to handle new question
4. Modify `save_onboarding` view to process new data

### Change Question Text

Edit `templates/accounts/onboarding.html`:
```html
<h2 class="question-title">Your new question text?</h2>
```

### Modify Intro Message

Edit the intro section in `onboarding.html`:
```html
<div class="onboarding-intro">
    <p>Your custom intro message here...</p>
</div>
```

## Important Notes

⚠️ **Never Fully Restrict Platform**
- Even with personalization, users can access all sections
- "Show All Platform" button is always available
- Guest users see everything

⚠️ **Existing Models Reused**
- No new category models created
- Uses existing: `SubjectCategory`, `Certificate`, `CourseCategory`, `MockExamCategory`

⚠️ **Middleware Exclusions**
- Onboarding pages excluded from redirect loop
- Static/media files excluded
- Admin panel excluded
- Auth pages excluded

## Testing

### Test Onboarding Flow

1. Create new user account
2. Should redirect to `/accounts/onboarding/`
3. Answer all 5 questions
4. Click "Tugatish"
5. Should redirect to home with personalized view

### Test Personalization

1. Complete onboarding with specific interests
2. Home page should show only selected sections
3. Click "Show All Platform" button
4. All sections should appear

### Test Reset

1. Go to `/accounts/onboarding/reset/`
2. Should redirect to onboarding page
3. Previous answers cleared
4. Can select new preferences

## Troubleshooting

### Onboarding Not Showing

Check:
- Middleware is added to `settings.py`
- User is authenticated
- `onboarding_completed = False` in database

### Sections Not Filtering

Check:
- Template tags are loaded: `{% load onboarding_tags %}`
- Using correct section type names
- User has completed onboarding

### Redirect Loop

Check:
- Onboarding URLs are in middleware exclusions
- User preference exists in database

## Future Enhancements

Possible improvements:
- Add more questions
- Machine learning recommendations
- A/B testing different onboarding flows
- Analytics dashboard for admin
- Email reminders for incomplete onboarding

## Support

For issues or questions:
- Check this guide first
- Review code in `accounts/onboarding_*.py` files
- Test in admin panel: `/admin/accounts/userinterestpreference/`
