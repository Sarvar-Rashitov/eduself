# Push Notification Test Ko'rsatmalari

## 1. Serverni Ishga Tushirish

```bash
python manage.py runserver
```

## 2. Browser'ni Ochish

Desktop browser'da oching (Chrome, Firefox, yoki Edge):
```
http://127.0.0.1:8000
```

## 3. Browser Console'ni Ochish

- **Windows/Linux**: F12 yoki Ctrl+Shift+I
- **Mac**: Cmd+Option+I

"Console" tab'ini tanlang.

## 4. Console Log'larni Kuzatish

Sahifa yuklanganda quyidagi xabarlar ko'rinishi kerak:

```
🚀 DOM yuklandi, NotificationManager yaratilmoqda...
🔔 NotificationManager init() boshlandi
✅ Browser notification qo'llab-quvvatlaydi
📊 Permission holati: default (yoki granted/denied)
🔍 checkPermission() chaqirildi, holat: default
⚠️ Permission hali so'ralmagan, prompt ko'rsatiladi
🔄 Polling boshlandi (har 30 soniyada)
✅ Polling interval o'rnatildi
✅ NotificationManager init() tugadi
✅ NotificationManager yaratildi: NotificationManager {...}
✅ window.showNotification() global funksiya o'rnatildi
```

## 5. Permission Berish

Agar permission prompt ko'rinsa:
1. Pastda o'ng tomonda prompt paydo bo'ladi
2. "Yoqish" tugmasini bosing
3. Browser dialog'da "Allow" ni bosing

Console'da ko'rinishi kerak:
```
✅ Notification permission berildi
🎉 Bildirishnomalar yoqildi!
📢 Notification ko'rsatilmoqda: 🎉 Bildirishnomalar yoqildi!
✅ Notification yaratildi: 🎉 Bildirishnomalar yoqildi!
```

## 6. Manual Test

Console'da quyidagi buyruqni yozing:

```javascript
window.showNotification('Test', 'Bu test xabari', '/')
```

Ko'rinishi kerak:
```
🌐 window.showNotification() chaqirildi
📢 show() chaqirildi: Test
✅ Notification yaratildi: Test
```

Va desktop'da notification paydo bo'lishi kerak!

## 7. Admin Paneldan Test

1. Yangi tab ochib admin panelga kiring:
   ```
   http://127.0.0.1:8000/nokia/
   ```

2. Core > Notifications > Add Notification

3. Ma'lumotlarni kiriting:
   - Title: "Test Notification"
   - Message: "Bu admin paneldan yuborilgan test"
   - Type: info
   - Icon: bi bi-bell-fill

4. Save

5. Birinchi tab'ga qayting (asosiy sahifa)

6. Console'ni kuzating, 30 soniya ichida:
   ```
   🔄 Polling: yangi notification'lar tekshirilmoqda...
   ✅ Permission granted va sahifa visible
   📡 fetchNotifications() chaqirildi
   📡 API response status: 200
   📡 API response data: {success: true, notifications: [...], count: 1}
   📥 Olingan notification'lar: 1
   📢 Notification ko'rsatilmoqda: Test Notification
   📢 show() chaqirildi: Test Notification
   ✅ Notification yaratildi: Test Notification
   ```

7. Desktop'da notification ko'rinishi kerak!

## Muammolarni Hal Qilish

### Agar console'da xato ko'rsatsa:

#### Xato: "Browser notification qo'llab-quvvatlanmaydi"
- Boshqa browser'da sinab ko'ring (Chrome tavsiya etiladi)
- Browser versiyasini yangilang

#### Xato: "Permission rad etilgan"
1. Address bar'dagi lock icon'ni bosing
2. Notifications > Allow
3. Sahifani yangilang (F5)

#### Xato: "API response status: 403" yoki "401"
- Login qilganingizni tekshiring
- Sahifani yangilang va qayta login qiling

#### Xato: "API response status: 404"
- URL to'g'ri ekanligini tekshiring
- `core/urls.py` da route mavjudligini tekshiring

#### Xato: "fetchNotifications() chaqirilmayapti"
- Permission "granted" ekanligini tekshiring
- Sahifa visible (active tab) ekanligini tekshiring
- 30 soniya kuting

### Agar notification ko'rinmasa:

1. **Permission tekshiring:**
   ```javascript
   Notification.permission
   ```
   "granted" bo'lishi kerak

2. **Manual test qiling:**
   ```javascript
   window.showNotification('Test', 'Test', '/')
   ```

3. **API test qiling:**
   ```javascript
   fetch('/api/notifications/unread/', {
       headers: {'X-Requested-With': 'XMLHttpRequest'}
   }).then(r => r.json()).then(console.log)
   ```

4. **Notification yangi ekanligini tekshiring:**
   - Faqat oxirgi 5 daqiqadagi notification'lar ko'rsatiladi
   - Yangi notification yarating

5. **OS notification settings'ni tekshiring:**
   - Windows: Settings > System > Notifications
   - Mac: System Preferences > Notifications
   - Browser uchun notification'lar yoqilgan bo'lishi kerak

## Muvaffaqiyatli Test

Agar hammasi to'g'ri ishlasa:

1. ✅ Console'da barcha log'lar ko'rinadi
2. ✅ Permission prompt paydo bo'ladi
3. ✅ Manual test ishlaydi
4. ✅ Admin paneldan notification keladi
5. ✅ Desktop'da notification ko'rinadi
6. ✅ Notification'ga click qilish ishlaydi

## Qo'shimcha Debug

Agar hali ham ishlamasa, quyidagi ma'lumotlarni yuboring:

1. Browser versiyasi:
   ```javascript
   navigator.userAgent
   ```

2. Barcha console log'lar (screenshot)

3. Network tab'dagi `/api/notifications/unread/` so'rovi (screenshot)

4. Django terminal'dagi xatolar (agar bor bo'lsa)
