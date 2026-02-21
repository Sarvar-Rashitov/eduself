# Browser Notifications - Quick Start Guide

## What is it?

Browser native notifications allow desktop users to receive real-time notifications directly on their desktop, even when the browser tab is in the background.

## How to Test

### 1. Start the Server
```bash
python manage.py runserver
```

### 2. Open in Desktop Browser
- Chrome, Firefox, or Edge recommended
- Must be desktop (not mobile)
- Open: http://127.0.0.1:8000

### 3. Enable Notifications
- A prompt will appear in the bottom-right corner
- Click "Yoqish" (Enable)
- Browser will ask for permission - click "Allow"
- You'll see a welcome notification

### 4. Test with Admin Panel
- Go to: http://127.0.0.1:8000/nokia/
- Navigate to: Core > Notifications
- Click "Add Notification"
- Fill in:
  - Title: "Test Notification"
  - Message: "This is a test"
  - Type: Info
  - Icon: bi bi-bell-fill
- Save

### 5. Wait for Notification
- Within 30 seconds, you should see a browser notification
- Click on it to navigate to the link (if provided)

## How it Works

```
User opens site
    ↓
Permission prompt appears
    ↓
User clicks "Yoqish"
    ↓
Browser asks for permission
    ↓
User clicks "Allow"
    ↓
Polling starts (every 30 seconds)
    ↓
Admin creates notification
    ↓
Within 30 seconds:
    → Browser notification appears
    → Auto-closes after 10 seconds
    → Click to navigate
```

## Features

✅ Auto-polling every 30 seconds
✅ Only fetches recent notifications (last 5 minutes)
✅ Beautiful Uzbek UI for permission prompt
✅ Welcome notification on first enable
✅ Click to navigate to notification link
✅ Auto-close after 10 seconds
✅ Only works when page is visible
✅ Graceful fallback if not supported

## Troubleshooting

### Notifications not appearing?

1. **Check browser support**
   - Open console (F12)
   - Type: `'Notification' in window`
   - Should return: `true`

2. **Check permission**
   - Open console (F12)
   - Type: `Notification.permission`
   - Should return: `"granted"`

3. **Check if polling is working**
   - Open console (F12)
   - Look for: "✅ Notification permission berilgan"
   - Should appear when page loads

4. **Test manually**
   - Open console (F12)
   - Type: `window.showNotification('Test', 'This is a test', '/')`
   - Should show a notification immediately

### Permission denied?

If you accidentally clicked "Block":
1. Click the lock icon in the address bar
2. Find "Notifications"
3. Change from "Block" to "Allow"
4. Refresh the page

### Still not working?

1. Clear browser cache and cookies
2. Try in incognito/private mode
3. Check if notifications are enabled in OS settings
4. Try a different browser

## API Endpoints

### Get Unread Notifications
```
GET /api/notifications/unread/
```

Returns notifications from the last 5 minutes that are unread.

### Save Permission Status
```
POST /api/notifications/permission/
Body: {"granted": true}
```

Saves the user's notification permission preference.

### Mark as Read
```
POST /api/notifications/<id>/read/
```

Marks a notification as read.

## Browser Support

| Browser | Desktop | Mobile |
|---------|---------|--------|
| Chrome  | ✅      | ❌     |
| Firefox | ✅      | ❌     |
| Edge    | ✅      | ❌     |
| Safari  | ✅      | ❌     |
| iOS Safari | ❌   | ❌     |

**Note**: Mobile browsers are intentionally not supported. This is a desktop-only feature.

## Production Deployment

### Requirements
- HTTPS is required in production
- Localhost works for development
- Valid SSL certificate needed

### Checklist
- [ ] Deploy code to production
- [ ] Ensure HTTPS is enabled
- [ ] Test on production domain
- [ ] Monitor browser console for errors
- [ ] Check notification delivery rates

## Advanced Usage

### Manual Notification
```javascript
window.showNotification(
    'Title',
    'Message body',
    'https://example.com'
);
```

### Check Permission
```javascript
if (Notification.permission === 'granted') {
    console.log('Notifications enabled');
}
```

### Custom Notification
```javascript
notificationManager.show({
    title: 'Custom Title',
    body: 'Custom message',
    icon: '/path/to/icon.png',
    url: 'https://example.com',
    vibrate: [200, 100, 200]
});
```

## Files

- `static/js/notifications.js` - Main notification manager
- `core/api_views.py` - API endpoints
- `core/urls.py` - URL routing
- `templates/base.html` - Script inclusion
- `BROWSER_NOTIFICATIONS_FEATURE.md` - Full documentation

## Support

For issues or questions:
1. Check the full documentation: `BROWSER_NOTIFICATIONS_FEATURE.md`
2. Run the test script: `python test_browser_notifications.py`
3. Check browser console for errors (F12)
4. Verify API endpoints are working

---

**Last Updated**: February 2026
**Status**: ✅ Production Ready
