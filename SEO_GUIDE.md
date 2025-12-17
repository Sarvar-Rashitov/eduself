# EduSelf SEO Qo'llanma

## O'rnatilgan SEO Xususiyatlari

### 1. Sitemap.xml
Saytingizning barcha sahifalari uchun avtomatik sitemap yaratildi:
- **URL**: `https://eduself.uz/sitemap.xml`
- **Qamrab olgan sahifalar**:
  - Bosh sahifa va statik sahifalar
  - Barcha fanlar (subjects)
  - Barcha mavzular (topics)
  - Barcha testlar
  - Barcha sertifikatlar
  - Mock imtihonlar
  - Ta'lim muassasalari
  - Yangiliklar
  - Kurslar

### 2. Robots.txt
Qidiruv tizimlariga yo'riqnoma:
- **URL**: `https://eduself.uz/robots.txt`
- **Ruxsat berilgan**: Barcha ochiq sahifalar
- **Taqiqlangan**: Admin panel, login/logout sahifalari

### 3. Meta Teglar
Har bir sahifa uchun SEO-optimallashtirilgan meta teglar:
- **Title**: Sahifa sarlavhasi
- **Description**: Sahifa tavsifi
- **Keywords**: Kalit so'zlar
- **Canonical URL**: Takrorlanishni oldini olish
- **Robots**: index, follow

### 4. Open Graph (Facebook/LinkedIn)
Ijtimoiy tarmoqlarda ulashish uchun:
- og:title
- og:description
- og:image
- og:url
- og:type

### 5. Twitter Cards
Twitter'da ulashish uchun:
- twitter:card
- twitter:title
- twitter:description
- twitter:image

### 6. Structured Data (Schema.org)
Google uchun tuzilgan ma'lumotlar:
- EducationalOrganization schema
- JSON-LD format

## Google Search Console'ga Qo'shish

### 1-qadam: Google Search Console'ga kiring
- https://search.google.com/search-console

### 2-qadam: Saytni qo'shing
- "Add property" tugmasini bosing
- `https://eduself.uz` kiriting

### 3-qadam: Tasdiqlash
**Tavsiya qilingan usul - HTML tag:**
```html
<meta name="google-site-verification" content="YOUR_CODE_HERE" />
```
Bu tegni `templates/base.html` fayliga qo'shing (head bo'limiga).

**Yoki DNS usuli:**
- DNS provayderingizga kiring
- TXT record qo'shing

### 4-qadam: Sitemap yuborish
1. Google Search Console'da "Sitemaps" bo'limiga o'ting
2. Sitemap URL'ni kiriting: `https://eduself.uz/sitemap.xml`
3. "Submit" tugmasini bosing

## Google Analytics O'rnatish

### 1-qadam: Google Analytics hisobi yarating
- https://analytics.google.com

### 2-qadam: Tracking ID oling
- Yangi property yarating
- Tracking ID ni nusxalang (masalan: G-XXXXXXXXXX)

### 3-qadam: Kodni qo'shing
`templates/base.html` fayliga quyidagi kodni qo'shing (</head> tegidan oldin):

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

## Yandex Metrica O'rnatish

### 1-qadam: Yandex Metrica hisobi yarating
- https://metrica.yandex.com

### 2-qadam: Counter ID oling

### 3-qadam: Kodni qo'shing
`templates/base.html` fayliga quyidagi kodni qo'shing:

```html
<!-- Yandex.Metrika counter -->
<script type="text/javascript" >
   (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
   m[i].l=1*new Date();
   for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
   k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
   (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

   ym(XXXXXX, "init", {
        clickmap:true,
        trackLinks:true,
        accurateTrackBounce:true,
        webvisor:true
   });
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/XXXXXX" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->
```

## SEO Tavsiyalar

### 1. Kontent Optimizatsiyasi
- Har bir sahifada noyob title va description bo'lishi kerak
- Kalit so'zlarni tabiiy ravishda ishlating
- H1, H2, H3 teglaridan to'g'ri foydalaning
- Rasmlar uchun alt atributlarini qo'shing

### 2. Tezlik Optimizatsiyasi
- Rasmlarni siqing (WebP formatidan foydalaning)
- CSS va JS fayllarni minify qiling
- CDN dan foydalaning
- Browser caching yoqing

### 3. Mobil Optimizatsiya
- Responsive dizayn (✓ allaqachon mavjud)
- Touch-friendly elementlar (✓ allaqachon mavjud)
- Tez yuklash

### 4. Ichki Havolalar
- Tegishli sahifalar o'rtasida havolalar qo'shing
- Breadcrumb navigatsiya qo'shing
- Footer'da muhim havolalar bo'lsin

### 5. Tashqi Havolalar
- Sifatli saytlardan backlink oling
- Ijtimoiy tarmoqlarda faol bo'ling
- Guest posting qiling

## Monitoring va Tahlil

### Haftalik Tekshiruvlar
1. Google Search Console'da xatolarni tekshiring
2. Sitemap statusini ko'ring
3. Qidiruv natijalarini kuzating

### Oylik Tahlil
1. Google Analytics'da trafikni tahlil qiling
2. Eng ko'p tashrif buyurilgan sahifalarni aniqlang
3. Bounce rate'ni kamaytirish yo'llarini toping
4. Conversion rate'ni oshiring

### SEO Metrikalar
- **Organic Traffic**: Qidiruv tizimlaridan kelgan foydalanuvchilar
- **Keyword Rankings**: Kalit so'zlar bo'yicha pozitsiya
- **Backlinks**: Tashqi havolalar soni
- **Page Speed**: Sahifa yuklash tezligi
- **Mobile Usability**: Mobil qurilmalarda foydalanish qulayligi

## Qo'shimcha Vositalar

### SEO Tekshirish Vositalari
- Google PageSpeed Insights: https://pagespeed.web.dev/
- GTmetrix: https://gtmetrix.com/
- Screaming Frog: https://www.screamingfrog.co.uk/
- Ahrefs: https://ahrefs.com/
- SEMrush: https://www.semrush.com/

### Schema Markup Tekshirish
- Google Rich Results Test: https://search.google.com/test/rich-results
- Schema.org Validator: https://validator.schema.org/

## Muammolarni Hal Qilish

### Sitemap ko'rinmayapti
1. URL to'g'riligini tekshiring: `https://eduself.uz/sitemap.xml`
2. Robots.txt'da sitemap ko'rsatilganligini tekshiring
3. Google Search Console'da qayta yuborib ko'ring

### Sahifalar indekslanmayapti
1. robots.txt'da ruxsat berilganligini tekshiring
2. Meta robots tegida "noindex" yo'qligini tekshiring
3. Google Search Console'da "URL Inspection" dan foydalaning

### Tezlik muammolari
1. Rasmlarni siqing
2. Caching yoqing
3. CDN dan foydalaning
4. Keraksiz plugin va scriptlarni o'chiring

## Yordam

Agar qo'shimcha yordam kerak bo'lsa:
- Email: support@eduself.uz
- Telegram: @eduself_uz

---

**Eslatma**: SEO - bu uzoq muddatli jarayon. Natijalar 3-6 oy ichida ko'rinadi. Sabr va izchillik muhim!
