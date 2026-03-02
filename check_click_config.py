"""
Click konfiguratsiyasini tekshirish
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()

from django.conf import settings


def check_click_config():
    """Click sozlamalarini tekshirish"""
    
    print("=" * 70)
    print("CLICK KONFIGURATSIYASINI TEKSHIRISH")
    print("=" * 70)
    
    # Barcha kerakli sozlamalar
    configs = {
        'CLICK_MERCHANT_ID': settings.CLICK_MERCHANT_ID,
        'CLICK_SERVICE_ID': settings.CLICK_SERVICE_ID,
        'CLICK_SECRET_KEY': settings.CLICK_SECRET_KEY,
        'CLICK_MERCHANT_USER_ID': settings.CLICK_MERCHANT_USER_ID,
    }
    
    print("\n📋 Hozirgi Sozlamalar:\n")
    
    all_configured = True
    
    for key, value in configs.items():
        # Qiymatni tekshirish
        is_default = value.startswith('your_') if isinstance(value, str) else False
        is_empty = not value or value.strip() == ''
        is_dots = '···' in str(value) or '...' in str(value)
        
        # Status aniqlash
        if is_default or is_empty:
            status = "❌ TO'LDIRILMAGAN"
            all_configured = False
            display_value = value if value else "(bo'sh)"
        elif is_dots:
            status = "⚠️  YASHIRIN"
            display_value = "••••••••••••"
        elif key == 'CLICK_SECRET_KEY':
            status = "✅ TO'LDIRILGAN"
            # Secret key'ni to'liq ko'rsatmaslik
            display_value = f"{value[:10]}..." if len(value) > 10 else "••••••••••"
        else:
            status = "✅ TO'LDIRILGAN"
            display_value = value
        
        print(f"{key:30} {status}")
        print(f"{'':30} Qiymat: {display_value}")
        print()
    
    # Xulosa
    print("=" * 70)
    print("XULOSA")
    print("=" * 70)
    
    if all_configured:
        print("\n✅ Barcha sozlamalar to'ldirilgan!")
        print("\n📝 Keyingi qadamlar:")
        print("   1. Test skriptini ishga tushiring:")
        print("      python test_click_payment.py")
        print("   2. Click merchant panelda callback URL'larni sozlang:")
        print("      Prepare: https://eduself.uz/subscriptions/payment/click/prepare/")
        print("      Complete: https://eduself.uz/subscriptions/payment/click/complete/")
    else:
        print("\n⚠️  Ba'zi sozlamalar to'ldirilmagan!")
        print("\n📝 To'ldirish kerak:")
        
        for key, value in configs.items():
            is_default = value.startswith('your_') if isinstance(value, str) else False
            is_empty = not value or value.strip() == ''
            
            if is_default or is_empty:
                print(f"   ❌ {key}")
                
                # Maslahat berish
                if key == 'CLICK_SECRET_KEY':
                    print("      → Click merchant paneldan oling")
                    print("      → https://my.click.uz → Xizmatlar → API → Secret Key")
                elif key == 'CLICK_MERCHANT_USER_ID':
                    print("      → Ixtiyoriy (optional)")
                    print("      → MERCHANT_ID'ni ishlatishingiz mumkin: 57452")
                    print("      → Yoki Click support'dan so'rang")
        
        print("\n📞 Yordam kerak bo'lsa:")
        print("   Email: support@click.uz")
        print("   Telegram: @click_support")
        print("   Telefon: +998 71 200 0 200")
    
    print("\n" + "=" * 70)
    
    # Qo'shimcha ma'lumot
    print("\n💡 Foydali Ma'lumotlar:")
    print(f"   Merchant ID: {configs['CLICK_MERCHANT_ID']}")
    print(f"   Service ID: {configs['CLICK_SERVICE_ID']}")
    print(f"   Merchant Panel: https://my.click.uz")
    print(f"   API Docs: https://docs.click.uz/")
    
    # Secret key uzunligini tekshirish
    if configs['CLICK_SECRET_KEY'] and not configs['CLICK_SECRET_KEY'].startswith('your_'):
        secret_len = len(configs['CLICK_SECRET_KEY'])
        print(f"\n🔑 Secret Key:")
        print(f"   Uzunlik: {secret_len} belgi")
        
        if secret_len < 16:
            print("   ⚠️  Juda qisqa! To'g'ri ekanligini tekshiring.")
        elif secret_len > 100:
            print("   ⚠️  Juda uzun! To'g'ri ekanligini tekshiring.")
        else:
            print("   ✅ Uzunlik normal")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    check_click_config()
