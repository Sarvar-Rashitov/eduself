"""Obuna handlerlari"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from asgiref.sync import sync_to_async
from telegram_bot.utils import get_user_or_none
from telegram_bot.decorators import require_subscription
import os

SITE_URL = os.getenv('SITE_URL', 'https://eduself.uz')


@sync_to_async
def get_subscription_plans():
    """Barcha faol obuna tariflarini olish"""
    from subscriptions.models import SubscriptionPlan
    return list(SubscriptionPlan.objects.filter(is_active=True).order_by('order', 'price'))


@sync_to_async
def get_plan_by_id(plan_id):
    """ID bo'yicha tarifni olish"""
    from subscriptions.models import SubscriptionPlan
    try:
        return SubscriptionPlan.objects.get(id=plan_id, is_active=True)
    except SubscriptionPlan.DoesNotExist:
        return None


@sync_to_async
def get_user_subscription(user):
    """Foydalanuvchi obunasini olish"""
    return user.get_active_subscription()


@sync_to_async
def create_payment(user, plan):
    """To'lov yaratish"""
    from subscriptions.models import Payment
    import uuid
    
    payment = Payment.objects.create(
        user=user,
        plan=plan,
        amount=plan.price,
        final_amount=plan.price,
        payment_method='click',  # Default
        status='pending'
    )
    return payment


