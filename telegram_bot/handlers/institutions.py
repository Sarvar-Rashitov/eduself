"""Ta'lim muassasalari handlerlari"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters, ConversationHandler, CommandHandler
from asgiref.sync import sync_to_async
from telegram_bot.keyboards import institutions_keyboard
from telegram_bot.decorators import require_subscription

SEARCH_INSTITUTION = 1


@sync_to_async
def get_institutions():
    from core.models import Institution
    return list(Institution.objects.filter(is_active=True).order_by('order', 'name'))


@sync_to_async
def get_institution(inst_id):
    from core.models import Institution
    try:
        return Institution.objects.get(id=inst_id, is_active=True)
    except Institution.DoesNotExist:
        return None


@sync_to_async
def get_institution_directions(inst):
    return list(inst.directions.filter(is_active=True).order_by('order', 'name'))


@sync_to_async
def search_institutions_db(query):
    from core.models import Institution
    institutions = list(Institution.objects.filter(
        is_active=True,
        name__icontains=query
    ).order_by('name')[:10])
    if not institutions:
        institutions = list(Institution.objects.filter(
            is_active=True,
            short_description__icontains=query
        ).order_by('name')[:10])
    return institutions


@sync_to_async
def get_institution_type_name(inst):
    from core.models import InstitutionType
    return dict(InstitutionType.choices).get(inst.institution_type, inst.institution_type)


@sync_to_async
def get_directions_count(inst):
    """Muassasadagi yo'nalishlar sonini olish"""
    return inst.directions.filter(is_active=True).count()


@sync_to_async
def get_contract_price_range(inst):
    """Kontrakt narxini olish"""
    return inst.get_contract_price_range()


@sync_to_async
def get_admission_period(inst):
    """Qabul muddatini olish"""
    return inst.get_admission_period()


@require_subscription("institutions")
async def institutions_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muassasalar menyusi"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        message = query.message
        edit = True
    else:
        message = update.message
        edit = False

    institutions = await get_institutions()

    if not institutions:
        text = "🏫 Hozircha muassasalar mavjud emas."
        if edit:
            await message.edit_text(text)
        else:
            await message.reply_text(text)
        return

    text = "🏫 *Ta'lim Muassasalari*\n\n"
    text += f"Jami: {len(institutions)} ta muassasa\n\n"
    text += "Muassasani tanlang yoki qidiring:"

    if edit:
        await message.edit_text(text, parse_mode='Markdown', reply_markup=institutions_keyboard(institutions))
    else:
        await message.reply_text(text, parse_mode='Markdown', reply_markup=institutions_keyboard(institutions))


