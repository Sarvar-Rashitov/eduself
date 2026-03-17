# Onboarding System Architecture

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER REGISTRATION                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ User.created     │
                    │ onboarding_      │
                    │ completed=False  │
                    └──────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ONBOARDING MIDDLEWARE                         │
│  Checks: user.interest_preference.onboarding_completed           │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
              False │                   │ True
                    ▼                   ▼
        ┌──────────────────┐   ┌──────────────────┐
        │ Redirect to      │   │ Continue to      │
        │ /onboarding/     │   │ requested page   │
        └──────────────────┘   └──────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ONBOARDING PAGE (5 Questions)                 │
│                                                                  │
│  Q1: Role (Single choice)                                       │
│      ├─ Abiturient                                              │
│      ├─ Talaba                                                  │
│      ├─ O'qituvchi                                              │
│      └─ Boshqa                                                  │
│                                                                  │
│  Q2: Subjects (Multiple choice)                                 │
│      ├─ [Dynamic from SubjectCategory]                          │
│      └─ Qiziqmaydi                                              │
│                                                                  │
│  Q3: Certificates (Multiple choice)                             │
│      ├─ [Dynamic from Certificate]                              │
│      └─ Qiziqmaydi                                              │
│                                                                  │
│  Q4: Courses (Multiple choice)                                  │
│      ├─ [Dynamic from CourseCategory]                           │
│      └─ Qiziqmaydi                                              │
│                                                                  │
│  Q5: Mock Exams (Multiple choice)                               │
│      ├─ [Dynamic from MockExamCategory]                         │
│      └─ Qiziqmaydi                                              │
│                                                                  │
│  [Skip Button] ────────────────────────┐                        │
│  [Complete Button]                     │                        │
└────────────────────────────────────────┼────────────────────────┘
                    │                    │
                    ▼                    ▼
        ┌──────────────────┐   ┌──────────────────┐
        │ Save preferences │   │ Skip onboarding  │
        │ POST /save/      │   │ POST /skip/      │
        └──────────────────┘   └──────────────────┘
                    │                    │
                    └────────┬───────────┘
                             ▼
                ┌──────────────────────────┐
                │ UserInterestPreference   │
                │ onboarding_completed=True│
                └──────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Redirect to     │
                    │ Home Page       │
                    └─────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      HOME PAGE RENDERING                         │
│                                                                  │
│  Template Tag: {% should_show_section user 'subjects' %}        │
│                                                                  │
│  Logic:                                                          │
│  ├─ If user not authenticated → Show all                        │
│  ├─ If onboarding not completed → Show all                      │
│  ├─ If no preferences saved → Show all                          │
│  └─ If preferences exist → Filter sections                      │
│                                                                  │
│  Sections:                                                       │
│  ├─ Subjects      [Conditional]                                 │
│  ├─ Certificates  [Conditional]                                 │
│  ├─ Courses       [Conditional]                                 │
│  ├─ Mock Exams    [Conditional]                                 │
│  └─ Institutions  [Always shown]                                │
│                                                                  │
│  Banner: "Showing personalized content"                         │
│  Button: "Show All Platform" → Clears preferences               │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         DJANGO PROJECT                           │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    ACCOUNTS APP                            │ │
│  │                                                            │ │
│  │  Models:                                                   │ │
│  │  ├─ User (existing)                                        │ │
│  │  └─ UserInterestPreference (new)                           │ │
│  │      ├─ user (OneToOne)                                    │ │
│  │      ├─ role (CharField)                                   │ │
│  │      ├─ selected_categories (JSONField)                    │ │
│  │      └─ onboarding_completed (BooleanField)                │ │
│  │                                                            │ │
│  │  Views:                                                    │ │
│  │  ├─ onboarding_view()                                      │ │
│  │  ├─ save_onboarding()                                      │ │
│  │  ├─ skip_onboarding()                                      │ │
│  │  ├─ show_all_platform()                                    │ │
│  │  └─ reset_onboarding()                                     │ │
│  │                                                            │ │
│  │  Middleware:                                               │ │
│  │  └─ OnboardingMiddleware                                   │ │
│  │      └─ Redirects new users to onboarding                  │ │
│  │                                                            │ │
│  │  Template Tags:                                            │ │
│  │  ├─ should_show_section                                    │ │
│  │  └─ has_any_interests                                      │ │
│  │                                                            │ │
│  │  Context Processor:                                        │ │
│  │  └─ user_preferences                                       │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                      CORE APP                              │ │
│  │                                                            │ │
│  │  Models (existing, reused):                                │ │
│  │  ├─ SubjectCategory                                        │ │
│  │  ├─ Certificate                                            │ │
│  │  ├─ CourseCategory                                         │ │
│  │  └─ MockExamCategory                                       │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    TEMPLATES                               │ │
│  │                                                            │ │
│  │  ├─ accounts/onboarding.html                               │ │
│  │  │   └─ 5-question onboarding UI                           │ │
│  │  │                                                          │ │
│  │  ├─ accounts/onboarding_banner.html                        │ │
│  │  │   └─ Personalization banner                             │ │
│  │  │                                                          │ │
│  │  └─ core/home_desktop.html (modified)                      │ │
│  │      └─ Uses template tags for filtering                   │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌──────────────┐
│   Browser    │
└──────┬───────┘
       │ 1. Request page
       ▼
