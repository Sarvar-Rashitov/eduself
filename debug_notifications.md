# Browser Notification Debug Guide

## Muammoni Aniqlash

### 1. Browser Console'ni Tekshirish

1. Saytni oching (http://127.0.0.1:8000)
2. F12 ni bosing (Developer Tools)
3. "Console" tab'ini oching
4. Quyidagi xabarlarni qidiring:

**Kutilayotgan xabarlar:**
```
✅ Notification permission berilgan
```
yoki
```
⚠️ Browser notification qo'llab-quvvatlanmaydi
```

### 2. Permission Holatini Tekshirish

Console'da quyidagi buyruqni yozing:
```javascript
Notification.permission
```

**Natijalar:**
- `"granted"` - Permission berilgan ✅
- `"denied"` - Permission rad etilgan ❌
- `"default"` - Hali so'ralmagan ⚠️

### 3. Browser Qo'llab-quvvatlashini Tekshirish

Console'da:
```javascript
'Notification' in window
```

Agar `false` bo'lsa, browser qo'llab-quvvatlamaydi.

### 4. Manual Test

Console'da:
```javascript
window.showNotification('Test', 'Bu test xabari', '/')
```

Agar bu ishlasa, polling muammosi.
Agar ishlamasa, permission muammosi.

### 5. Network Tab'ni Tekshirish

1. F12 > Network tab
2. Sahifani yangilang
3. Quyidagi so'rovlarni qidiring:
   - `/api/notifications/unread/`
   
Agar so'rov yo'q bo'lsa, polling ishlamayapti.
Agar 403/401 xato bo'lsa, authentication muammosi.

### 6. Notification Yaratish

Admin panelda notification yarating:
1. http://127.0.0.1:8000/nokia/
2. Core > Notifications > Add
3. Title: "Test"
4. Message: "Test message"
5. Save

Keyin 30 soniya kuting.

## Keng Tarqalgan Muammolar

### Muammo 1: Permission Prompt Ko'rinmaydi

**Sabab:** localStorage'da dismissed flag bor

**Yechim:**
```javascript
// Console'da
localStorage.removeItem('notification-prompt-dismissed');
location.reload();
```

### Muammo 2: Permission "denied"

**Yechim:**
1. Address bar'dagi lock icon'ni bosing
2. Notifications > Allow
3. Sahifani yangilang

### Muammo 3: Notification Eski

**Sabab:** Faqat oxirgi 5 daqiqadagi notification'lar ko'rsatiladi

**Yechim:** Yangi notification yarating

### Muammo 4: Polling Ishlamayapti

**Tekshirish:**
```javascript
// Console'da
notificationManager
```

Agar `undefined` bo'lsa, script yuklanmagan.

**Yechim:** Sahifani yangilang (Ctrl+F5)

### Muammo 5: API Xatosi

**Tekshirish:** Network tab'da 500 xato

**Yechim:** Django logs'ni tekshiring:
```bash
python manage.py runserver
```

Terminal'da xatolarni ko'ring.

## Qadam-ba-Qadam Debug

### Qadam 1: Browser Qo'llab-quvvatlashini Tekshirish
```javascript
console.log('Notification support:', 'Notification' in window);
console.log('Permission:', Notification.permission);
```

### Qadam 2: NotificationManager Mavjudligini Tekshirish
```javascript
console.log('NotificationManager:', typeof notificationManager);
```

### Qadam 3: Manual Notification Test
```javascript
if (Notification.permission === 'granted') {
    new Notification('Test', {
        body: 'Bu test',
        icon: '/static/icons/icon-192x192.png'
    });
}
```

### Qadam 4: API Test
```javascript
fetch('/api/notifications/unread/', {
    headers: {
        'X-Requested-With': 'XMLHttpRequest'
    }
})
.then(r => r.json())
.then(data => console.log('API response:', data));
```

### Qadam 5: Polling Test
```javascript
// 30 soniya kuting va console'ni kuzating
// Har 30 soniyada so'rov bo'lishi kerak
```

## Tez Yechim

Agar hech narsa ishlamasa:

1. **Browser cache'ni tozalash:**
   - Ctrl+Shift+Delete
   - "Cached images and files" ni tanlang
   - Clear

2. **Hard refresh:**
   - Ctrl+F5 (Windows)
   - Cmd+Shift+R (Mac)

3. **Incognito mode'da test qiling:**
   - Ctrl+Shift+N (Chrome)
   - Ctrl+Shift+P (Firefox)

4. **Boshqa browser'da test qiling:**
   - Chrome
   - Firefox
   - Edge

## Xatolarni Yig'ish

Agar muammo davom etsa, quyidagi ma'lumotlarni yuboring:

1. **Browser ma'lumoti:**
```javascript
console.log('Browser:', navigator.userAgent);
```

2. **Permission holati:**
```javascript
console.log('Permission:', Notification.permission);
```

3. **Console xatolari:**
   - F12 > Console
   - Barcha qizil xatolarni screenshot qiling

4. **Network xatolari:**
   - F12 > Network
   - Failed so'rovlarni screenshot qiling

5. **Django logs:**
   - Terminal'dagi xatolarni copy qiling
