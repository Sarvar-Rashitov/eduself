#!/usr/bin/env python3
"""
iOS PWA Icon Generator Script
Bu script mavjud icon-192x192.png faylidan iOS uchun kerakli barcha icon o'lchamlarini yaratadi.
"""

import os
from PIL import Image, ImageDraw
import sys

def create_icon(source_path, output_path, size, background_color=None):
    """Icon yaratish funksiyasi"""
    try:
        # Asl rasmni ochish
        with Image.open(source_path) as img:
            # RGBA formatiga o'tkazish
            img = img.convert('RGBA')
            
            # Yangi o'lchamga o'zgartirish (high quality)
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            
            # Agar background color berilgan bo'lsa, uni qo'shish
            if background_color:
                background = Image.new('RGBA', (size, size), background_color)
                # Alpha blending bilan birlashtirish
                final_img = Image.alpha_composite(background, resized)
                # RGB formatiga o'tkazish (PNG uchun)
                final_img = final_img.convert('RGB')
            else:
                final_img = resized
            
            # Saqlash
            final_img.save(output_path, 'PNG', optimize=True)
            print(f"✓ Yaratildi: {output_path} ({size}x{size})")
            return True
            
    except Exception as e:
        print(f"✗ Xatolik {output_path}: {e}")
        return False

def create_splash_screen(source_path, output_path, width, height, background_color='#4F46E5'):
    """Splash screen yaratish funksiyasi"""
    try:
        # Asl rasmni ochish
        with Image.open(source_path) as img:
            img = img.convert('RGBA')
            
            # Background yaratish
            background = Image.new('RGB', (width, height), background_color)
            
            # Icon o'lchamini hisoblash (splash screen uchun kichikroq)
            icon_size = min(width, height) // 4
            icon_resized = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
            
            # Icon'ni markazga joylashtirish
            x = (width - icon_size) // 2
            y = (height - icon_size) // 2
            
            # Icon'ni background ustiga joylashtirish
            if icon_resized.mode == 'RGBA':
                background.paste(icon_resized, (x, y), icon_resized)
            else:
                background.paste(icon_resized, (x, y))
            
            # Saqlash
            background.save(output_path, 'PNG', optimize=True)
            print(f"✓ Splash yaratildi: {output_path} ({width}x{height})")
            return True
            
    except Exception as e:
        print(f"✗ Splash xatolik {output_path}: {e}")
        return False

def main():
    # Asosiy sozlamalar
    source_icon = 'static/icons/icon-192x192.png'
    icons_dir = 'static/icons'
    
    # Source icon mavjudligini tekshirish
    if not os.path.exists(source_icon):
        print(f"✗ Asl icon topilmadi: {source_icon}")
        print("Iltimos, avval icon-192x192.png faylini yarating.")
        return False
    
    # Icons papkasini yaratish
    os.makedirs(icons_dir, exist_ok=True)
    
    print("🚀 iOS PWA iconlarini yaratish boshlandi...")
    print(f"📁 Asl fayl: {source_icon}")
    print(f"📁 Chiqish papkasi: {icons_dir}")
    print("-" * 50)
    
    success_count = 0
    total_count = 0
    
    # Asosiy PWA iconlar
    pwa_sizes = [16, 32, 72, 96, 128, 144, 152, 192, 384, 512]
    
    print("📱 PWA iconlarini yaratish...")
    for size in pwa_sizes:
        output_path = f"{icons_dir}/icon-{size}x{size}.png"
        if create_icon(source_icon, output_path, size):
            success_count += 1
        total_count += 1
    
    # Apple Touch iconlar
    apple_sizes = [57, 60, 72, 76, 114, 120, 144, 152, 180]
    
    print("\n🍎 Apple Touch iconlarini yaratish...")
    for size in apple_sizes:
        output_path = f"{icons_dir}/apple-icon-{size}x{size}.png"
        if create_icon(source_icon, output_path, size):
            success_count += 1
        total_count += 1
    
    # Favicon'lar
    print("\n🌐 Favicon'larni yaratish...")
    favicon_sizes = [(16, 'favicon-16x16.png'), (32, 'favicon-32x32.png')]
    for size, filename in favicon_sizes:
        output_path = f"{icons_dir}/{filename}"
        if create_icon(source_icon, output_path, size):
            success_count += 1
        total_count += 1
    
    # iOS Splash Screen'lar
    splash_screens = [
        (640, 1136, 'splash-640x1136.png'),    # iPhone 5/SE
        (750, 1334, 'splash-750x1334.png'),    # iPhone 6/7/8
        (1242, 2208, 'splash-1242x2208.png'),  # iPhone 6/7/8 Plus
        (1125, 2436, 'splash-1125x2436.png'),  # iPhone X/XS
        (1536, 2048, 'splash-1536x2048.png'),  # iPad
        (1668, 2224, 'splash-1668x2224.png'),  # iPad Pro 10.5"
        (2048, 2732, 'splash-2048x2732.png'),  # iPad Pro 12.9"
    ]
    
    print("\n🎨 iOS Splash Screen'larni yaratish...")
    for width, height, filename in splash_screens:
        output_path = f"{icons_dir}/{filename}"
        if create_splash_screen(source_icon, output_path, width, height):
            success_count += 1
        total_count += 1
    
    # Natijalarni ko'rsatish
    print("\n" + "=" * 50)
    print(f"✅ Yakunlandi: {success_count}/{total_count} fayl muvaffaqiyatli yaratildi")
    
    if success_count == total_count:
        print("🎉 Barcha iconlar muvaffaqiyatli yaratildi!")
        print("\n📋 Keyingi qadamlar:")
        print("1. Barcha iconlar static/icons/ papkasida yaratildi")
        print("2. Web server'ni qayta ishga tushiring")
        print("3. iOS Safari'da saytni oching")
        print("4. 'Bosh ekranga qo'shish' tugmasini bosing")
        print("5. PWA sifatida ishlatishni boshlang!")
    else:
        print(f"⚠️  {total_count - success_count} ta fayl yaratilmadi")
        print("Xatoliklarni tekshiring va qayta urinib ko'ring.")
    
    return success_count == total_count

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Jarayon to'xtatildi")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Kutilmagan xatolik: {e}")
        sys.exit(1)