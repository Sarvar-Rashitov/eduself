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
def get_user_position(user):
    from accounts.models import User
    if user.total_points > 0:
        higher_users = User.objects.filter(total_points__gt=user.total_points).count()
        return higher_users + 1
    return None


@sync_to_async
def get_detailed_stats(user):
    from core.models import TopicResult, CertificateResult, MockExamResult
    from django.db.models import Avg

    regular_tests = TopicResult.objects.filter(user=user).count()
    regular_passed = TopicResult.objects.filter(user=user, passed=True).count()

    cert_tests = CertificateResult.objects.filter(user=user).count()
    cert_passed = CertificateResult.objects.filter(user=user, passed=True).count()

    mock_tests = MockExamResult.objects.filter(user=user).count()
    mock_passed = MockExamResult.objects.filter(user=user, passed=True).count()

    avg_score = TopicResult.objects.filter(user=user).aggregate(avg=Avg('score'))['avg'] or 0

    return {
        'regular_tests': regular_tests,
        'regular_passed': regular_passed,
        'cert_tests': cert_tests,
        'cert_passed': cert_passed,
        'mock_tests': mock_tests,
        'mock_passed': mock_passed,
        'avg_score': avg_score
    }


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


@sync_to_async
def get_top_users():
    from accounts.models import User
    return list(User.objects.filter(total_points__gt=0).order_by('-total_points')[:20])


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

    # Escape special characters for Markdown
    first_name = (user.first_name or user.username or "Foydalanuvchi").replace("_", "\\_")
    username = (user.username or "").replace("_", "\\_")
    email = (user.email or "").replace("_", "\\_")

    text = f"👤 *{first_name}*\n\n"
    if email:
        text += f"📧 Email: {email}\n"
    if username:
        text += f"📱 Username: @{username}\n"
    text += f"\n━━━━━━━━━━━━━━━\n"
    text += f"📊 *Statistika:*\n\n"
    text += f"🏆 Umumiy ball: *{user.total_points}*\n"
    if position:
        text += f"🥇 Reyting: *{position}-o'rin*\n"
    text += f"📝 Yechilgan testlar: {stats['total_tests']}\n"
    text += f"✅ O'tilgan testlar: {stats['passed_tests']}\n"
    text += f"📈 Progress: {stats['progress']}%\n"

    if edit:
        await message.edit_text(text, parse_mode='Markdown', reply_markup=profile_keyboard())
    else:
        await message.reply_text(text, parse_mode='Markdown', reply_markup=profile_keyboard())


async def profile_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Batafsil statistika"""
    query = update.callback_query
    await query.answer()

    user = await get_user_or_none(update.effective_user.id)
    if not user:
        return

    stats = await get_detailed_stats(user)

    text = f"📊 *Batafsil Statistika*\n\n"
    text += f"👤 {user.first_name or user.username}\n"
    text += f"━━━━━━━━━━━━━━━\n\n"

    text += f"📚 *Oddiy testlar:*\n"
    text += f"   Yechilgan: {stats['regular_tests']}\n"
    text += f"   O'tilgan: {stats['regular_passed']}\n\n"

    text += f"🏆 *Sertifikat testlari:*\n"
    text += f"   Yechilgan: {stats['cert_tests']}\n"
    text += f"   O'tilgan: {stats['cert_passed']}\n\n"

    text += f"📝 *Mock imtihonlar:*\n"
    text += f"   Yechilgan: {stats['mock_tests']}\n"
    text += f"   O'tilgan: {stats['mock_passed']}\n\n"

    text += f"━━━━━━━━━━━━━━━\n"
    text += f"📈 O'rtacha ball: {stats['avg_score']:.1f}%\n"
    text += f"🏆 Umumiy ball: {user.total_points}\n"

    keyboard = [[InlineKeyboardButton("⬅️ Orqaga", callback_data="profile")]]

    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


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


@require_subscription("leaderboard")
async def global_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Global reyting"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        message = query.message
        edit = True
    else:
        message = update.message
        edit = False

    current_user = await get_user_or_none(update.effective_user.id)
    top_users = await get_top_users()

    text = "🏆 *Global Reyting*\n\n"

    medals = ['🥇', '🥈', '🥉']
    for i, user in enumerate(top_users):
        medal = medals[i] if i < 3 else f"{i+1}."
        name = user.first_name or user.username

        if current_user and user.id == current_user.id:
            text += f"*{medal} {name}: {user.total_points} ball* ⬅️\n"
        else:
            text += f"{medal} {name}: {user.total_points} ball\n"

    if not top_users:
        text += "Hali natijalar yo'q."

    if current_user and current_user.total_points > 0:
        position = await get_user_position(current_user)
        if position and position > 20:
            text += f"\n━━━━━━━━━━━━━━━\n"
            text += f"*Sizning o'rningiz: {position}*\n"
            text += f"Ball: {current_user.total_points}\n"

    keyboard = [[InlineKeyboardButton("🏠 Asosiy menyu", callback_data="main_menu")]]

    if edit:
        await message.edit_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_profile_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Profil tugmasi"""
    if update.message.text == "👤 Profil":
        await profile_menu(update, context)


async def handle_leaderboard_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reyting tugmasi"""
    if update.message.text == "📊 Reyting":
        await global_leaderboard(update, context)


def register_handlers(app):
    """Profile handlerlarini ro'yxatdan o'tkazish"""
    app.add_handler(CallbackQueryHandler(profile_menu, pattern="^profile$"))
    app.add_handler(CallbackQueryHandler(profile_stats, pattern="^profile_stats$"))
    app.add_handler(CallbackQueryHandler(profile_history, pattern="^profile_history$"))
    app.add_handler(CallbackQueryHandler(global_leaderboard, pattern="^leaderboard$"))
    app.add_handler(MessageHandler(filters.Regex("^👤 Profil$"), handle_profile_text))
    app.add_handler(MessageHandler(filters.Regex("^📊 Reyting$"), handle_leaderboard_text))
