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
    """Profil menyusi - zamonaviy dizayn"""
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

    # Profil header
    text = f"╔═══════════════════╗\n"
    text += f"    👤 *PROFIL*\n"
    text += f"╚═══════════════════╝\n\n"
    
    text += f"🎯 *{first_name}*\n"
    if username:
        text += f"📱 @{username}\n"
    if email:
        text += f"📧 {email}\n"
    
    text += f"\n╭─────────────────╮\n"
    text += f"│  💎 OBUNA HOLATI  │\n"
    text += f"╰─────────────────╯\n\n"
    
    # Obuna ma'lumotlari
    if sub_info['has_subscription']:
        sub = sub_info['subscription']
        end_date = sub.end_date.strftime('%d.%m.%Y')
        text += f"✅ *{sub.plan.name}*\n"
        text += f"📅 Tugash: {end_date}\n"
        
        # Lives ma'lumotlari
        lives = sub_info['lives_info']
        if lives['system_active']:
            if sub.plan.unlimited_lives:
                text += f"❤️ Yurakchalar: ♾️ *Cheksiz*\n"
            else:
                hearts = "❤️" * lives['current_lives'] + "🤍" * (lives['max_lives'] - lives['current_lives'])
                text += f"❤️ {hearts}\n"
                text += f"   {lives['current_lives']}/{lives['max_lives']}\n"
                if lives['next_life_in'] and not lives['is_full']:
                    minutes = int(lives['next_life_in'].total_seconds() / 60)
                    text += f"⏱ Keyingi: {minutes} daq\n"
    else:
        text += f"❌ *Faol obuna yo'q*\n"
        text += f"💡 Pro obuna bilan cheksiz imkoniyatlar!\n"
        
        # Lives ma'lumotlari
        lives = sub_info['lives_info']
        if lives['system_active']:
            hearts = "❤️" * lives['current_lives'] + "🤍" * (lives['max_lives'] - lives['current_lives'])
            text += f"\n❤️ {hearts}\n"
            text += f"   {lives['current_lives']}/{lives['max_lives']}\n"
            if lives['next_life_in'] and not lives['is_full']:
                minutes = int(lives['next_life_in'].total_seconds() / 60)
                text += f"⏱ Keyingi: {minutes} daq\n"
    
    text += f"\n╭─────────────────╮\n"
    text += f"│  📊 STATISTIKA   │\n"
    text += f"╰─────────────────╯\n\n"
    
    # Statistika
    text += f"🏆 XP: *{user.total_points:,}*\n"
    if position:
        text += f"🥇 Reyting: *#{position}*\n"
    
    # Progress bar
    progress_bar = "█" * (stats['progress'] // 10) + "░" * (10 - stats['progress'] // 10)
    text += f"\n📈 Progress: {stats['progress']}%\n"
    text += f"[{progress_bar}]\n\n"
    
    text += f"📝 Testlar: {stats['total_tests']}\n"
    text += f"✅ O'tilgan: {stats['passed_tests']}\n"
    
    if stats['total_tests'] > 0:
        success_rate = int((stats['passed_tests'] / stats['total_tests']) * 100)
        text += f"🎯 Muvaffaqiyat: {success_rate}%\n"

    if edit:
        await message.edit_text(text, parse_mode='Markdown', reply_markup=profile_keyboard(sub_info['has_subscription']))
    else:
        await message.reply_text(text, parse_mode='Markdown', reply_markup=profile_keyboard(sub_info['has_subscription']))


async def profile_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test tarixi - zamonaviy dizayn"""
    query = update.callback_query
    await query.answer()

    user = await get_user_or_none(update.effective_user.id)
    if not user:
        return

    results = await get_test_history(user)

    text = f"╔═══════════════════╗\n"
    text += f"   📜 TEST TARIXI\n"
    text += f"╚═══════════════════╝\n\n"

    if results:
        for idx, r in enumerate(results, 1):
            status = "✅" if r['passed'] else "❌"
            date_str = r['date'].strftime('%d.%m.%Y')
            
            # Score bar
            score_bars = int(r['score'] / 10)
            score_visual = "█" * score_bars + "░" * (10 - score_bars)
            
            text += f"{idx}. {r['type']} *{r['title']}*\n"
            text += f"   {status} {r['score']}% [{score_visual}]\n"
            text += f"   📅 {date_str}\n\n"
    else:
        text += "📭 Hali testlar yechilmagan.\n\n"
        text += "💡 Fanlar bo'limidan test yechishni boshlang!"

    keyboard = [[InlineKeyboardButton("⬅️ Profilga qaytish", callback_data="profile")]]

    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


async def subscription_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Obuna ma'lumotlari"""
    query = update.callback_query
    await query.answer()

    user = await get_user_or_none(update.effective_user.id)
    if not user:
        return

    sub_info = await get_user_subscription_info(user)

    text = f"╔═══════════════════╗\n"
    text += f"  💎 OBUNA MA'LUMOTLARI\n"
    text += f"╚═══════════════════╝\n\n"

    if sub_info['has_subscription']:
        sub = sub_info['subscription']
        start_date = sub.start_date.strftime('%d.%m.%Y')
        end_date = sub.end_date.strftime('%d.%m.%Y')
        
        text += f"✅ *Faol obuna*\n\n"
        text += f"📦 Tarif: *{sub.plan.name}*\n"
        text += f"📅 Boshlanish: {start_date}\n"
        text += f"📅 Tugash: {end_date}\n\n"
        
        # Qolgan kunlar
        from django.utils import timezone
        days_left = (sub.end_date - timezone.now()).days
        if days_left > 0:
            text += f"⏳ Qolgan: *{days_left} kun*\n\n"
        
        text += f"╭─────────────────╮\n"
        text += f"│  🎁 IMKONIYATLAR  │\n"
        text += f"╰─────────────────╯\n\n"
        
        if sub.plan.unlimited_lives:
            text += f"♾️ Cheksiz yurakchalar\n"
        
        if sub.plan.ai_analysis_limit == -1:
            text += f"🤖 Cheksiz AI tahlil\n"
        else:
            used = sub.ai_analysis_used
            limit = sub.plan.ai_analysis_limit
            text += f"🤖 AI tahlil: {used}/{limit}\n"
        
        if sub.plan.ai_companion_limit == -1:
            text += f"💬 Cheksiz AI yordamchi\n"
        else:
            used = sub.ai_companion_used
            limit = sub.plan.ai_companion_limit
            text += f"💬 AI yordamchi: {used}/{limit}\n"
        
        if sub.plan.university_exam_limit == -1:
            text += f"🏆 Cheksiz universitet imtihonlari\n"
        else:
            used = sub.university_exam_used
            limit = sub.plan.university_exam_limit
            text += f"🏆 Universitet: {used}/{limit}\n"
        
        if sub.plan.mock_exam_limit == -1:
            text += f"📝 Cheksiz mock imtihonlar\n"
        else:
            used = sub.mock_exam_used
            limit = sub.plan.mock_exam_limit
            text += f"📝 Mock: {used}/{limit}\n"
        
        if sub.plan.certificate_test_limit == -1:
            text += f"🎓 Cheksiz sertifikat testlari\n"
        else:
            used = sub.certificate_test_used
            limit = sub.plan.certificate_test_limit
            text += f"🎓 Sertifikat: {used}/{limit}\n"
        
        text += f"🔓 Barcha mavzular ochiq\n"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Obunani yangilash", callback_data="subscription_plans")],
            [InlineKeyboardButton("⬅️ Profilga qaytish", callback_data="profile")]
        ]
    else:
        text += f"❌ *Faol obuna yo'q*\n\n"
        text += f"💡 Pro obuna bilan quyidagi imkoniyatlarga ega bo'ling:\n\n"
        text += f"♾️ Cheksiz yurakchalar\n"
        text += f"🔓 Barcha mavzular ochiq\n"
        text += f"🤖 AI tahlil va yordamchi\n"
        text += f"🏆 Universitet imtihonlari\n"
        text += f"📝 Mock imtihonlar\n"
        text += f"🎓 Sertifikat testlari\n"
        
        keyboard = [
            [InlineKeyboardButton("✨ Pro obuna olish", callback_data="subscription_plans")],
            [InlineKeyboardButton("⬅️ Profilga qaytish", callback_data="profile")]
        ]

    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_profile_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Profil tugmasi"""
    if update.message.text == "👤 Profil":
        await profile_menu(update, context)


def register_handlers(app):
    """Profile handlerlarini ro'yxatdan o'tkazish"""
    app.add_handler(CallbackQueryHandler(profile_menu, pattern="^profile$"))
    app.add_handler(CallbackQueryHandler(profile_history, pattern="^profile_history$"))
    app.add_handler(CallbackQueryHandler(subscription_info, pattern="^subscription_info$"))
    app.add_handler(MessageHandler(filters.Regex("^👤 Profil$"), handle_profile_text))
