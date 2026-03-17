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
def create_payment(user, plan, promo_code=None):
    """To'lov yaratish"""
    from subscriptions.models import Payment
    import uuid
    
    final_amount = plan.price
    discount_amount = 0
    
    if promo_code:
        # Promokod tekshirish
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
        payment_method='click',  # Default
        status='pending'
    )
    return payment


@sync_to_async
def get_promo_code(code):
    """Promokodni olish"""
    from subscriptions.models import PromoCode
    try:
        return PromoCode.objects.get(code=code.upper(), is_active=True)
    except PromoCode.DoesNotExist:
        return None


@sync_to_async
def get_discounted_price(promo_code, plan):
    """Chegirmali narxni hisoblash"""
    if promo_code and promo_code.is_valid() and promo_code.plan == plan:
        return promo_code.get_discounted_price()
    return None


async def subscription_plans_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Obuna tariflari ro'yxati - bitta xabar va tugmalar"""
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
    
    # EduSelf Pro xabari
    text = "╔═══════════════════╗\n"
    text += "   ✨ EDUSELF PRO ✨\n"
    text += "╚═══════════════════╝\n\n"
    
    if current_sub:
        end_date = current_sub.end_date.strftime('%d.%m.%Y')
        text += f"✅ *Sizda faol obuna bor*\n"
        text += f"📦 Tarif: *{current_sub.plan.name}*\n"
        text += f"📅 Tugash: {end_date}\n\n"
        text += "━━━━━━━━━━━━━━━\n\n"
    
    text += "🎯 *Premium imkoniyatlar:*\n\n"
    text += "♾️ Cheksiz yurakchalar\n"
    text += "🔓 Barcha mavzular ochiq\n"
    text += "🤖 AI tahlil va yordamchi\n"
    text += "🏆 Universitet imtihonlari\n"
    text += "📝 Mock imtihonlar\n"
    text += "🎓 Sertifikat testlari\n\n"
    text += "━━━━━━━━━━━━━━━\n\n"
    text += "👇 *Tariflardan birini tanlang:*"
    
    # Tariflar tugmalari
    keyboard = []
    for plan in plans:
        price_text = f"{int(plan.price):,}".replace(',', ' ')
        
        if plan.is_popular:
            button_text = f"⭐ {plan.name} - {price_text} so'm"
        else:
            button_text = f"💎 {plan.name} - {price_text} so'm"
        
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"plan_detail_{plan.id}")])
    
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
    """Tarif tafsilotlari - to'liq ma'lumot"""
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
    
    price_text = f"{int(plan.price):,}".replace(',', ' ')
    
    # Tarif tafsilotlari - to'liq ma'lumot
    if plan.is_popular:
        text = f"╔═══════════════════╗\n"
        text += f"  ⭐ {plan.name.upper()} ⭐\n"
        text += f"╚═══════════════════╝\n"
        text += f"🔥 *ENG MASHHUR TARIF*\n\n"
    else:
        text = f"╔═══════════════════╗\n"
        text += f"   💎 {plan.name.upper()}\n"
        text += f"╚═══════════════════╝\n\n"
    
    if plan.description:
        text += f"📝 {plan.description}\n\n"
    
    text += f"━━━━━━━━━━━━━━━\n\n"
    text += f"💰 *Narx:* {price_text} so'm\n"
    text += f"📅 *Muddat:* {plan.duration_days} kun\n"
    text += f"💵 *Kuniga:* {int(plan.price / plan.duration_days):,} so'm\n\n"
    
    text += f"━━━━━━━━━━━━━━━\n\n"
    text += f"🎁 *TARIF IMKONIYATLARI:*\n\n"
    
    if plan.unlimited_lives:
        text += "♾️ *Cheksiz yurakchalar*\n"
        text += "   • Testlarni cheklovsiz yeching\n"
        text += "   • Xatolik qilsangiz ham davom eting\n"
        text += "   • Istalgan vaqt mashq qiling\n\n"
    
    if plan.ai_analysis_limit == -1:
        text += "🤖 *Cheksiz AI tahlil*\n"
        text += "   • Xatolaringizni batafsil tahlil qiling\n"
        text += "   • Har bir savolga tushuntirish oling\n"
        text += "   • O'z xatolaringizdan o'rganing\n\n"
    elif plan.ai_analysis_limit > 0:
        text += f"🤖 *{plan.ai_analysis_limit} ta AI tahlil*\n"
        text += "   • Xatolaringizni tahlil qiling\n"
        text += "   • Tushuntirish va maslahatlar oling\n\n"
    
    if plan.ai_companion_limit == -1:
        text += "💬 *Cheksiz AI yordamchi*\n"
        text += "   • Istalgan savolingizga javob oling\n"
        text += "   • Mavzularni tushuntirib bering\n"
        text += "   • 24/7 shaxsiy o'qituvchi\n\n"
    elif plan.ai_companion_limit > 0:
        text += f"💬 *{plan.ai_companion_limit} ta AI yordamchi*\n"
        text += "   • Savollaringizga javob oling\n"
        text += "   • Mavzularni tushuntirib bering\n\n"
    
    if plan.university_exam_limit == -1:
        text += "🏆 *Cheksiz universitet imtihonlari*\n"
        text += "   • Barcha universitet testlarini yeching\n"
        text += "   • Real imtihon sharoitida mashq qiling\n"
        text += "   • Qabul imtihoniga tayyorlaning\n\n"
    elif plan.university_exam_limit > 0:
        text += f"🏆 *{plan.university_exam_limit} ta universitet imtihoni*\n"
        text += "   • Universitet testlarini yeching\n"
        text += "   • Qabul imtihoniga tayyorlaning\n\n"
    
    if plan.mock_exam_limit == -1:
        text += "📝 *Cheksiz mock imtihonlar*\n"
        text += "   • Real imtihon formatida mashq qiling\n"
        text += "   • Vaqt boshqaruvini o'rganing\n"
        text += "   • Imtihon stressini kamaytiring\n\n"
    elif plan.mock_exam_limit > 0:
        text += f"📝 *{plan.mock_exam_limit} ta mock imtihon*\n"
        text += "   • Real imtihonlarga tayyorlaning\n"
        text += "   • Vaqt boshqaruvini o'rganing\n\n"
    
    if plan.certificate_test_limit == -1:
        text += "🎓 *Cheksiz sertifikat testlari*\n"
        text += "   • Rasmiy sertifikat oling\n"
        text += "   • Bilimingizni tasdiqlang\n"
        text += "   • Portfolio uchun hujjat\n\n"
    elif plan.certificate_test_limit > 0:
        text += f"🎓 *{plan.certificate_test_limit} ta sertifikat testi*\n"
        text += "   • Rasmiy sertifikat oling\n"
        text += "   • Bilimingizni tasdiqlang\n\n"
    
    text += "🔓 *Barcha mavzular ochiq*\n"
    text += "   • 100+ mavzuga kirish\n"
    text += "   • Istalgan tartibda o'rganing\n"
    text += "   • Hech qanday cheklov yo'q\n\n"
    
    text += "━━━━━━━━━━━━━━━\n\n"
    text += "💡 *Obuna bo'lish uchun quyidagi tugmani bosing*"
    
    keyboard = [
        [InlineKeyboardButton("🛒 Obuna bo'lish", callback_data=f"subscribe_{plan.id}")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="subscription_plans")]
    ]
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def subscribe_to_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tarifga obuna bo'lish - promokod so'rash"""
    query = update.callback_query
    await query.answer()
    
    plan_id = int(query.data.split('_')[1])
    plan = await get_plan_by_id(plan_id)
    
    if not plan:
        await query.answer("❌ Tarif topilmadi!", show_alert=True)
        return
    
    user = await get_user_or_none(update.effective_user.id)
    if not user:
        return
    
    # Promokod so'rash
    price_text = f"{int(plan.price):,}".replace(',', ' ')
    
    text = f"╔═══════════════════╗\n"
    text += f"     🎟 PROMOKOD\n"
    text += f"╚═══════════════════╝\n\n"
    text += f"Agar sizda promokod bo'lsa, uni yuboring.\n\n"
    text += f"Promokod bo'lmasa, \"Yo'q\" tugmasini bosing.\n\n"
    text += f"━━━━━━━━━━━━━━━\n\n"
    text += f"📦 Tarif: *{plan.name}*\n"
    text += f"💰 Narx: *{price_text} so'm*\n"
    text += f"📅 Muddat: *{plan.duration_days} kun*"
    
    keyboard = [
        [InlineKeyboardButton("❌ Promokod yo'q", callback_data=f"no_promo_{plan.id}")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data=f"plan_detail_{plan.id}")]
    ]
    
    # Context'ga plan_id saqlash
    context.user_data['waiting_promo_for_plan'] = plan.id
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def no_promo_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Promokodsiz davom etish"""
    query = update.callback_query
    await query.answer()
    
    plan_id = int(query.data.split('_')[2])
    
    # Context'dan o'chirish
    context.user_data.pop('waiting_promo_for_plan', None)
    
    # To'lov turini tanlash
    await show_payment_methods(update, context, plan_id, None)


