# 🔔 Browser Native Notification Xususiyati

## Nima Qilindi

Desktop versiya uchun browser native notification (Web Push Notification) qo'shildi.

## ✨ Xususiyatlar

### Browser Native Notifications

- 🔔 Real-time notification'lar
- 🖥️ Desktop notification (Windows, macOS, Linux)
- 📱 Mobile browser notification (Android)
- 🎨 Chiroyli permission prompt
- ⚡ Avtomatik polling (har 30 soniyada)
- 🔕 Foydalanuvchi sozlamalari

### Qo'llab-quvvatlanadigan Brauzerlar

- ✅ Chrome 50+
- ✅ Firefox 44+
- ✅ Edge 14+
- ✅ Safari 16+ (macOS)
- ✅ Opera 37+
- ❌ iOS Safari (qo'llab-quvvatlanmaydi)

## 🔧 Texnik Detalllar

### Frontend (`static/js/notifications.js`)

**NotificationManager Class:**
```javascript
class NotificationManager {
    - checkPermission()      // Permission tekshirish
    - requestPermission()    // Permission so'rash
    - show(options)          // Notification ko'rsatish
    - fetchNotifications()   // Server'dan olish
    - startPolling()         // Avtomatik yangilash
}
```

**Permission Prompt:**
- Chiroyli slide-in animation
- "Yoqish" va "Keyinroq" tugmalari
- 1 kun ichida qayta so'ramaslik

**Polling:**
- Har 30 soniyada yangi notification'larni tekshirish
- Faqat sahifa ko'rinib turganida
- Oxirgi 5 daqiqadagi yangi notification'lar

### Backend (`core/api_views.py`)

**API Endpoints:**

1. **GET `/api/notifications/unread/`**
   - O'qilmagan notification'larni olish
   - Oxirgi 5 daqiqadagi yangi notification'lar
   - Shaxsiy + Global notification'lar

2. **POST `/api/notifications/permission/`**
   - Permission holatini saqlash
   - granted: true/false

3. **POST `/api/notifications/<id>/read/`**
   - Notification'ni o'qilgan deb belgilash

## 📱 Qanday Ishlaydi

### 1. Sahifa Yuklanganda

```
1. NotificationManager init
   ↓
2. Permission tekshirish
   ↓
3. Agar "default":
   → Permission prompt ko'rsatish
   ↓
4. Agar "granted":
   → Polling boshlash
```

### 2. Permission So'rash

```
1. Foydalanuvchi "Yoqish" ni bosadi
   ↓
2. Browser native permission dialog
   ↓
3. Agar "granted":
   → Welcome notification
   → Server'ga xabar berish
   → Polling boshlash
```

### 3. Notification Ko'rsatish

```
1. Polling (har 30 soniya)
   ↓
2. Server'dan yangi notification'lar
   ↓
3. Har biri uchun:
   → Browser native notification
   → 10 soniyadan keyin avtomatik yopilish
   ↓
4. Click event:
   → Sahifaga o'tish
   → Notification yopilish
```

## 🎨 Notification Ko'rinishi

### Desktop (Windows)

```
┌─────────────────────────────────┐
│ 🔔 EduSelf                      │
├─────────────────────────────────┤
│ Yangi Xususiyat!                │
│                                 │
│ EduSelf platformasida yangi     │
│ xususiyatlar qo'shildi...       │
│                                 │
│ [Icon]                          │
└─────────────────────────────────┘
```

### Desktop (macOS)

```
┌─────────────────────────────────┐
│ [Icon] EduSelf                  │
│                                 │
│ Yangi Xususiyat!                │
│ EduSelf platformasida yangi     │
│ xususiyatlar qo'shildi...       │
└─────────────────────────────────┘
```

## 🎯 Foydalanish Stsenariylari

### Stsenariy 1: Birinchi Marta

```
1. Foydalanuvchi saytga kiradi
2. Permission prompt paydo bo'ladi
3. "Yoqish" ni bosadi
4. Browser permission dialog
5. "Allow" ni bosadi
6. Welcome notification keladi
7. Endi barcha notification'lar keladi
```

### Stsenariy 2: Permission Berilgan

```
1. Foydalanuvchi saytga kiradi
2. Polling avtomatik boshlanadi
3. Admin yangi notification yaratadi
4. 30 soniya ichida:
   → Browser notification keladi
5. Foydalanuvchi click qiladi
6. Sahifaga o'tadi
```

### Stsenariy 3: Permission Rad Etilgan

```
1. Foydalanuvchi "Keyinroq" ni bosadi
2. Prompt yopiladi
3. 1 kun ichida qayta so'ralmaydi
4. Notification'lar kelmaydi
```

## 💡 Kod Misollari

### Manual Notification Ko'rsatish

```javascript
// Global funksiya
window.showNotification(
    'Yangi Xabar',
    'Bu test notification',
    'https://eduself.uz'
);
```

### Permission Tekshirish

```javascript
if (Notification.permission === 'granted') {
    console.log('Permission berilgan');
} else if (Notification.permission === 'denied') {
    console.log('Permission rad etilgan');
} else {
    console.log('Permission so\'ralmagan');
}
```

### Custom Notification

```javascript
notificationManager.show({
    title: 'Custom Title',
    body: 'Custom message',
    icon: '/path/to/icon.png',
    badge: '/path/to/badge.png',
    url: 'https://example.com',
    vibrate: [200, 100, 200],
    requireInteraction: true
});
```

## 🔒 Xavfsizlik

### Permission

- Foydalanuvchi ruxsati kerak
- Browser tomonidan boshqariladi
- Har doim rad etish mumkin

### HTTPS

- Faqat HTTPS saytlarda ishlaydi
- Localhost'da ham ishlaydi (development)

### Privacy

- Foydalanuvchi ma'lumotlari saqlanmaydi
- Faqat notification title va message yuboriladi

## 📊 Monitoring

### Browser Console

```javascript
// Permission holati
console.log(Notification.permission);

// Notification manager
console.log(notificationManager);

// Test notification
window.showNotification('Test', 'Bu test', '/');
```

### Server Logs

```python
# core/api_views.py
logger.info(f"Notification fetched: {user.email}")
logger.error(f"Notification error: {e}")
```

## 🧪 Test Qilish

### Manual Test

1. Saytga kiring (desktop browser)
2. Permission prompt paydo bo'lishini kuting
3. "Yoqish" ni bosing
4. Browser permission dialog'da "Allow"
5. Welcome notification kelishini tekshiring
6. Admin panelda yangi notification yarating
7. 30 soniya ichida browser notification kelishini kuting

### Console Test

```javascript
// Browser console'da
window.showNotification(
    'Test Notification',
    'Bu test xabari',
    'https://eduself.uz'
);
```

## 🎨 Customization

### Permission Prompt Dizayni

`static/js/notifications.js` da:

```javascript
const promptHTML = `
    <div id="notification-prompt" style="...">
        <!-- O'z dizayningiz -->
    </div>
`;
```

### Notification Icon

```javascript
const defaultOptions = {
    icon: '/static/icons/icon-192x192.png',  // O'zgartiring
    badge: '/static/icons/icon-96x96.png',   // O'zgartiring
};
```

### Polling Interval

```javascript
setInterval(async () => {
    // ...
}, 30000); // 30 soniya → 60000 (1 daqiqa)
```

## 🚀 Kelajakdagi Yaxshilanishlar

1. **Service Worker**: Offline notification'lar
2. **Push API**: Server-side push
3. **Action Buttons**: Notification'da tugmalar
4. **Rich Notifications**: Rasm, video
5. **Notification History**: Tarix
6. **User Preferences**: Sozlamalar
7. **Sound**: Custom ovozlar
8. **Vibration Patterns**: Custom vibration

## 📞 Yordam

### Notification Kelmayapti

1. **Permission tekshiring**:
   - Browser settings → Notifications
   - Site settings → Permissions

2. **Browser qo'llab-quvvatlashini tekshiring**:
   ```javascript
   console.log('Notification' in window);
   ```

3. **HTTPS tekshiring**:
   - Faqat HTTPS saytlarda ishlaydi
   - Localhost'da ham ishlaydi

4. **Console log'larni ko'ring**:
   - F12 → Console
   - Xatolarni tekshiring

### Permission Qayta So'rash

Agar permission rad etilgan bo'lsa:
1. Browser settings'ga o'ting
2. Site settings → Notifications
3. "Block" dan "Allow" ga o'zgartiring
4. Sahifani yangilang

## 🎓 Foydalanuvchi Uchun

### Notification'larni Yoqish

1. Saytga kiring
2. Pastda o'ng tomonda prompt paydo bo'ladi
3. "Yoqish" tugmasini bosing
4. Browser dialog'da "Allow" ni bosing
5. Tayyor! Endi notification'lar keladi

### Notification'larni O'chirish

1. Browser settings'ga o'ting
2. Privacy → Site settings → Notifications
3. eduself.uz ni toping
4. "Block" ni tanlang

---

**Eslatma**: Browser native notification'lar faqat desktop va Android browser'larda ishlaydi. iOS Safari qo'llab-quvvatlamaydi.
