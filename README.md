# EduSelf Platform

Django-based educational platform with multi-language support.

## Features

- 7-language support (Uzbek, English, Russian, Kazakh, Karakalpak, Tajik, Kyrgyz)
- AI-powered translation using DeepSeek API
- Static translations (425 translations in `static_translations.json`)
- User authentication and profiles
- Course management
- AI assistant for educational recommendations
- Telegram bot integration
- Email notifications

## Language System

- Default language: Uzbek (uz)
- Dynamic content: AI translation with 10-second timeout
- Static content: Pre-translated in `static_translations.json`
- Texts longer than 200 characters: Return original (no AI translation)

## Key Files

- `manage.py` - Django management
- `main.py` - Main application entry
- `run_bot.py` - Telegram bot
- `static_translations.json` - 425 static translations
- `core/translation.py` - AI translation system
- `core/middleware.py` - Language detection
- `core/templatetags/translation_tags.py` - Template filters

## Production Notes

Current fixes applied:
- ✅ API timeout reduced to 10 seconds (prevents worker timeouts)
- ✅ Length check for texts > 200 chars (prevents long API calls)
- ✅ Default language set to Uzbek for all users
- ✅ Session-based language switching for guest users
- ✅ Improved error handling in translation system

## Deployment

Platform deployed on Render.com with automatic deployments from main branch.

After any changes:
```bash
git add .
git commit -m "Your message"
git push origin main
```

Render will automatically detect and deploy changes.
