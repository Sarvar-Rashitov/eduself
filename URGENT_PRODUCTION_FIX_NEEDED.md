# 🚨 URGENT: Production Server Fix Required

## Current Situation
Your production server on Render is experiencing **WORKER TIMEOUT** errors that are causing the site to crash. This is happening because of the oferta page translations.

## What's Causing It
1. The oferta page has long text paragraphs (200-300 characters)
2. When users visit the page in non-Uzbek languages, it tries to translate these texts
3. The AI API calls are taking too long (30+ seconds)
4. Gunicorn workers timeout after 30 seconds and crash
5. This causes 500 errors for users

## What I've Fixed (Locally)

### ✅ 1. Reduced API Timeout
Changed from 30 seconds to 10 seconds in `core/translation.py`

### ✅ 2. Added Safety Checks
Added length checks in `core/templatetags/translation_tags.py` to prevent translating texts longer than 500 characters via API

### ✅ 3. Added Missing Translation
Added the missing oferta translation to `static_translations.json` (now 425 total translations)

### ✅ 4. Better Error Handling
Added try-except blocks to prevent crashes if translation fails

## What You Need to Do NOW

### Step 1: Commit and Push Changes
```bash
git add .
git commit -m "Fix: Prevent worker timeouts from long translation API calls"
git push origin main
```

### Step 2: Wait for Render to Deploy
- Render will automatically detect the changes and redeploy
- This usually takes 2-5 minutes
- Watch the deploy logs on Render dashboard

### Step 3: Verify the Fix
After deployment, check:
1. Visit your site homepage - should load without errors
2. Visit `/oferta/` page - should load
3. Try switching languages - should work
4. Check Render logs - should see "✅ Loaded 425 static translations"

## Files Changed

1. ✅ `core/translation.py` - Reduced timeout
2. ✅ `core/templatetags/translation_tags.py` - Added safety checks
3. ✅ `static_translations.json` - Added missing translation (425 total)
4. ✅ `TRANSLATION_TIMEOUT_FIX.md` - Documentation
5. ✅ `add_missing_oferta_translation.py` - Script used

## Expected Results After Fix

### Before (Current - BAD):
```
[CRITICAL] WORKER TIMEOUT (pid:74)
SystemExit: 1
Worker exiting
```

### After (Expected - GOOD):
```
✅ Loaded 425 static translations from /path/to/static_translations.json
200 OK - Page loaded successfully
No worker timeouts
```

## If Still Having Issues

If the problem persists after deployment:

### Option A: Temporary Disable AI Translation for Oferta
Add this to `templates/core/oferta_mobile.html`:
```django
{% if request.LANGUAGE_CODE == 'uz' %}
    {# Show oferta content #}
{% else %}
    <p>This page is only available in Uzbek at the moment.</p>
{% endif %}
```

### Option B: Pre-translate Everything
Run a script to pre-translate all oferta texts and add them to static_translations.json

### Option C: Increase Worker Timeout (Not Recommended)
In Render dashboard, add environment variable:
```
GUNICORN_TIMEOUT=60
```

## Monitoring

After deployment, monitor these metrics:
- ✅ Response times < 2 seconds
- ✅ No 500 errors
- ✅ No worker timeout messages in logs
- ✅ All pages loading correctly

## Priority: CRITICAL

This is blocking your production site. Users are seeing 500 errors. Deploy the fix ASAP.

---

**Status:** Ready to deploy
**Action Required:** Commit and push to trigger Render deployment
**ETA:** 5 minutes after push
**Risk:** Low (changes are defensive and safe)

