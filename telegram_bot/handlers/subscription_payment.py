"""To'lov handlerlari - Click va Payme"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async
from telegram_bot.utils import get_user_or_none
from django.conf import settings
import os
import base64


SITE_URL = os.getenv('SITE_URL', 'https://eduself.uz')


@sync_to_async
def get_plan_by_id(plan_id):
    """ID bo'yicha tarifni olish"""
    from subscriptions.models import SubscriptionPlan
    try:
        return SubscriptionPlan.objects.get(id=plan_id, is_active=True)
    except SubscriptionPlan.DoesNotExist:
        return None


@sync_to_async
def get_promo_code(code):
    """Promokodni olish"""
    from subscriptions.models import PromoCode
    try:
        return PromoCode.objects.get(code=code.upper(), is_active=True)
    except PromoCode.DoesNotExist:
        return None


@sync_to_async
def create_payment(user, plan, promo_code=None):
    """To'lov yaratish"""
    from subscriptions.models import Payment
    
    final_amount = plan.price
    discount_amount = 0
    
    if promo_code:
        if promo_code.is_valid():
            final_amount = promo_code.get_discounted_price()
            discount_amount = plan.price - final_amount
    
    payment = Payment.objects.create(
        user=user,
        plan=plan,
        amount=plan.price,
        promo_code=promo_code,
        discount_amount=discount_amount,
        final_amount=final_amount,
        payment_method='click',
        status='pending'
    )
    return payment


async def payment_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Click to'lov - to'g'ridan-to'g'ri Click sahifasiga"""
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split('_')
    plan_id = int(parts[2])
    promo_code_str = parts[3] if len(parts) > 3 else 'none'
    
    plan = await get_plan_by_id(plan_id)
    
    if not plan:
        await query.answer("❌ Tarif topilmadi!", show_alert=True)
        return
    
    user = await get_user_or_none(update.effective_user.id)
    if not user:
        return
    
    # Promokodni olish
    promo_code = None
    if promo_code_str != 'none':
        promo_code = await get_promo_code(promo_code_str)
    
    # To'lov yaratish
    payment = await create_payment(user, plan, promo_code)
    
    # Click to'lov URL'i - to'g'ridan-to'g'ri Click sahifasiga
    click_url = (
        f"https://my.click.uz/services/pay?"
        f"service_id={settings.CLICK_SERVICE_ID}&"
        f"merchant_id={settings.CLICK_MERCHANT_ID}&"
        f"amount={payment.final_amount}&"
        f"transaction_param={payment.id}&"
        f"return_url={SITE_URL}/subscriptions/my-subscriptions/"
    )
    
    price_text = f"{int(payment.final_amount):,}".replace(',', ' ')
    
    text = f"╔═══════════════════╗\n"
    text += f"   💳 CLICK TO'LOV\n"
    text += f"╚═══════════════════╝\n\n"
    text += f"📦 Tarif: *{plan.name}*\n"
    
    if promo_code and payment.discount_amount > 0:
        original_price = f"{int(plan.price):,}".replace(',', ' ')
        discount = f"{int(payment.discount_amount):,}".replace(',', ' ')
        text += f"💰 Asl narx: ~{original_price} so'm~\n"
        text += f"🎉 Chegirma: -{discount} so'm\n"
    
    text += f"💰 To'lov summasi: *{price_text} so'm*\n"
    text += f"📅 Muddat: *{plan.duration_days} kun*\n\n"
    text += "━━━━━━━━━━━━━━━\n\n"
    text += "✅ Quyidagi tugmani bosib to'lovni amalga oshiring\n\n"
    text += "🔒 Xavfsiz to'lov tizimi\n"
    text += "⚡ Obuna darhol faollashadi\n"
    text += "📱 Karta yoki telefon raqam orqali"
    
    keyboard = [
        [InlineKeyboardButton("💳 Click orqali to'lash →", url=click_url)],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data=f"plan_detail_{plan.id}")]
    ]
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def payment_payme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Payme to'lov - to'g'ridan-to'g'ri Payme sahifasiga"""
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split('_')
    plan_id = int(parts[2])
    promo_code_str = parts[3] if len(parts) > 3 else 'none'
    
    plan = await get_plan_by_id(plan_id)
    
    if not plan:
        await query.answer("❌ Tarif topilmadi!", show_alert=True)
        return
    
    user = await get_user_or_none(update.effective_user.id)
    if not user:
        return
    
    # Promokodni olish
    promo_code = None
    if promo_code_str != 'none':
        promo_code = await get_promo_code(promo_code_str)
    
    # To'lov yaratish
    payment = await create_payment(user, plan, promo_code)
    
    # Payme to'lov URL'i - to'g'ridan-to'g'ri Payme sahifasiga
    account = base64.b64encode(f'{{"payment_id":"{payment.id}"}}'.encode()).decode()
    payme_url = (
        f"{settings.PAYME_ENDPOINT}?"
        f"m={settings.PAYME_MERCHANT_ID}&"
        f"ac.payment_id={payment.id}&"
        f"a={int(payment.final_amount * 100)}&"  # Payme tiyin'da ishlaydi
        f"c={SITE_URL}/subscriptions/my-subscriptions/"
    )
    
    price_text = f"{int(payment.final_amount):,}".replace(',', ' ')
    
    text = f"╔═══════════════════╗\n"
    text += f"   💳 PAYME TO'LOV\n"
    text += f"╚═══════════════════╝\n\n"
    text += f"📦 Tarif: *{plan.name}*\n"
    
    if promo_code and payment.discount_amount > 0:
        original_price = f"{int(plan.price):,}".replace(',', ' ')
        discount = f"{int(payment.discount_amount):,}".replace(',', ' ')
        text += f"💰 Asl narx: ~{original_price} so'm~\n"
        text += f"🎉 Chegirma: -{discount} so'm\n"
    
    text += f"💰 To'lov summasi: *{price_text} so'm*\n"
    text += f"📅 Muddat: *{plan.duration_days} kun*\n\n"
    text += "━━━━━━━━━━━━━━━\n\n"
    text += "✅ Quyidagi tugmani bosib to'lovni amalga oshiring\n\n"
    text += "🔒 Xavfsiz to'lov tizimi\n"
    text += "⚡ Obuna darhol faollashadi\n"
    text += "📱 Payme orqali to'lash"
    
    keyboard = [
        [InlineKeyboardButton("💳 Payme orqali to'lash →", url=payme_url)],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data=f"plan_detail_{plan.id}")]
    ]
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
