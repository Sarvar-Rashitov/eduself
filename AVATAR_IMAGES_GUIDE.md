# Avatar Rasmlari Qo'llanmasi

## Joylashuv
Avatar rasmlari `static/images/avatars/` papkasida joylashgan.

## Kerakli Rasmlar
Jami 8 ta avatar rasmi kerak:
- `avatar-1.png`
- `avatar-2.png`
- `avatar-3.png`
- `avatar-4.png`
- `avatar-5.png`
- `avatar-6.png`
- `avatar-7.png`
- `avatar-8.png`

## Rasm Talablari
- **Format**: PNG (shaffof fon bilan)
- **O'lcham**: 200x200 px yoki 400x400 px (yuqori sifat uchun)
- **Stil**: Rasmdagi kabi illustratsiya avatarlari
- **Xilma-xillik**: Turli xil yuz, soch, kiyim ranglari

## Avatar Rasmlarini Qayerdan Olish Mumkin

### 1. Bepul Avatar Generatorlar
- **DiceBear Avatars**: https://www.dicebear.com/
  - Avataaars, Bottts, Personas va boshqa stillar
  - PNG formatda yuklab olish mumkin
  
- **Boring Avatars**: https://boringavatars.com/
  - Oddiy va zamonaviy dizayn
  
- **Avatar Maker**: https://avatarmaker.com/
  - O'zingiz yaratishingiz mumkin

### 2. Bepul Illustratsiya Kutubxonalari
- **unDraw**: https://undraw.co/illustrations
- **Humaaans**: https://www.humaaans.com/
- **Open Peeps**: https://www.openpeeps.com/

### 3. Figma/Sketch Resurslar
- Figma Community'da "avatar" qidirib topishingiz mumkin
- Ko'plab bepul avatar to'plamlari mavjud

## Rasmlarni Qo'shish

1. Avatar rasmlarini yuklab oling (PNG format)
2. Rasmlarni `static/images/avatars/` papkasiga joylashtiring
3. Rasmlarni `avatar-1.png` dan `avatar-8.png` gacha nomlang
4. Static fayllarni yig'ing:
   ```bash
   python manage.py collectstatic --noinput
   ```

## Hozirgi Holat

Hozirda `static/images/avatars/` papkasi yaratilgan, lekin rasmlar yo'q.
Siz yuqoridagi manbalardan avatar rasmlarini yuklab, papkaga joylashtiring.

## Vaqtinchalik Yechim

Agar hozir rasmlar bo'lmasa, UI Avatars API dan foydalanish mumkin.
User modelida `get_avatar_url()` metodini o'zgartiring:

```python
def get_avatar_url(self):
    if self.profile_image:
        return self.profile_image.url
    
    # Vaqtinchalik: UI Avatars API
    name = self.get_display_name()
    colors = ['6366f1', '8b5cf6', 'ec4899', 'f59e0b', '10b981', '3b82f6', 'ef4444', '14b8a6']
    color = colors[self.avatar_number % len(colors)]
    return f"https://ui-avatars.com/api/?name={name}&background={color}&color=fff&size=200&bold=true"
```

## Foydalanuvchi Avatar Tanlashi

Kelajakda foydalanuvchilarga o'zlari avatar tanlash imkoniyatini qo'shish mumkin:
1. Profile edit sahifasida 8 ta avatarni ko'rsatish
2. Foydalanuvchi birini tanlaydi
3. `avatar_number` maydoni yangilanadi
