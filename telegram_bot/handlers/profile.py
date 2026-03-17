"""Profil handlerlari"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from asgiref.sync import sync_to_async
from telegram_bot.keyboards import profile_keyboard
from telegram_bot.utils import get_user_or_none
from telegram_bot.decorators import require_subscription


@sync_to_async
def get_user_stats(user):
    from core.models import TopicResult, CertificateResult, MockExamResult
    total_tests = TopicResult.objects.filter(user=user).count()
    total_tests += CertificateResult.objects.filter(user=user).count()
    total_tests += MockExamResult.objects.filter(user=user).count()

    passed_tests = TopicResult.objects.filter(user=user, passed=True).count()
    passed_tests += CertificateResult.objects.filter(user=user, passed=True).count()
    passed_tests += MockExamResult.objects.filter(user=user, passed=True).count()

    progress = int((passed_tests / total_tests) * 100) if total_tests > 0 else 0

    return {
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'progress': progress
    }


@sync_to_async
def get_user_subscription_info(user):
    """Foydalanuvchi obuna ma'lumotlarini olish"""
    subscription = user.get_active_subscription()
    lives_info = user.get_lives_info()
    
    return {
        'has_subscription': subscription is not None,
        'subscription': subscription,
        'lives_info': lives_info
    }


@sync_to_async
def get_user_position(user):
    from accounts.models import User
    if user.total_points > 0:
        higher_users = User.objects.filter(total_points__gt=user.total_points).count()
        return higher_users + 1
    return None


@sync_to_async
def get_test_history(user):
    from core.models import TopicResult, CertificateResult, MockExamResult
    results = []

    for r in TopicResult.objects.filter(user=user).select_related('topic').order_by('-completed_at')[:5]:
        results.append({
            'type': '📚',
            'title': r.topic.name[:25],
            'score': r.score,
            'passed': r.passed,
            'date': r.completed_at
        })

    for r in CertificateResult.objects.filter(user=user).select_related('test').order_by('-completed_at')[:5]:
        results.append({
            'type': '🏆',
            'title': r.test.title[:25],
            'score': r.score,
            'passed': r.passed,
            'date': r.completed_at
        })

    for r in MockExamResult.objects.filter(user=user).select_related('exam').order_by('-completed_at')[:5]:
        results.append({
            'type': '📝',
            'title': r.exam.title[:25],
            'score': r.score,
            'passed': r.passed,
            'date': r.completed_at
        })

    results.sort(key=lambda x: x['date'], reverse=True)
    return results[:10]


@require_subscription("profile")
async def profile_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Profil menyusi"""
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

    stats = await get_user_stats(user)
    position = await get_user_position(user)
    sub_info = await get_user_subscription_info(user)

    # Escape special characters for Markdown
    first_name = (user.first_name or user.username or "Foydalanuvchi").replace("_", "\\_")
    username = (user.username or "").replace("_", "\\_")
    email = (user.email or "").replace("_", "\\_")

    text = f"👤 *{first_name}*\n\n"
    if email:
        text += f"📧 Email: {email}\n"
    if username:
        text += f"📱 Username: @{username}\n"
    
    # Obuna ma'lumotlari
    text += f"\n━━━━━━━━━━━━━━━\n"
    text += f"💎 *Obuna:*\n"
    if sub_info['has_subscription']:
        sub = sub_info['subscription']
        end_date = sub.end_date.strftime('%d.%m.%Y')
        text += f"✅ {sub.plan.name}\n"
        text += f"📅 Tugash: {end_date}\n"
    else:
        text += f"❌ Faol obuna yo'q\n"
    
    # Lives ma'lumotlari
    lives = sub_info['lives_info']
    if lives['system_active']:
        if sub_info['has_subscription'] and sub_info['subscription'].plan.unlimited_lives:
            text += f"❤️ Yurakchalar: ♾️ Cheksiz\n"
        else:
            hearts = "❤️" * lives['current_lives'] + "🤍" * (lives['max_lives'] - lives['current_lives'])
            text += f"❤️ Yurakchalar: {hearts} ({lives['current_lives']}/{lives['max_lives']})\n"
            if lives['next_life_in'] and not lives['is_full']:
                minutes = int(lives['next_life_in'].total_seconds() / 60)
                text += f"⏱ Keyingi yurakcha: {minutes} daqiqada\n"
    
    text += f"\n━━━━━━━━━━━━━━━\n"
    text += f"📊 *Statistika:*\n\n"
    text += f"🏆 Umumiy XP: *{user.total_points}*\n"
    if position:
        text += f"🥇 Reyting: *{position}-o'rin*\n"
    text += f"📝 Yechilgan testlar: {stats['total_tests']}\n"
    text += f"✅ O'tilgan testlar: {stats['passed_tests']}\n"
    text += f"📈 Progress: {stats['progress']}%\n"

    if edit:
        await message.edit_text(text, parse_mode='Markdown', reply_markup=profile_keyboard(sub_info['has_subscription']))
    else:
        await message.reply_text(text, parse_mode='Markdown', reply_markup=profile_keyboard(sub_info['has_subscription']))


async def profile_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test tarixi"""
    query = update.callback_query
    await query.answer()

    user = await get_user_or_none(update.effective_user.id)
    if not user:
        return

    results = await get_test_history(user)

    text = f"📜 *Test Tarixi*\n\n"

    if results:
        for r in results:
            status = "✅" if r['passed'] else "❌"
            date_str = r['date'].strftime('%d.%m.%Y')
            text += f"{r['type']} {r['title']}\n"
            text += f"   {status} {r['score']}% | {date_str}\n\n"
    else:
        text += "Hali testlar yechilmagan."

    keyboard = [[InlineKeyboardButton("⬅️ Orqaga", callback_data="profile")]]

    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_profile_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Profil tugmasi"""
    if update.message.text == "👤 Profil":
        await profile_menu(update, context)


def register_handlers(app):
    """Profile handlerlarini ro'yxatdan o'tkazish"""
    app.add_handler(CallbackQueryHandler(profile_menu, pattern="^profile$"))
    app.add_handler(CallbackQueryHandler(profile_history, pattern="^profile_history$"))
    app.add_handler(MessageHandler(filters.Regex("^👤 Profil$"), handle_profile_text))