┌──────────────────────┐
│   Middleware Stack   │
│                      │
│  ┌────────────────┐  │
│  │ Onboarding     │  │
│  │ Middleware     │  │
│  └────────┬───────┘  │
└───────────┼──────────┘
            │ 2. Check onboarding status
            ▼
┌──────────────────────┐
│   Database           │
│                      │
│  UserInterest        │
│  Preference          │
│  ├─ onboarding_      │
│  │  completed?       │
│  └─ selected_        │
│     categories       │
└───────────┬──────────┘
            │ 3. Return status
            ▼
┌──────────────────────┐
│   View               │
│                      │
│  ├─ If False:        │
│  │  Redirect to      │
│  │  onboarding       │
│  │                   │
│  └─ If True:         │
│     Continue to      │
│     requested page   │
└───────────┬──────────┘
            │ 4. Render template
            ▼
┌──────────────────────┐
│   Template           │
│                      │
│  Template Tags:      │
│  ├─ Load preferences │
│  ├─ Filter sections  │
│  └─ Show banner      │
└───────────┬──────────┘
            │ 5. HTML response
            ▼
┌──────────────┐
│   Browser    │
└──────────────┘
```

## Database Schema

```
┌─────────────────────────────────────────────────────────────┐
│                    accounts_user                            │
├─────────────────────────────────────────────────────────────┤
│ id (PK)                                                     │
│ username                                                    │
│ email                                                       │
│ first_name                                                  │
│ last_name                                                   │
│ ...                                                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ OneToOne
                              ▼