async def show_payment_methods(update: Update, context: ContextTypes.DEFAULT_TYPE, plan_id: int, promo_code=None):
    """To'lov turlarini ko'rsatish"""
    plan = await get_plan_by_id(plan_id)
    
    if not plan:
        if update.callback_query:
            await update.callback_query.answer("❌ Tarif topilmadi!", show_alert=True)
        return
    
    price = plan.price
    discount_text = ""
    
    if promo_code:
        # Promokod tekshirish va chegirma hisoblash
        discount_price = await get_discounted_price(promo_code, plan)
        if discount_price:
            price = discount_price
            discount_amount = plan.price - price
            discount_text = f"\n🎉 Promokod qo'llanildi!\n💸 Chegirma: {int(discount_amount):,} so'm\n\n"
    
    price_text = f"{int(price):,}".replace(',', ' ')
    original_price_text = f"{int(plan.price):,}".replace(',', ' ')
    
    text = f"💳 *To'lov*\n\n"
    text += f"📦 Tarif: *{plan.name}*\n"
    
    if promo_code and discount_text:
        text += f"💰 Asl narx: ~{original_price_text} so'm~\n"
        text += discount_text
        text += f"💰 To'lov summasi: *{price_text} so'm*\n"
    else:
        text += f"💰 Summa: *{price_text} so'm*\n"
    
    text += f"📅 Muddat: *{plan.duration_days} kun*\n\n"
    text += "To'lov turini tanlang:"
    
    keyboard = [
        [InlineKeyboardButton("💳 Click orqali to'lash", callback_data=f"pay_click_{plan.id}_{promo_code or 'none'}")],
        [InlineKeyboardButton("💳 Payme orqali to'lash", callback_data=f"pay_payme_{plan.id}_{promo_code or 'none'}")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="subscription_plans")]
    ]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def payment_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Click to'lov"""
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
    
    # Click to'lov havolasi
    click_url = f"{SITE_URL}/subscriptions/payment/{payment.id}/click/"
    
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
    """Payme to'lov"""
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
    
    # Payme to'lov havolasi
    payme_url = f"{SITE_URL}/subscriptions/payment/{payment.id}/payme/"
    
    price_text = f"{int(payment.final_amount):,}".replace(',', ' ')
    
    text = f"💳 *Payme orqali to'lov*\n\n"
    text += f"📦 Tarif: {plan.name}\n"
    
    if promo_code and payment.discount_amount > 0:
        original_price = f"{int(plan.price):,}".replace(',', ' ')
        discount = f"{int(payment.discount_amount):,}".replace(',', ' ')
        text += f"💰 Asl narx: ~{original_price} so'm~\n"
        text += f"🎉 Chegirma: {discount} so'm\n"
    
    text += f"💰 To'lov summasi: *{price_text} so'm*\n"
    text += f"📅 Muddat: {plan.duration_days} kun\n\n"
    text += "━━━━━━━━━━━━━━━\n\n"
    text += "Quyidagi tugmani bosib to'lovni amalga oshiring.\n"
    text += "To'lov muvaffaqiyatli bo'lgandan so'ng obuna avtomatik faollashadi."
    
    keyboard = [
        [InlineKeyboardButton("💳 Payme orqali to'lash", url=payme_url)],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="subscription_plans")]
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


