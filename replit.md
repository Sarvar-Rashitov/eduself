# EduSelf - O'zbekiston Ta'lim Platformasi

## Overview
EduSelf - bu O'zbekiston uchun yaratilgan zamonaviy ta'lim platformasi. Platforma mobile-first dizayn asosida qurilgan va Django MVT (Model-View-Template) arxitekturasiga asoslangan.

**Domain**: eduself.uz

## Project Architecture

### Tech Stack
- **Backend**: Django 5.2.8 (Python)
- **Database**: PostgreSQL
- **Frontend**: Django Templates + Bootstrap 5
- **CSS**: Custom mobile-first responsive design

### Directory Structure
```
/
├── eduself/           # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/          # User authentication app
│   ├── models.py      # User, PasswordResetToken
│   ├── views.py       # Login, Register, Profile
│   ├── forms.py       # Auth forms
│   └── admin.py
├── core/              # Main application
│   ├── models.py      # Subjects, Tests, Institutions, etc.
│   ├── views.py       # All page views
│   ├── admin.py       # CMS configuration
│   └── templatetags/  # Custom filters
├── templates/         # HTML templates
│   ├── base.html      # Base template with mobile nav
│   ├── accounts/      # Auth templates
│   └── core/          # Page templates
├── static/
│   └── css/style.css  # Mobile-first CSS
└── media/             # User uploads
```

## Key Features

### 1. User Authentication
- Username, email, password registration
- Login/Logout functionality
- Password reset via email link
- Profile management with image upload

### 2. Subjects (Fanlar)
- Uzbekistan general education subjects
- Topics within each subject
- Tests within topics
- Progress tracking

### 3. Certificates (Sertifikatlar)
- IELTS, TOEFL, SAT preparation
- Topics and tests for each certificate
- Similar structure to Subjects

### 4. Mock Exams
- Full-length practice exams
- DTM-style tests
- Score tracking

### 5. Educational Institutions (Ta'lim Muassasalari)
- Training Centers (O'quv markazlari)
- Schools - State and Private (Maktablar)
- Universities - State, Foreign branches, Private (Oliy ta'lim)

### 6. CMS (Admin Panel)
All content manageable via Django Admin:
- `/admin/` - Admin panel
- Default admin credentials: admin / admin123

## Recent Changes
- **2024-12-01**: Initial project setup
  - Created Django project with MVT architecture
  - Implemented mobile-first responsive design
  - Added user authentication with password recovery
  - Created all core models (Subjects, Tests, Institutions)
  - Set up PostgreSQL database
  - Configured Django Admin as CMS

## Running the Project
```bash
python manage.py runserver 0.0.0.0:5000
```

## Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## User Preferences
- Language: O'zbek (Uzbek)
- Design: Mobile-first, bottom navigation
- Framework: Django MVT
- Database: PostgreSQL
