#!/usr/bin/env python3
"""
iOS PWA Test Script
Bu script iOS PWA sozlamalarini tekshiradi va test qiladi.
"""

import os
import json
import requests
from urllib.parse import urljoin

def check_file_exists(filepath):
    """Fayl mavjudligini tekshirish"""
    exists = os.path.exists(filepath)
    print(f"{'✓' if exists else '✗'} {filepath}")
    return exists

def check_manifest():
    """Manifest faylini tekshirish"""
    print("\n📋 Manifest.json tekshiruvi:")
    manifest_path = 'static/manifest.json'
    
    if not check_file_exists(manifest_path):
        return False
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # Kerakli maydonlarni tekshirish
        required_fields = ['name', 'short_name', 'start_url', 'display', 'theme_color', 'background_color', 'icons']
        
        for field in required_fields:
            if field in manifest:
                print(f"✓ {field}: {manifest[field] if field != 'icons' else f'{len(manifest[field])} ta icon'}")
            else:
                print(f"✗ {field}: mavjud emas")
        
        # Icon'larni tekshirish
        if 'icons' in manifest:
            print(f"\n📱 Icon'lar ({len(manifest['icons'])} ta):")
            for icon in manifest['icons']:
                icon_path = icon['src'].lstrip('/')
                exists = os.path.exists(icon_path)
                print(f"{'✓' if exists else '✗'} {icon['sizes']} - {icon_path}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"✗ JSON xatolik: {e}")
        return False
    except Exception as e:
        print(f"✗ Xatolik: {e}")
        return False

def check_service_worker():
    """Service Worker faylini tekshirish"""
    print("\n⚙️ Service Worker tekshiruvi:")
    sw_path = 'static/sw.js'
    
    if not check_file_exists(sw_path):
        return False
    
    try:
        with open(sw_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Kerakli funksiyalarni tekshirish
        required_features = [
            ('install', 'install event listener'),
            ('activate', 'activate event listener'),
            ('fetch', 'fetch event listener'),
            ('caches.open', 'cache API usage'),
            ('skipWaiting', 'skipWaiting call'),
            ('clients.claim', 'clients.claim call')
        ]
        
        for feature, description in required_features:
            if feature in content:
                print(f"✓ {description}")
            else:
                print(f"✗ {description}")
        
        return True
        
    except Exception as e:
        print(f"✗ Xatolik: {e}")
        return False

def check_icons():
    """Icon fayllarini tekshirish"""
    print("\n🎨 Icon fayllar tekshiruvi:")
    
    # PWA iconlar
    pwa_sizes = [16, 32, 72, 96, 128, 144, 152, 192, 384, 512]
    apple_sizes = [57, 60, 72, 76, 114, 120, 144, 152, 180]
    
    pwa_count = 0
    apple_count = 0
    
    print("PWA Icon'lar:")
    for size in pwa_sizes:
        path = f"static/icons/icon-{size}x{size}.png"
        if check_file_exists(path):
            pwa_count += 1
    
    print(f"\nApple Touch Icon'lar:")
    for size in apple_sizes:
        path = f"static/icons/apple-icon-{size}x{size}.png"
        if check_file_exists(path):
            apple_count += 1
    
    # Splash screen'lar
    splash_screens = [
        'splash-640x1136.png',
        'splash-750x1334.png', 
        'splash-1242x2208.png',
        'splash-1125x2436.png',
        'splash-1536x2048.png',
        'splash-1668x2224.png',
        'splash-2048x2732.png'
    ]
    
    splash_count = 0
    print(f"\niOS Splash Screen'lar:")
    for splash in splash_screens:
        path = f"static/icons/{splash}"
        if check_file_exists(path):
            splash_count += 1
    
    print(f"\n📊 Natija:")
    print(f"PWA Icon'lar: {pwa_count}/{len(pwa_sizes)}")
    print(f"Apple Touch Icon'lar: {apple_count}/{len(apple_sizes)}")
    print(f"Splash Screen'lar: {splash_count}/{len(splash_screens)}")
    
    return pwa_count > 0 and apple_count > 0

def check_html_meta_tags():
    """HTML meta tag'larini tekshirish"""
    print("\n🏷️ HTML Meta Tag'lar tekshiruvi:")
    
    template_path = 'templates/base.html'
    if not check_file_exists(template_path):
        return False
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # iOS PWA uchun kerakli meta tag'lar
        required_meta_tags = [
            ('apple-mobile-web-app-capable', 'iOS PWA qo\'llab-quvvatlash'),
            ('apple-mobile-web-app-status-bar-style', 'iOS status bar style'),
            ('apple-mobile-web-app-title', 'iOS app nomi'),
            ('theme-color', 'Theme color'),
            ('viewport', 'Viewport sozlamalari'),
            ('manifest', 'Manifest link'),
            ('apple-touch-icon', 'Apple touch icon')
        ]
        
        for tag, description in required_meta_tags:
            if tag in content:
                print(f"✓ {description}")
            else:
                print(f"✗ {description}")
        
        return True
        
    except Exception as e:
        print(f"✗ Xatolik: {e}")
        return False

def test_pwa_score():
    """PWA score'ni baholash"""
    print("\n🏆 PWA Baholash:")
    
    score = 0
    max_score = 5
    
    # Manifest
    if os.path.exists('static/manifest.json'):
        score += 1
        print("✓ Manifest mavjud (+1)")
    else:
        print("✗ Manifest yo'q")
    
    # Service Worker
    if os.path.exists('static/sw.js'):
        score += 1
        print("✓ Service Worker mavjud (+1)")
    else:
        print("✗ Service Worker yo'q")
    
    # Icon'lar
    if os.path.exists('static/icons/icon-192x192.png') and os.path.exists('static/icons/icon-512x512.png'):
        score += 1
        print("✓ Asosiy icon'lar mavjud (+1)")
    else:
        print("✗ Asosiy icon'lar yo'q")
    
    # Apple Touch Icon'lar
    if os.path.exists('static/icons/apple-icon-180x180.png'):
        score += 1
        print("✓ Apple Touch Icon mavjud (+1)")
    else:
        print("✗ Apple Touch Icon yo'q")
    
    # HTML meta tag'lar
    if os.path.exists('templates/base.html'):
        with open('templates/base.html', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'apple-mobile-web-app-capable' in content:
                score += 1
                print("✓ iOS PWA meta tag'lar mavjud (+1)")
            else:
                print("✗ iOS PWA meta tag'lar yo'q")
    
    print(f"\n📊 PWA Score: {score}/{max_score}")
    
    if score == max_score:
        print("🎉 Ajoyib! PWA to'liq tayyor")
    elif score >= 3:
        print("👍 Yaxshi! Ba'zi yaxshilashlar kerak")
    else:
        print("⚠️ Ko'p ishlar qoldi")
    
    return score

def generate_test_report():
    """Test hisobotini yaratish"""
    print("=" * 60)
    print("🧪 iOS PWA TEST HISOBOTI")
    print("=" * 60)
    
    # Barcha testlarni ishga tushirish
    manifest_ok = check_manifest()
    sw_ok = check_service_worker()
    icons_ok = check_icons()
    html_ok = check_html_meta_tags()
    score = test_pwa_score()
    
    print("\n" + "=" * 60)
    print("📋 XULOSA")
    print("=" * 60)
    
    if all([manifest_ok, sw_ok, icons_ok, html_ok]) and score >= 4:
        print("✅ iOS PWA to'liq tayyor!")
        print("\n🚀 Keyingi qadamlar:")
        print("1. Web server'ni ishga tushiring")
        print("2. iOS Safari'da saytni oching")
        print("3. Ulashish tugmasini bosing")
        print("4. 'Bosh ekranga qo'shish' ni tanlang")
        print("5. PWA sifatida foydalaning!")
    else:
        print("⚠️ Ba'zi muammolar mavjud:")
        if not manifest_ok:
            print("- Manifest faylini to'g'rilang")
        if not sw_ok:
            print("- Service Worker'ni to'g'rilang")
        if not icons_ok:
            print("- Icon fayllarini yarating (generate_ios_icons.py ishga tushiring)")
        if not html_ok:
            print("- HTML meta tag'larni qo'shing")
        if score < 4:
            print("- PWA score'ni oshiring")

def main():
    """Asosiy funksiya"""
    try:
        generate_test_report()
    except KeyboardInterrupt:
        print("\n\n❌ Test to'xtatildi")
    except Exception as e:
        print(f"\n❌ Kutilmagan xatolik: {e}")

if __name__ == "__main__":
    main()