async def handle_promo_code_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Promokod kiritilganda"""
    if 'waiting_promo_for_plan' not in context.user_data:
        return
    
    plan_id = context.user_data.pop('waiting_promo_for_plan')
    promo_code_text = update.message.text.strip().upper()
    
    user = await get_user_or_none(update.effective_user.id)
    if not user:
        return
    
    # Promokodni tekshirish
    promo_code = await get_promo_code(promo_code_text)
    plan = await get_plan_by_id(plan_id)
    
    if not plan:
        await update.message.reply_text("❌ Tarif topilmadi!")
        return
    
    if not promo_code:
        text = f"❌ *Promokod topilmadi*\n\n"
        text += f"Promokod: `{promo_code_text}`\n\n"
        text += "Iltimos, to'g'ri promokodni kiriting yoki promokodsiz davom eting."
        
        keyboard = [
            [InlineKeyboardButton("❌ Promokod yo'q", callback_data=f"no_promo_{plan_id}")],
            [InlineKeyboardButton("⬅️ Orqaga", callback_data="subscription_plans")]
        ]
        
        await update.message.reply_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    # Promokod to'g'ri - to'lov sahifasiga o'tish
    if not promo_code.is_valid():
        text = f"❌ *Promokod amal qilmaydi*\n\n"
        text += f"Promokod muddati tugagan yoki maksimal foydalanish limitiga yetgan.\n\n"
        text += "Iltimos, boshqa promokodni kiriting yoki promokodsiz davom eting."
        
        keyboard = [
            [InlineKeyboardButton("❌ Promokod yo'q", callback_data=f"no_promo_{plan_id}")],
            [InlineKeyboardButton("⬅️ Orqaga", callback_data="subscription_plans")]
        ]
        
        await update.message.reply_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    if promo_code.plan != plan:
        text = f"❌ *Promokod mos kelmaydi*\n\n"
        text += f"Bu promokod boshqa tarif uchun.\n\n"
        text += "Iltimos, to'g'ri promokodni kiriting yoki promokodsiz davom eting."
        
        keyboard = [
            [InlineKeyboardButton("❌ Promokod yo'q", callback_data=f"no_promo_{plan_id}")],
            [InlineKeyboardButton("⬅️ Orqaga", callback_data="subscription_plans")]
        ]
        
        await update.message.reply_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    # Promokod to'g'ri
    text = f"✅ *Promokod qo'llanildi!*\n\n"
    text += f"🎉 Promokod: `{promo_code_text}`\n\n"
    
    discount_price = promo_code.get_discounted_price()
    discount_amount = plan.price - discount_price
    
    original_price = f"{int(plan.price):,}".replace(',', ' ')
    discount_text = f"{int(discount_amount):,}".replace(',', ' ')
    final_price = f"{int(discount_price):,}".replace(',', ' ')
    
    text += f"💰 Asl narx: ~{original_price} so'm~\n"
    text += f"💸 Chegirma: {discount_text} so'm\n"
    text += f"💰 To'lov summasi: *{final_price} so'm*\n\n"
    text += "To'lov turini tanlang:"
    
    keyboard = [
        [InlineKeyboardButton("💳 Click orqali to'lash", callback_data=f"pay_click_{plan_id}_{promo_code_text}")],
        [InlineKeyboardButton("💳 Payme orqali to'lash", callback_data=f"pay_payme_{plan_id}_{promo_code_text}")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="subscription_plans")]
    ]
    
    await update.message.reply_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def register_handlers(app):
    """Subscription handlerlarini ro'yxatdan o'tkazish"""
    from telegram.ext import MessageHandler, filters
    
    app.add_handler(CallbackQueryHandler(subscription_plans_menu, pattern="^subscription_plans$"))
    app.add_handler(CallbackQueryHandler(plan_detail, pattern=r"^plan_detail_\d+$"))
    app.add_handler(CallbackQueryHandler(subscribe_to_plan, pattern=r"^subscribe_\d+$"))
    app.add_handler(CallbackQueryHandler(no_promo_code, pattern=r"^no_promo_\d+$"))
    app.add_handler(CallbackQueryHandler(payment_click, pattern=r"^pay_click_\d+"))
    app.add_handler(CallbackQueryHandler(payment_payme, pattern=r"^pay_payme_\d+"))
    app.add_handler(MessageHandler(filters.Regex("^💎 EduSelf Pro$"), handle_pro_text))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_promo_code_input))