async def institutions_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muassasalar sahifalash"""
    query = update.callback_query
    await query.answer()

    page = int(query.data.split('_')[-1])
    institutions = await get_institutions()

    await query.edit_message_reply_markup(reply_markup=institutions_keyboard(institutions, page))


async def institution_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muassasa tafsilotlari"""
    query = update.callback_query
    await query.answer()

    inst_id = int(query.data.split('_')[-1])

    inst = await get_institution(inst_id)
    if not inst:
        await query.edit_message_text("❌ Muassasa topilmadi.")
        return

    type_name = await get_institution_type_name(inst)

    text = f"🏫 *{inst.name}*\n\n"
    text += f"📋 Turi: {type_name}\n"

    if inst.short_description:
        text += f"\n📝 {inst.short_description}\n"

    if inst.address:
        text += f"\n📍 Manzil: {inst.address}\n"

    if inst.phone:
        text += f"📞 Tel: {inst.phone}\n"

    if inst.email:
        text += f"📧 Email: {inst.email}\n"

    if inst.website:
        text += f"🌐 Sayt: {inst.website}\n"

    price_range = await get_contract_price_range(inst)
    if price_range != "Narx ko'rsatilmagan":
        text += f"\n💰 Kontrakt: {price_range}\n"

    admission = await get_admission_period(inst)
    if admission != "Qabul muddati ko'rsatilmagan":
        text += f"📅 Qabul: {admission}\n"

    directions_count = await get_directions_count(inst)
    if directions_count > 0:
        text += f"\n📚 Yo'nalishlar: {directions_count} ta\n"

    keyboard = []

    if directions_count > 0:
        keyboard.append([InlineKeyboardButton(
            "📚 Yo'nalishlar",
            callback_data=f"inst_directions_{inst_id}"
        )])

    social_row = []
    if inst.telegram:
        social_row.append(InlineKeyboardButton("📱 Telegram", url=inst.telegram))
    if inst.instagram:
        social_row.append(InlineKeyboardButton("📷 Instagram", url=inst.instagram))
    if social_row:
        keyboard.append(social_row)

    if inst.website:
        keyboard.append([InlineKeyboardButton("🌐 Saytga o'tish", url=inst.website)])

    keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="institutions")])

    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def institution_directions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muassasa yo'nalishlari"""
    query = update.callback_query
    await query.answer()

    inst_id = int(query.data.split('_')[-1])

    inst = await get_institution(inst_id)
    if not inst:
        await query.edit_message_text("❌ Muassasa topilmadi.")
        return

    directions = await get_institution_directions(inst)

    text = f"📚 *{inst.name}*\n"
    text += f"*Yo'nalishlar:*\n\n"

    for i, direction in enumerate(directions, 1):
        text += f"{i}. *{direction.name}*\n"
        if direction.contract_price:
            text += f"   💰 {direction.contract_price:,.0f} so'm\n"
        text += f"   📖 {direction.get_education_language_display()}\n"
        text += f"   🎓 {direction.get_education_form_display()}\n"
        if direction.passing_score:
            text += f"   ✅ O'tish bali: {direction.passing_score}\n"
        text += "\n"

    if not directions:
        text += "Yo'nalishlar haqida ma'lumot yo'q."

    keyboard = [[InlineKeyboardButton("⬅️ Orqaga", callback_data=f"institution_{inst_id}")]]

    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def search_institutions_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muassasa qidirish boshlash"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🔍 *Muassasa qidirish*\n\n"
        "Muassasa nomini yoki kalit so'zni kiriting:\n\n"
        "_Bekor qilish uchun /cancel_",
        parse_mode='Markdown'
    )
    return SEARCH_INSTITUTION


async def search_institutions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muassasa qidirish"""
    search_query = update.message.text.strip()

    institutions = await search_institutions_db(search_query)

    if not institutions:
        await update.message.reply_text(
            f"❌ '{search_query}' bo'yicha muassasa topilmadi.\n"
            "Boshqa so'z bilan qidiring yoki /cancel buyrug'ini yuboring."
        )
        return SEARCH_INSTITUTION

    text = f"🔍 *'{search_query}' bo'yicha natijalar:*\n\n"
    text += f"Topildi: {len(institutions)} ta\n\n"

    keyboard = []
    for inst in institutions:
        keyboard.append([InlineKeyboardButton(
            f"🏫 {inst.name[:40]}",
            callback_data=f"institution_{inst.id}"
        )])
    keyboard.append([InlineKeyboardButton("🔍 Qayta qidirish", callback_data="search_institutions")])
    keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="institutions")])

    await update.message.reply_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return ConversationHandler.END


async def cancel_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Qidiruvni bekor qilish"""
    await update.message.reply_text("❌ Qidiruv bekor qilindi.")
    return ConversationHandler.END


async def handle_institutions_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muassasalar tugmasi"""
    if update.message.text == "🏫 Muassasalar":
        await institutions_menu(update, context)


def register_handlers(app):
    """Institution handlerlarini ro'yxatdan o'tkazish"""
    search_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(search_institutions_start, pattern="^search_institutions$")],
        states={
            SEARCH_INSTITUTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_institutions)]
        },
        fallbacks=[CommandHandler("cancel", cancel_search)],
        allow_reentry=True,
        per_message=False
    )

    app.add_handler(search_conv)
    app.add_handler(CallbackQueryHandler(institutions_menu, pattern="^institutions$"))
    app.add_handler(CallbackQueryHandler(institutions_page, pattern=r"^inst_page_\d+$"))
    app.add_handler(CallbackQueryHandler(institution_detail, pattern=r"^institution_\d+$"))
    app.add_handler(CallbackQueryHandler(institution_directions, pattern=r"^inst_directions_\d+$"))
    app.add_handler(MessageHandler(filters.Regex("^🏫 Muassasalar$"), handle_institutions_text))
