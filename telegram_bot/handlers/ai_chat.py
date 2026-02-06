"""AI Hamroh handlerlari"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters, ConversationHandler, CommandHandler
from telegram_bot.keyboards import ai_chat_keyboard, main_menu_keyboard
from telegram_bot.decorators import require_subscription

AI_CHAT = 1


@require_subscription("ai")
async def ai_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """AI Hamroh menyusi"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        message = query.message
        edit = True
    else:
        message = update.message
        edit = False

    text = "🤖 *AI Hamroh*\n\n"
    text += "Men sizga har qanday savollaringizga javob bera olaman:\n\n"
    text += "📚 Fanlar bo'yicha savollar\n"
    text += "🏫 Ta'lim muassasalarini tanlash\n"
    text += "🏆 Sertifikatlar haqida ma'lumot\n"
    text += "📝 Test va imtihonlarga tayyorgarlik\n\n"
    text += "Savol berish uchun tugmani bosing:"

    if edit:
        await message.edit_text(text, parse_mode='Markdown', reply_markup=ai_chat_keyboard())
    else:
        await message.reply_text(text, parse_mode='Markdown', reply_markup=ai_chat_keyboard())


async def start_ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """AI chat boshlash"""
    query = update.callback_query
    await query.answer()

    context.user_data['ai_mode'] = True

    await query.edit_message_text(
        "💬 *Savol berish*\n\n"
        "Savolingizni yozing, men javob beraman!\n\n"
        "Suhbatni tugatish uchun /stop buyrug'ini yuboring.",
        parse_mode='Markdown'
    )
    return AI_CHAT


async def handle_ai_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """AI xabarini qayta ishlash"""
    user_message = update.message.text

    await update.message.chat.send_action('typing')

    try:
        from ai_assistant.services import DeepSeekAIService
        ai_service = DeepSeekAIService()

        chat_history = context.user_data.get('ai_history', [])

        response = ai_service.generate_response(
            user_message=user_message,
            chat_history=chat_history,
            context_data={}
        )

        ai_response = response.get('content', 'Kechirasiz, javob berishda xatolik yuz berdi.')

        chat_history.append({'role': 'user', 'content': user_message})
        chat_history.append({'role': 'assistant', 'content': ai_response})

        context.user_data['ai_history'] = chat_history[-10:]

        ai_response = ai_response.replace('**', '*')

        keyboard = [
            [InlineKeyboardButton("🔄 Yangi savol", callback_data="ai_continue")],
            [InlineKeyboardButton("🏠 Asosiy menyu", callback_data="main_menu")]
        ]

        if len(ai_response) > 4000:
            parts = [ai_response[i:i+4000] for i in range(0, len(ai_response), 4000)]
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    await update.message.reply_text(
                        part,
                        parse_mode='Markdown',
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    )
                else:
                    await update.message.reply_text(part, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                ai_response,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        return AI_CHAT

    except Exception as e:
        await update.message.reply_text(
            f"❌ Xatolik yuz berdi. Qayta urinib ko'ring.\n\n"
            f"Suhbatni tugatish uchun /stop",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Qayta urinish", callback_data="ai_new_chat")]
            ])
        )
        return AI_CHAT


async def ai_continue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """AI suhbatni davom ettirish"""
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "💬 Keyingi savolingizni yozing:",
        parse_mode='Markdown'
    )
    return AI_CHAT


async def stop_ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """AI chatni to'xtatish"""
    context.user_data.pop('ai_mode', None)
    context.user_data.pop('ai_history', None)

    await update.message.reply_text(
        "✅ AI suhbat yakunlandi.\n\n"
        "Asosiy menyuga qaytish uchun tugmani bosing:",
        reply_markup=main_menu_keyboard()
    )
    return ConversationHandler.END


async def handle_ai_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """AI Hamroh tugmasi"""
    if update.message.text == "🤖 AI Hamroh":
        await ai_menu(update, context)


async def end_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Suhbatni tugatish"""
    return ConversationHandler.END


def register_handlers(app):
    """AI handlerlarini ro'yxatdan o'tkazish"""
    ai_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_ai_chat, pattern="^ai_new_chat$"),
        ],
        states={
            AI_CHAT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ai_message),
                CallbackQueryHandler(ai_continue, pattern="^ai_continue$"),
            ]
        },
        fallbacks=[
            CommandHandler("stop", stop_ai_chat),
            CallbackQueryHandler(end_conversation, pattern="^main_menu$")
        ],
        allow_reentry=True,
        per_message=False
    )

    app.add_handler(ai_conv)
    app.add_handler(CallbackQueryHandler(ai_menu, pattern="^ai_chat$"))
    app.add_handler(MessageHandler(filters.Regex("^🤖 AI Hamroh$"), handle_ai_text))
