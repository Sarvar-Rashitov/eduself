"""Fanlar handlerlari"""
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from asgiref.sync import sync_to_async
from telegram_bot.keyboards import subjects_keyboard, topics_keyboard, tests_keyboard
from telegram_bot.utils import get_user_or_none
from telegram_bot.decorators import require_subscription


@sync_to_async
def get_subjects():
    from core.models import Subject
    return list(Subject.objects.filter(is_active=True).order_by('order', 'name'))


@sync_to_async
def get_subject(subject_id):
    from core.models import Subject
    try:
        return Subject.objects.get(id=subject_id, is_active=True)
    except Subject.DoesNotExist:
        return None


@sync_to_async
def get_topics(subject):
    return list(subject.topics.filter(is_active=True).order_by('order', 'name'))


@sync_to_async
def get_topic(topic_id):
    from core.models import Topic
    try:
        return Topic.objects.select_related('subject').get(id=topic_id, is_active=True)
    except Topic.DoesNotExist:
        return None


@sync_to_async
def get_tests(topic, user):
    tests = list(topic.tests.filter(is_active=True).order_by('order', 'created_at'))
    for test in tests:
        test.is_unlocked = test.is_unlocked_for_user(user) if user else False
    return tests


@sync_to_async
def get_tests_count(subject):
    return subject.get_tests_count()


@require_subscription("subjects")
async def subjects_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fanlar menyusi"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        message = query.message
        edit = True
    else:
        message = update.message
        edit = False

    subjects = await get_subjects()

    if not subjects:
        text = "📚 Hozircha fanlar mavjud emas."
        if edit:
            await message.edit_text(text)
        else:
            await message.reply_text(text)
        return

    text = "📚 *Fanlar ro'yxati*\n\nO'rganmoqchi bo'lgan fanni tanlang:"

    if edit:
        await message.edit_text(text, parse_mode='Markdown', reply_markup=subjects_keyboard(subjects))
    else:
        await message.reply_text(text, parse_mode='Markdown', reply_markup=subjects_keyboard(subjects))


async def subjects_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fanlar sahifalash"""
    query = update.callback_query
    await query.answer()

    page = int(query.data.split('_')[-1])
    subjects = await get_subjects()

    await query.edit_message_reply_markup(reply_markup=subjects_keyboard(subjects, page))


async def subject_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fan tafsilotlari"""
    query = update.callback_query
    await query.answer()

    subject_id = int(query.data.split('_')[-1])

    subject = await get_subject(subject_id)
    if not subject:
        await query.edit_message_text("❌ Fan topilmadi.")
        return

    topics = await get_topics(subject)
    tests_count = await get_tests_count(subject)

    text = f"📖 *{subject.name}*\n\n"
    if subject.description:
        text += f"{subject.description}\n\n"
    text += f"📑 Mavzular soni: {len(topics)}\n"
    text += f"📝 Testlar soni: {tests_count}\n\n"
    text += "Mavzuni tanlang:"

    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=topics_keyboard(topics, subject_id)
    )


async def topic_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mavzu tafsilotlari"""
    query = update.callback_query
    await query.answer()

    user = await get_user_or_none(update.effective_user.id)
    topic_id = int(query.data.split('_')[-1])

    topic = await get_topic(topic_id)
    if not topic:
        await query.edit_message_text("❌ Mavzu topilmadi.")
        return

    tests = await get_tests(topic, user)

    text = f"📑 *{topic.name}*\n\n"
    text += f"📖 Fan: {topic.subject.name}\n"
    text += f"📝 Testlar soni: {len(tests)}\n\n"
    text += "Testni tanlang:"

    context.user_data['current_topic_id'] = topic_id

    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=tests_keyboard(tests, topic_id)
    )


async def handle_subjects_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fanlar tugmasi bosilganda"""
    if update.message.text == "📚 Fanlar":
        await subjects_menu(update, context)


def register_handlers(app):
    """Subject handlerlarini ro'yxatdan o'tkazish"""
    app.add_handler(CallbackQueryHandler(subjects_menu, pattern="^subjects$"))
    app.add_handler(CallbackQueryHandler(subjects_page, pattern=r"^subjects_page_\d+$"))
    app.add_handler(CallbackQueryHandler(subject_detail, pattern=r"^subject_\d+$"))
    app.add_handler(CallbackQueryHandler(topic_detail, pattern=r"^topic_\d+$"))
    app.add_handler(MessageHandler(filters.Regex("^📚 Fanlar$"), handle_subjects_text))
