# Onboarding System - Quick Test Guide

## 🧪 How to Test the Complete System

### Test 1: New User Onboarding Flow
```bash
# 1. Start the development server
python manage.py runserver

# 2. Open browser and go to registration page
http://localhost:8000/accounts/register/

# 3. Register a new user
- Fill in registration form
- Submit

# Expected: Should redirect to onboarding page
```

**Onboarding Page Checks**:
- [ ] See 5 questions
- [ ] Q1: Role selection (Abiturient/Talaba/O'qituvchi/Boshqa)
- [ ] Q2: Subjects with categories from database
- [ ] Q3: Certificates with options from database
- [ ] Q4: Courses with categories from database
- [ ] Q5: Mock Exams with categories from database
- [ ] Each Q2-5 has "Qiziqmaydi" option
- [ ] Can select multiple options
- [ ] Progress bar shows 0-100%
- [ ] Beautiful animations and gradients

**Complete Onboarding**:
- [ ] Select at least 2 categories in Q2 (e.g., "Aniq fanlar", "Ijtimoiy fanlar")
- [ ] Select at least 1 certificate in Q3 (e.g., "SAT")
- [ ] Select at least 1 course category in Q4
- [ ] Select at least 1 mock exam category in Q5
- [ ] Click "Tugatish" button
- [ ] See success modal
- [ ] Modal shows what sections were enabled
- [ ] Click "Platformaga o'tish"
- [ ] Redirected to home page

### Test 2: Personalized Navigation
**Desktop Navigation** (if using desktop):
```
Check header navigation:
- [ ] Only selected sections visible
- [ ] If selected "Fanlar" → "Fanlar" link visible
- [ ] If NOT selected "Kurslar" → "Kurslar" link hidden
- [ ] "Muassasalar" always visible
```

**Mobile Navigation**:
```
Check bottom navigation:
- [ ] Only selected sections visible
- [ ] Icons match selected categories
- [ ] "Muassasalar" always visible
```

### Test 3: Filtered Pages
**Subjects Page**:
```
Navigate to: /subjects/

Expected:
- [ ] See purple banner at top
- [ ] Banner says "Shaxsiylashtirilgan ko'rinish"
- [ ] Filter tabs show ONLY selected categories
- [ ] Example: Selected 2 → Only 2 tabs visible
- [ ] Click "Barchasini ko'rish" → Shows all categories
```

**Certificates Page**:
```
Navigate to: /certificates/

Expected:
- [ ] See green banner at top
- [ ] Only selected certificates visible
- [ ] Quick access button works
```

**Mock Exams Page**:
```
Navigate to: /mock-exams/

Expected:
- [ ] See orange banner at top
- [ ] Only selected exam categories visible
- [ ] Filter tabs show only selected
```

**Courses Page**:
```
Navigate to: /courses/

Expected:
- [ ] See purple banner at top
- [ ] Only selected course categories visible
- [ ] Filtering works correctly
```

### Test 4: Mobile Home Page
```
Navigate to: / (on mobile or resize browser)

Expected:
- [ ] Features carousel shows only selected sections
- [ ] If selected "Fanlar" → "Fanlar" card visible
- [ ] If NOT selected "Kurslar" → "Kurslar" card hidden
- [ ] "Muassasalar" always visible
- [ ] "Reyting" always visible
- [ ] Carousel loops correctly
```

### Test 5: Profile Controls
```
Navigate to: /accounts/profile/

Steps:
1. Click "Sozlamalar" tab
2. See "Shaxsiylashtirish" section
3. Click "To'liq platformani ko'rish"

Expected:
- [ ] Redirected to home
- [ ] All categories now visible everywhere
- [ ] Navigation shows all sections
- [ ] Filter tabs show all categories
- [ ] Banners disappear

4. Go back to profile → Sozlamalar
5. Click "Qiziqishlarimni qayta tanlash"

Expected:
- [ ] Redirected to onboarding page
- [ ] Can select new preferences
- [ ] Previous selections cleared
```

### Test 6: Persistence
```
Steps:
1. Complete onboarding with specific selections
2. Logout
3. Login again

Expected:
- [ ] NO onboarding shown
- [ ] Preferences persist
- [ ] Same filtered view as before
- [ ] Navigation still filtered
```

### Test 7: Guest User
```
Steps:
1. Logout (or open incognito window)
2. Visit home page
3. Navigate to subjects, certificates, etc.

Expected:
- [ ] See ALL categories
- [ ] No filtering applied
- [ ] No personalization banners
- [ ] Full platform access
```

## 🐛 Common Issues & Solutions

### Issue: Onboarding not showing
**Solution**: Check middleware is enabled in settings.py
```python
MIDDLEWARE = [
    ...
    'accounts.onboarding_middleware.OnboardingMiddleware',
]
```

### Issue: Categories not loading
**Solution**: Ensure database has categories
```bash
python manage.py shell
>>> from core.models import SubjectCategory
>>> SubjectCategory.objects.all()
```

### Issue: Filtering not working
**Solution**: Check template tags are loaded
```html
{% load onboarding_tags %}
{% should_show_section user 'subjects' as show_subjects %}
```

### Issue: Profile buttons not visible
**Solution**: Complete onboarding first, then check profile

## ✅ Success Criteria

All tests pass if:
1. ✅ New users see onboarding
2. ✅ Onboarding saves preferences correctly
3. ✅ Navigation filters based on preferences
4. ✅ All pages show only selected categories
5. ✅ Visual indicators appear on filtered pages
6. ✅ Profile controls work correctly
7. ✅ Preferences persist across sessions
8. ✅ Guest users see everything
9. ✅ No errors in console
10. ✅ Beautiful UI with animations

## 📊 Test Results Template

```
Date: ___________
Tester: ___________

Test 1 - New User Onboarding: [ ] PASS [ ] FAIL
Test 2 - Personalized Navigation: [ ] PASS [ ] FAIL
Test 3 - Filtered Pages: [ ] PASS [ ] FAIL
Test 4 - Mobile Home Page: [ ] PASS [ ] FAIL
Test 5 - Profile Controls: [ ] PASS [ ] FAIL
Test 6 - Persistence: [ ] PASS [ ] FAIL
Test 7 - Guest User: [ ] PASS [ ] FAIL

Notes:
_________________________________
_________________________________
_________________________________
```

## 🚀 Quick Test Commands

```bash
# Check for errors
python manage.py check

# Run migrations (if needed)
python manage.py migrate

# Create test user
python manage.py createsuperuser

# Start server
python manage.py runserver

# Open in browser
http://localhost:8000
```

## 📝 Manual Testing Checklist

### Desktop Testing
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge

### Mobile Testing
- [ ] iOS Safari
- [ ] Android Chrome
- [ ] Responsive mode in browser

### User Scenarios
- [ ] New user registration
- [ ] Existing user login
- [ ] Guest browsing
- [ ] Profile management
- [ ] Category selection
- [ ] Full platform toggle

## 🎯 Expected Behavior Summary

**New Users**: Onboarding → Select interests → Personalized view
**Returning Users**: Login → See personalized view → Can toggle full view
**Guest Users**: Browse → See everything → No restrictions

**Key Points**:
- Onboarding is one-time only
- Preferences persist forever
- Users can always see full platform
- No functionality is restricted
- Beautiful, smooth animations
- Mobile-first responsive design
