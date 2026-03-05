"""
Icon Generator Script for PWA
Bu script EduSelf logosidan barcha kerakli icon o'lchamlarini yaratadi.

Requirements:
    pip install Pillow

Usage:
    python generate_icons.py logo.png
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# Icon o'lchamlari
ICON_SIZES = [16, 32, 72, 96, 128, 144, 152, 192, 384, 512]

# Maskable icon uchun padding (10%)
MASKABLE_PADDING = 0.1

def create_placeholder_logo(size=512):
    """
    EduSelf platformasi uchun ultra-zamonaviy va chiroyli icon
    Modern UI/UX printsiplari asosida
    """
    # RGBA formatda rasm yaratish
    img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center = size // 2
    
    # === BACKGROUND: Zamonaviy Gradient Circle ===
    # Smooth radial gradient effect
    for i in range(size // 2, 0, -1):
        # Gradient from center: #667eea → #764ba2 → darker edges
        progress = i / (size // 2)
        r = int(102 + (118 - 102) * (1 - progress) + 30 * (1 - progress))
        g = int(126 - (126 - 75) * (1 - progress))
        b = int(234 - (234 - 162) * (1 - progress))
        alpha = int(255 * progress)
        
        draw.ellipse(
            [center - i, center - i, center + i, center + i],
            fill=(r, g, b, alpha)
        )
    
    # === MAIN CIRCLE: Oq background ===
    main_radius = int(size * 0.42)
    draw.ellipse(
        [center - main_radius, center - main_radius,
         center + main_radius, center + main_radius],
        fill=(255, 255, 255, 255)
    )
    
    # === DECORATIVE CIRCLES: Orqa fonda ===
    # Top-right accent circle
    accent_size = int(size * 0.15)
    draw.ellipse(
        [center + main_radius - accent_size, center - main_radius,
         center + main_radius, center - main_radius + accent_size],
        fill=(102, 126, 234, 100)
    )
    
    # Bottom-left accent circle
    draw.ellipse(
        [center - main_radius, center + main_radius - accent_size,
         center - main_radius + accent_size, center + main_radius],
        fill=(118, 75, 162, 100)
    )
    
    # === MAIN ICON: Stylized "E" with book ===
    icon_size = int(size * 0.5)
    icon_x = center - icon_size // 2
    icon_y = center - icon_size // 2
    
    # Modern "E" shape (3 horizontal bars)
    bar_height = int(icon_size * 0.12)
    bar_width_long = int(icon_size * 0.6)
    bar_width_short = int(icon_size * 0.45)
    spacing = int(icon_size * 0.18)
    
    # Gradient colors for bars
    colors = [
        (79, 70, 229, 255),   # Indigo
        (102, 126, 234, 255), # Light Indigo
        (118, 75, 162, 255)   # Purple
    ]
    
    # Top bar (longest)
    y_pos = icon_y + int(icon_size * 0.15)
    draw.rounded_rectangle(
        [icon_x + int(icon_size * 0.15), y_pos,
         icon_x + int(icon_size * 0.15) + bar_width_long, y_pos + bar_height],
        radius=bar_height // 2,
        fill=colors[0]
    )
    
    # Middle bar (medium)
    y_pos += spacing
    draw.rounded_rectangle(
        [icon_x + int(icon_size * 0.15), y_pos,
         icon_x + int(icon_size * 0.15) + bar_width_short, y_pos + bar_height],
        radius=bar_height // 2,
        fill=colors[1]
    )
    
    # Bottom bar (longest)
    y_pos += spacing
    draw.rounded_rectangle(
        [icon_x + int(icon_size * 0.15), y_pos,
         icon_x + int(icon_size * 0.15) + bar_width_long, y_pos + bar_height],
        radius=bar_height // 2,
        fill=colors[2]
    )
    
    # === ACCENT: Graduation cap icon (kichik, o'ng yuqorida) ===
    cap_size = int(size * 0.18)
    cap_x = center + int(size * 0.22)
    cap_y = center - int(size * 0.28)
    
    # Cap base (rounded rectangle)
    cap_base_height = int(cap_size * 0.25)
    draw.rounded_rectangle(
        [cap_x - cap_size // 2, cap_y,
         cap_x + cap_size // 2, cap_y + cap_base_height],
        radius=cap_base_height // 2,
        fill=(255, 193, 7, 255)  # Gold
    )
    
    # Cap top (diamond shape)
    cap_top_size = int(cap_size * 0.6)
    draw.polygon(
        [
            (cap_x, cap_y - cap_top_size // 2),  # Top
            (cap_x + cap_top_size // 2, cap_y),   # Right
            (cap_x, cap_y + cap_top_size // 4),   # Bottom
            (cap_x - cap_top_size // 2, cap_y)    # Left
        ],
        fill=(255, 193, 7, 255)
    )
    
    # Tassel (decorative string)
    tassel_length = int(cap_size * 0.4)
    draw.line(
        [(cap_x + cap_size // 3, cap_y),
         (cap_x + cap_size // 2, cap_y + tassel_length)],
        fill=(255, 193, 7, 255),
        width=max(2, size // 200)
    )
    # Tassel end (small circle)
    tassel_end_size = int(cap_size * 0.15)
    draw.ellipse(
        [cap_x + cap_size // 2 - tassel_end_size // 2,
         cap_y + tassel_length - tassel_end_size // 2,
         cap_x + cap_size // 2 + tassel_end_size // 2,
         cap_y + tassel_length + tassel_end_size // 2],
        fill=(255, 193, 7, 255)
    )
    
    # === SPARKLE EFFECTS: Yulduzchalar ===
    sparkle_positions = [
        (center - int(size * 0.35), center - int(size * 0.15)),
        (center + int(size * 0.32), center + int(size * 0.25)),
        (center - int(size * 0.15), center + int(size * 0.35))
    ]
    
    for sx, sy in sparkle_positions:
        sparkle_size = int(size * 0.04)
        # Horizontal line
        draw.line(
            [(sx - sparkle_size, sy), (sx + sparkle_size, sy)],
            fill=(255, 193, 7, 200),
            width=max(2, size // 250)
        )
        # Vertical line
        draw.line(
            [(sx, sy - sparkle_size), (sx, sy + sparkle_size)],
            fill=(255, 193, 7, 200),
            width=max(2, size // 250)
        )
    
    # === SUBTLE SHADOW: Depth effect ===
    shadow_offset = int(size * 0.01)
    shadow_radius = main_radius + shadow_offset
    for i in range(5):
        alpha = int(30 - i * 5)
        draw.ellipse(
            [center - shadow_radius - i, center - shadow_radius - i,
             center + shadow_radius + i, center + shadow_radius + i],
            outline=(0, 0, 0, alpha),
            width=1
        )
    
    return img

def create_maskable_icon(img, size):
    """
    Maskable icon yaratish (Android adaptive icons uchun)
    Ultra-zamonaviy gradient background bilan
    """
    # Yangi rasm yaratish
    maskable = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(maskable)
    
    center = size // 2
    
    # Radial gradient background (markazdan tashqariga)
    for i in range(size // 2, 0, -1):
        progress = i / (size // 2)
        # Gradient: #667eea → #764ba2
        r = int(102 + (118 - 102) * (1 - progress))
        g = int(126 - (126 - 75) * (1 - progress))
        b = int(234 - (234 - 162) * (1 - progress))
        
        draw.ellipse(
            [center - i, center - i, center + i, center + i],
            fill=(r, g, b, 255)
        )
    
    # Original rasmni kichikroq qilish (75% o'lcham - ko'proq padding)
    inner_size = int(size * 0.75)
    img_resized = img.resize((inner_size, inner_size), Image.Resampling.LANCZOS)
    
    # Markazga joylashtirish
    offset = (size - inner_size) // 2
    
    # Agar rasm RGBA bo'lsa, alpha channel bilan paste qilish
    if img_resized.mode == 'RGBA':
        maskable.paste(img_resized, (offset, offset), img_resized)
    else:
        maskable.paste(img_resized, (offset, offset))
    
    return maskable

def generate_icons(source_image_path, output_dir='static/icons'):
    """
    Barcha kerakli icon o'lchamlarini yaratish
    """
    # Output papkasini yaratish
    os.makedirs(output_dir, exist_ok=True)
    
    # Source rasmni yuklash yoki placeholder yaratish
    if os.path.exists(source_image_path):
        print(f"📷 Logo yuklanmoqda: {source_image_path}")
        source_img = Image.open(source_image_path)
        
        # RGBA formatga o'tkazish
        if source_img.mode != 'RGBA':
            source_img = source_img.convert('RGBA')
    else:
        print("⚠️  Logo topilmadi. Placeholder yaratilmoqda...")
        source_img = create_placeholder_logo()
    
    # Har bir o'lcham uchun icon yaratish
    for size in ICON_SIZES:
        # Oddiy icon
        icon = source_img.resize((size, size), Image.Resampling.LANCZOS)
        icon_path = os.path.join(output_dir, f'icon-{size}x{size}.png')
        icon.save(icon_path, 'PNG', optimize=True)
        print(f"✅ Yaratildi: icon-{size}x{size}.png")
        
        # Maskable icon (faqat 192 va 512 uchun)
        if size in [192, 512]:
            maskable = create_maskable_icon(source_img, size)
            maskable_path = os.path.join(output_dir, f'icon-{size}x{size}-maskable.png')
            maskable.save(maskable_path, 'PNG', optimize=True)
            print(f"✅ Yaratildi: icon-{size}x{size}-maskable.png (maskable)")
    
    print(f"\n🎉 Barcha iconlar yaratildi: {output_dir}/")
    print("\n📝 Keyingi qadamlar:")
    print("1. manifest.json faylida icon yo'llarini tekshiring")
    print("2. python manage.py collectstatic --noinput")
    print("3. PWA'ni test qiling")

def main():
    if len(sys.argv) > 1:
        source_image = sys.argv[1]
    else:
        print("ℹ️  Logo fayl yo'li ko'rsatilmadi.")
        print("📝 Foydalanish: python generate_icons.py logo.png")
        print("\n🎨 Placeholder icon yaratilmoqda...")
        source_image = "placeholder"
    
    generate_icons(source_image)

if __name__ == '__main__':
    main()
