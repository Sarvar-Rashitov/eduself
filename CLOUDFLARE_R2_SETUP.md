# Cloudflare R2 Storage Setup Guide

## 1. Cloudflare R2 Bucket yaratish

1. Cloudflare Dashboard ga kiring
2. **R2 Object Storage** bo'limiga o'ting
3. **Create bucket** tugmasini bosing
4. Bucket nomini kiriting (masalan: `eduself-media`)
5. **Create bucket** tugmasini bosing

## 2. API Token yaratish

1. Cloudflare Dashboard da **My Profile** > **API Tokens** ga o'ting
2. **Create Token** tugmasini bosing
3. **Custom token** ni tanlang
4. Quyidagi sozlamalarni kiriting:
   - **Token name**: `EduSelf R2 Access`
   - **Permissions**:
     - Account - Cloudflare R2:Edit
   - **Account Resources**: 
     - Include - Specific account - [sizning account id]
   - **Zone Resources**: All zones
5. **Continue to summary** > **Create Token**
6. Token ni nusxalab oling (bu Access Key ID bo'ladi)

## 3. Secret Access Key olish

1. R2 bo'limida **Manage R2 API tokens** ga o'ting
2. **Create API token** tugmasini bosing
3. Token nomini kiriting
4. **Permissions**: Admin Read & Write
5. **Create API token**
6. **Access Key ID** va **Secret Access Key** ni nusxalab oling

## 4. Environment Variables ni yangilash

`.env` faylingizda quyidagi qiymatlarni o'zgartiring:

```env
# Cloudflare R2 Storage
USE_S3=True
AWS_ACCESS_KEY_ID=your-actual-access-key-id
AWS_SECRET_ACCESS_KEY=your-actual-secret-access-key
AWS_STORAGE_BUCKET_NAME=eduself-media
AWS_S3_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
AWS_S3_REGION_NAME=auto
AWS_DEFAULT_ACL=None
# AWS_S3_CUSTOM_DOMAIN=media.eduself.uz  # Agar custom domain sozlasangiz
```

**Account ID ni topish:**
1. Cloudflare Dashboard da o'ng tomonda **Account ID** ko'rinadi
2. Yoki R2 bo'limida **Settings** da topishingiz mumkin

## 5. Custom Domain sozlash (ixtiyoriy)

Agar o'z domeningizni ishlatmoqchi bo'lsangiz:

1. R2 bucket sozlamalarida **Custom Domains** ga o'ting
2. **Connect Domain** tugmasini bosing
3. Subdomain kiriting (masalan: `media.eduself.uz`)
4. DNS record qo'shish ko'rsatmalarini bajaring
5. `.env` faylida `AWS_S3_CUSTOM_DOMAIN=media.eduself.uz` ni yoqing

## 6. Render.com da Environment Variables sozlash

Render.com dashboard da:

1. Loyihangizni tanlang
2. **Environment** tab ga o'ting
3. Quyidagi o'zgaruvchilarni qo'shing:
   - `USE_S3=True`
   - `AWS_ACCESS_KEY_ID=your-access-key`
   - `AWS_SECRET_ACCESS_KEY=your-secret-key`
   - `AWS_STORAGE_BUCKET_NAME=your-bucket-name`
   - `AWS_S3_ENDPOINT_URL=https://account-id.r2.cloudflarestorage.com`
   - `AWS_S3_REGION_NAME=auto`
   - `AWS_DEFAULT_ACL=None`

## 7. Mavjud media fayllarni ko'chirish

Agar mavjud media fayllaringiz bo'lsa:

```bash
python manage.py migrate_media_to_r2
```

## 8. Test qilish

1. Admin panelga kiring
2. Biror model ga rasm yuklang
3. Rasm R2 da saqlanganini tekshiring
4. Rasm to'g'ri ko'rsatilayotganini tekshiring

## Xavfsizlik

- API kalitlarni hech qachon kodga qo'shmang
- Faqat kerakli permissions bering
- Token larni muntazam yangilab turing