async def subscription_plans_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Obuna tariflari ro'yxati"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        message = query.message
        edit = True
    else:
        message = update.message
        edit = False
    
    user = await get_user_or_none(update.effective_user.id)
    if not user:
        return
    
    plans = await get_subscription_plans()
    current_sub = await get_user_subscription(user)
    
    text = "💎 *EduSelf Pro*\n\n"
    
    if current_sub:
        end_date = current_sub.end_date.strftime('%d.%m.%Y')
        text += f"✅ Sizda faol obuna bor: *{current_sub.plan.name}*\n"
        text += f"📅 Tugash sanasi: {end_date}\n\n"
        text += "━━━━━━━━━━━━━━━\n\n"
    
    text += "*Premium imkoniyatlar:*\n\n"
    text += "♾️ Cheksiz yurakchalar\n"
    text += "🔓 Barcha mavzular ochiq\n"
    text += "🤖 AI tahlil va hamroh\n"
    text += "🏆 Universitet imtihonlari\n"
    text += "📝 Mock imtihonlar\n"
    text += "🎓 Sertifikat testlari\n\n"
    text += "Quyidagi tariflardan birini tanlang:"
    
    keyboard = []
    for plan in plans:
        price_text = f"{int(plan.price):,}".replace(',', ' ')
        duration_text = f"{plan.duration_days} kun"
        
        if plan.is_popular:
            button_text = f"⭐ {plan.name} - {price_text} so'm / {duration_text}"
        else:
            button_text = f"💎 {plan.name} - {price_text} so'm / {duration_text}"
        
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"plan_{plan.id}")])
    
    keyboard.append([InlineKeyboardButton("🏠 Asosiy menyu", callback_data="main_menu")])
    
    if edit:
        await message.edit_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await message.reply_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def plan_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tarif tafsilotlari"""
    query = update.callback_query
    await query.answer()
    
    plan_id = int(query.data.split('_')[1])
    plan = await get_plan_by_id(plan_id)
    
    if not plan:
        await query.answer("❌ Tarif topilmadi!", show_alert=True)
        return
    
    user = await get_user_or_none(update.effective_user.id)
    
    price_text = f"{int(plan.price):,}".replace(',', ' ')
    
    text = f"💎 *{plan.name}*\n\n"
    
    if plan.description:
        text += f"{plan.description}\n\n"
    
    text += f"💰 Narx: *{price_text} so'm*\n"
    text += f"📅 Muddat: *{plan.duration_days} kun*\n\n"
    
    text += "*Imkoniyatlar:*\n\n"
    
    if plan.unlimited_lives:
        text += "♾️ Cheksiz yurakchalar\n"
    
    if plan.ai_analysis_limit == -1:
        text += "🤖 Cheksiz AI tahlil\n"
    elif plan.ai_analysis_limit > 0:
        text += f"🤖 {plan.ai_analysis_limit} ta AI tahlil\n"
    
    if plan.ai_companion_limit == -1:
        text += "💬 Cheksiz AI hamroh\n"
    elif plan.ai_companion_limit > 0:
        text += f"💬 {plan.ai_companion_limit} ta AI hamroh\n"
    
    if plan.university_exam_limit == -1:
        text += "🏆 Cheksiz universitet imtihonlari\n"
    elif plan.university_exam_limit > 0:
        text += f"🏆 {plan.university_exam_limit} ta universitet imtihoni\n"
    
    if plan.mock_exam_limit == -1:
        text += "📝 Cheksiz mock imtihonlar\n"
    elif plan.mock_exam_limit > 0:
        text += f"📝 {plan.mock_exam_limit} ta mock imtihon\n"
    
    if plan.certificate_test_limit == -1:
        text += "🎓 Cheksiz sertifikat testlari\n"
    elif plan.certificate_test_limit > 0:
        text += f"🎓 {plan.certificate_test_limit} ta sertifikat testi\n"
    
    text += "\n🔓 Barcha mavzular ochiq\n"
    text += "\nTo'lov turini tanlang:"
    
    keyboard = [
        [InlineKeyboardButton("💳 Click", callback_data=f"pay_click_{plan.id}")],
        [InlineKeyboardButton("💳 Payme", callback_data=f"pay_payme_{plan.id}")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="subscription_plans")]
    ]
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def payment_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Click to'lov"""
    query = update.callback_query
    await query.answer()
    
    plan_id = int(query.data.split('_')[2])
    plan = await get_plan_by_id(plan_id)
    
    if not plan:
        await query.answer("❌ Tarif topilmadi!", show_alert=True)
        return
    
    user = await get_user_or_none(update.effective_user.id)
    if not user:
        return
    
    # To'lov yaratish
    payment = await create_payment(user, plan)
    
    # Click to'lov havolasi
    click_url = f"{SITE_URL}/subscriptions/payment/{payment.id}/click/"
    
    price_text = f"{int(plan.price):,}".replace(',', ' ')
    
    text = f"💳 *Click orqali to'lov*\n\n"
    text += f"📦 Tarif: {plan.name}\n"
    text += f"💰 Summa: {price_text} so'm\n"
    text += f"📅 Muddat: {plan.duration_days} kun\n\n"
    text += "Quyidagi tugmani bosib to'lovni amalga oshiring:"
    
    keyboard = [
        [InlineKeyboardButton("💳 Click orqali to'lash", url=click_url)],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data=f"plan_{plan.id}")]
    ]
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def payment_payme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Payme to'lov"""
    query = update.callback_query
    await query.answer()
    
    plan_id = int(query.data.split('_')[2])
    plan = await get_plan_by_id(plan_id)
    
    if not plan:
        await query.answer("❌ Tarif topilmadi!", show_alert=True)
        return
    
    user = await get_user_or_none(update.effective_user.id)
    if not user:
        return
    
    # To'lov yaratish
    payment = await create_payment(user, plan)
    
    # Payme to'lov havolasi
    payme_url = f"{SITE_URL}/subscriptions/payment/{payment.id}/payme/"
    
    price_text = f"{int(plan.price):,}".replace(',', ' ')
    
    text = f"💳 *Payme orqali to'lov*\n\n"
    text += f"📦 Tarif: {plan.name}\n"
    text += f"💰 Summa: {price_text} so'm\n"
    text += f"📅 Muddat: {plan.duration_days} kun\n\n"
    text += "Quyidagi tugmani bosib to'lovni amalga oshiring:"
    
    keyboard = [
        [InlineKeyboardButton("💳 Payme orqali to'lash", url=payme_url)],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data=f"plan_{plan.id}")]
    ]
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def handle_pro_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """EduSelf Pro tugmasi bosilganda"""
    if update.message.text == "💎 EduSelf Pro":
        await subscription_plans_menu(update, context)


def register_handlers(app):
    """Subscription handlerlarini ro'yxatdan o'tkazish"""
    app.add_handler(CallbackQueryHandler(subscription_plans_menu, pattern="^subscription_plans$"))
    app.add_handler(CallbackQueryHandler(plan_detail, pattern=r"^plan_\d+$"))
    app.add_handler(CallbackQueryHandler(payment_click, pattern=r"^pay_click_\d+$"))
    app.add_handler(CallbackQueryHandler(payment_payme, pattern=r"^pay_payme_\d+$"))
    app.add_handler(MessageHandler(filters.Regex("^💎 EduSelf Pro$"), handle_pro_text))