┌─────────────────────────────────────────────────────────────┐
│           accounts_userinterestpreference                   │
├─────────────────────────────────────────────────────────────┤
│ id (PK)                                                     │
│ user_id (FK) → accounts_user.id                             │
│ role (VARCHAR)                                              │
│   ├─ 'abiturient'                                           │
│   ├─ 'student'                                              │
│   ├─ 'teacher'                                              │
│   └─ 'other'                                                │
│ selected_categories (JSON)                                  │
│   {                                                         │
│     "subjects": [1, 2, 3],                                  │
│     "certificates": [1],                                    │
│     "courses": [2, 3],                                      │
│     "mock_exams": [1, 2]                                    │
│   }                                                         │
│ onboarding_completed (BOOLEAN)                              │
│ created_at (DATETIME)                                       │
│ updated_at (DATETIME)                                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ References (via JSON IDs)
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Existing Category Models (not modified)                     │
│                                                              │
│  ├─ core_subjectcategory                                     │
│  ├─ core_certificate                                         │
│  ├─ core_coursecategory                                      │
│  └─ core_mockexamcategory                                    │
└──────────────────────────────────────────────────────────────┘
```

## Request/Response Flow

### Scenario 1: New User First Visit

```
User → Register → Login
                    │
                    ▼
            ┌───────────────┐
            │ Middleware    │
            │ checks        │
            └───────┬───────┘
                    │
                    ▼ onboarding_completed = False
            ┌───────────────┐
            │ Redirect 302  │
            │ /onboarding/  │
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │ Onboarding    │
            │ Page (5 Q's)  │
            └───────┬───────┘
                    │
                    ▼ User answers
            ┌───────────────┐
            │ POST /save/   │
            │ Save prefs    │
            └───────┬───────┘
                    │
                    ▼ onboarding_completed = True
            ┌───────────────┐
            │ Redirect 302  │
            │ /home/        │
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │ Home Page     │
            │ (Filtered)    │
            └───────────────┘
```

### Scenario 2: Returning User

```
User → Login
        │
        ▼
┌───────────────┐
│ Middleware    │
│ checks        │
└───────┬───────┘
        │
        ▼ onboarding_completed = True
┌───────────────┐
│ Continue to   │
│ /home/        │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Template      │
│ loads prefs   │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Filter        │
│ sections      │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Home Page     │
│ (Filtered)    │
└───────────────┘
```

### Scenario 3: Guest User

```
User → Visit /home/
        │
        ▼
┌───────────────┐
│ Middleware    │
│ checks        │
└───────┬───────┘
        │
        ▼ user.is_authenticated = False
┌───────────────┐
│ Skip check    │
│ Continue      │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Template      │
│ no filtering  │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Home Page     │
│ (All sections)│
└───────────────┘
```

## Key Design Decisions

### 1. Why JSONField for selected_categories?

**Pros:**
- Flexible structure
- No additional tables needed
- Easy to query and update
- Supports multiple category types

**Cons:**
- Can't use foreign key constraints
- Requires manual validation

**Decision:** JSONField is better for this use case because:
- Categories are reference data, not relational
- Simplifies queries
- Easier to extend with new category types

### 2. Why Middleware instead of Decorator?

**Pros:**
- Applies globally to all views
- No need to add decorator to each view
- Centralized logic

**Cons:**
- Runs on every request
- Need to exclude certain paths

**Decision:** Middleware is better because:
- Ensures onboarding is never missed
- Cleaner code (no decorators everywhere)
- Easy to exclude specific paths

### 3. Why Template Tags instead of View Logic?

**Pros:**
- Reusable across templates
- Keeps view logic simple
- Easy to test

**Cons:**
- Adds template complexity

**Decision:** Template tags are better because:
- Separation of concerns
- Reusable in multiple templates
- Easier to maintain

## Performance Considerations

### Database Queries

```python
# Efficient: Single query with select_related
preference = user.interest_preference  # Uses OneToOne, cached

# Efficient: JSON field access (no additional queries)
categories = preference.selected_categories.get('subjects', [])

# Efficient: Batch query for categories
SubjectCategory.objects.filter(id__in=categories)
```

### Caching Strategy

```python
# User preferences are cached on user object
# No need for additional caching layer

# Template tag caches result during template rendering
@register.simple_tag
def should_show_section(user, section_type):
    # Result is cached for template render cycle
    ...
```

### Middleware Performance

```python
# Middleware only checks authenticated users
if not request.user.is_authenticated:
    return  # Skip check, no DB query

# Single DB query per request (cached on user object)
preference = request.user.interest_preference
```

## Security Considerations

1. **CSRF Protection**: All POST endpoints use CSRF tokens
2. **Authentication Required**: All onboarding endpoints require login
3. **Input Validation**: Category IDs validated against database
4. **No SQL Injection**: Using Django ORM
5. **XSS Protection**: Django template auto-escaping

## Scalability

- **Database**: Single table, indexed on user_id
- **Queries**: O(1) lookups using OneToOne relationship
- **Memory**: Minimal (JSON field, small data)
- **Caching**: User object caching handles most cases

## Future Enhancements

1. **Analytics Dashboard**
   - Track popular category combinations
   - A/B test different question orders
   - Measure completion rates

2. **Machine Learning**
   - Recommend categories based on similar users
   - Predict user interests from behavior

3. **Advanced Filtering**
   - Time-based recommendations
   - Difficulty-based filtering
   - Progress-based suggestions

4. **Social Features**
   - Share preferences with friends
   - Compare interests with peers
   - Group recommendations
