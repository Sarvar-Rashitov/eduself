# Telegram Bot Yangilanishlari

## Qo'shilgan Funksiyalar

### 1. Lives System (Yurakchalar Tizimi)

Telegram botga to'liq lives system qo'shildi:

- **Test boshlashda tekshiruv**: Foydalanuvchi test boshlashdan oldin yurakchalar mavjudligi tekshiriladi
- **Test muvaffaqiyatsiz bo'lganda**: Agar test o'tish ballidan past bo'lsa, 1 yurakcha yo'qotiladi
- **Yurakchalar tugaganda**: Foydalanuvchiga Pro obuna taklif qilinadi
- **Profilida ko'rsatish**: Foydalanuvchi profilida yurakchalar holati ko'rsatiladi
- **Pro foydalanuvchilar**: Cheksiz yurakchalar

### 2. Pro Obuna Tizimi

Telegram botga to'liq obuna tizimi qo'shildi:

- **Obuna ma'lumotlari**: Profilida faol obuna ko'rsatiladi
- **Obuna tariflari**: Yangi `/subscription_plans` handler orqali tariflar ko'rsatiladi
- **Saytga yo'naltirish**: Obuna sotib olish uchun saytga havola
- **Pro imkoniyatlar**:
  - ♾️ Cheksiz yurakchalar
  - 🔓 Barcha mavzular ochiq
  - 🤖 AI tahlil va hamroh
  - 🏆 Universitet imtihonlari
  - 📝 Mock imtihonlar
  - 🎓 Sertifikat testlari

### 3. Mavzular Progressiv Ochilishi

Fanlar bo'limida mavzular progressiv ochilish tizimi qo'shildi:

- **Birinchi mavzu**: Har doim ochiq
- **Keyingi mavzular**: Oldingi mavzudan o'tish ballidan yuqori ball olish kerak
- **Pro foydalanuvchilar**: Barcha mavzular ochiq
- **Vizual ko'rsatish**: 
  - ✅ Ochiq mavzular
  - 🔒 Yopiq mavzular
- **Yopiq mavzuga kirganda**: Pro obuna taklif qilinadi

## O'zgartirilgan Fayllar

### 1. `core/models.py`
- `Topic` modeliga `is_unlocked_for_user()` metodi qo'shildi
- Mavzu ochilganligini tekshirish logikasi

### 2. `telegram_bot/handlers/subjects.py`
- `get_topics()` funksiyasi yangilandi - unlock holati qo'shildi
- `subject_detail()` funksiyasi yangilandi - user parametri qo'shildi
- `topic_detail()` funksiyasi yangilandi - unlock tekshiruvi qo'shildi
- `check_topic_unlocked()` yangi funksiya

### 3. `telegram_bot/handlers/profile.py`
- `get_user_subscription_info()` yangi funksiya
- `profile_menu()` yangilandi - obuna va lives ma'lumotlari qo'shildi
- Profilida yurakchalar va obuna holati ko'rsatiladi

### 4. `telegram_bot/handlers/subscription.py` (YANGI)
- Yangi handler yaratildi
- `subscription_plans()` funksiyasi - obuna tariflari
- Saytga yo'naltirish

### 5. `telegram_bot/handlers/tests.py`
- `check_user_lives()` yangi funksiya
- `lose_user_life()` yangi funksiya
- `get_user_lives_info()` yangi funksiya
- `start_topic_test()` yangilandi - lives tekshiruvi qo'shildi
- `finish_topic_from_callback()` yangilandi - test muvaffaqiyatsiz bo'lganda yurakcha yo'qotish

### 6. `telegram_bot/keyboards.py`
- `topics_keyboard()` yangilandi - unlock holati qo'shildi
- `profile_keyboard()` yangilandi - Pro obuna tugmasi qo'shildi

### 7. `telegram_bot/bot.py`
- `subscription_handlers` import va register qo'shildi

## Foydalanish

### Foydalanuvchi uchun:

1. **Fanlar bo'limida**:
   - Birinchi mavzu har doim ochiq
   - Keyingi mavzular oldingi mavzudan o'tgandan keyin ochiladi
   - 🔒 belgisi yopiq mavzularni ko'rsatadi

2. **Test yechishda**:
   - Har bir test uchun yurakcha kerak
   - Test muvaffaqiyatsiz bo'lsa, 1 yurakcha yo'qotiladi
   - Yurakchalar tugasa, Pro obuna taklif qilinadi

3. **Profilida**:
   - Yurakchalar holati ko'rsatiladi
   - Faol obuna ma'lumotlari ko'rsatiladi
   - Pro obuna tugmasi (agar obuna bo'lmasa)

4. **Pro obuna**:
   - Cheksiz yurakchalar
   - Barcha mavzular ochiq
   - Qo'shimcha imkoniyatlar

## Texnik Ma'lumotlar

- Barcha funksiyalar `@sync_to_async` decorator bilan async qilingan
- Lives tizimi `accounts.models.User` modelidagi metodlardan foydalanadi
- Obuna tizimi `subscriptions.models` dan foydalanadi
- Mavzu ochilish logikasi `core.models.Topic.is_unlocked_for_user()` metodida

## Test Qilish

1. Botni ishga tushiring: `python telegram_bot/bot.py`
2. Telegram botda `/start` buyrug'ini yuboring
3. "📚 Fanlar" tugmasini bosing
4. Fanni tanlang va mavzular ro'yxatini ko'ring
5. Birinchi mavzuni yeching
6. Ikkinchi mavzu ochilganligini tekshiring
7. Profilga o'ting va yurakchalar holatini ko'ring
8. Test muvaffaqiyatsiz bo'lsa, yurakcha yo'qotilishini tekshiring

## Kelajakda Qo'shilishi Mumkin

- Yurakchalar to'ldirilish vaqtini real-time ko'rsatish
- Obunani bot orqali sotib olish (Click/Payme integratsiyasi)
- Yurakchalarni do'stlarga yuborish
- Yurakchalar uchun reklama ko'rish
