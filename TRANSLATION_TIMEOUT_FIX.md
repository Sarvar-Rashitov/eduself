# Translation Timeout Fix 🔧

## Problem
The production server is experiencing worker timeouts due to long AI translation API calls. Workers are crashing with `WORKER TIMEOUT` errors.

## Root Cause
1. Long oferta body texts (200-300 characters) are causing API calls to timeout
2. Some translations are missing from `static_translations.json`
3. The `t` template tag falls back to AI translation when static translation not found
4. API timeout was set to 30 seconds (too long for Gunicorn's 30-second worker timeout)

## Solutions Implemented

### 1. Reduced API Timeout
**File:** `core/translation.py`
```python
# Changed from timeout=30 to timeout=10
response = requests.post(
    self.api_url,
    headers=headers,
    json=data,
    timeout=10  # Reduced to prevent worker timeouts
)
```

### 2. Added Length Check in Template Tags
**File:** `core/templatetags/translation_tags.py`

Added protection against translating very long texts:
```python
# In both trans() and t() functions:
if len(text) > 500:
    print(f"⚠️ Text too long for AI translation ({len(text)} chars), returning original")
    return text
```

### 3. Improved Static Translation Loading
**File:** `core/templatetags/translation_tags.py`

Added multiple path attempts and logging:
```python
possible_paths = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'static_translations.json'),
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static_translations.json'),
    'static_translations.json',
]

for translations_file in possible_paths:
    if os.path.exists(translations_file):
        with open(translations_file, 'r', encoding='utf-8') as f:
            STATIC_TRANSLATIONS = json.load(f)
        print(f"✅ Loaded {len(STATIC_TRANSLATIONS)} static translations")
        break
```

### 4. Added Error Handling
Both `trans()` and `t()` functions now have try-except blocks to prevent crashes:
```python
try:
    return translator.translate(text, 'uz', target_lang)
except Exception as e:
    print(f"❌ Translation error: {e}")
    return text
```

## Missing Translation Found

One oferta translation key was missing:
```
"Ushbu hujjat EduSelf platformasidan foydalanish shartlarini belgilaydi"
```

This needs to be added to `static_translations.json`.

## Deployment Steps

1. **Add missing translation** (see script below)
2. **Commit changes** to git
3. **Deploy to production** (Render will auto-deploy)
4. **Monitor logs** for:
   - "✅ Loaded X static translations" message
   - No more worker timeout errors
   - Successful page loads

## Quick Fix Script

Run this to add the missing translation:

```python
python add_missing_oferta_translation.py
```

## Testing

After deployment, test:
1. Visit oferta page: `/oferta/`
2. Switch languages using language selector
3. Verify all text translates without timeouts
4. Check server logs for no worker timeout errors

## Monitoring

Watch for these log messages:
- ✅ `Loaded 425 static translations` (should be 425 after fix)
- ⚠️ `Text too long for AI translation` (if any texts > 500 chars)
- ❌ `Translation error` (if API fails)
- 🚫 `WORKER TIMEOUT` (should NOT appear anymore)

## Alternative Solution (If Still Failing)

If timeouts persist, consider:
1. Pre-translate all oferta texts and add to static_translations.json
2. Disable AI fallback for static pages (oferta, privacy)
3. Use async translation with Celery for long texts
4. Increase Gunicorn worker timeout (not recommended)

## Files Modified

1. `core/translation.py` - Reduced timeout to 10s
2. `core/templatetags/translation_tags.py` - Added length check and better error handling
3. `static_translations.json` - Need to add 1 missing translation

## Status

- ✅ Local changes made
- ⏳ Waiting for deployment
- ⏳ Need to add missing translation
- ⏳ Need to test on production

---

**Created:** February 23, 2026
**Priority:** CRITICAL - Blocking production
