"""Test handlerlari"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from asgiref.sync import sync_to_async
from telegram_bot.keyboards import test_start_keyboard, main_menu_keyboard
from telegram_bot.utils import get_user_or_none
import time
import asyncio


@sync_to_async
def get_test(test_id):
    from core.models import Test
    try:
        return Test.objects.select_related('topic').get(id=test_id, is_active=True)
    except Test.DoesNotExist:
        return None


@sync_to_async
def get_test_questions(test):
    return list(test.questions.all().prefetch_related('answers').order_by('order'))


@sync_to_async
def get_question(question_id):
    from core.models import Question
    return Question.objects.prefetch_related('answers').get(id=question_id)


@sync_to_async
def get_answer(answer_id, question):
    from core.models import Answer
    return Answer.objects.get(id=answer_id, question=question)


@sync_to_async
def get_correct_answer(question):
    return question.answers.filter(is_correct=True).first()


@sync_to_async
def is_test_unlocked(test, user):
    return test.is_unlocked_for_user(user)


@sync_to_async
def get_best_result(user, test):
    from core.models import TestResult
    return TestResult.objects.filter(user=user, test=test).order_by('-score').first()


@sync_to_async
def get_questions_count(test):
    return test.get_questions_count()


@sync_to_async
def get_max_points(test):
    return test.get_max_points()


@sync_to_async
def save_test_result(user, test, score, total, correct, passed, time_taken, earned_points, answers):
    from core.models import TestResult
    TestResult.objects.create(
        user=user, test=test, score=score, total_questions=total,
        correct_answers=correct, passed=passed, time_taken=time_taken,
        earned_points=earned_points, user_answers=answers
    )
    user.total_points += earned_points
    user.save()


@sync_to_async
def get_test_leaderboard(test):
    from core.models import TestResult
    from django.db.models import Max
    return list(TestResult.objects.filter(test=test).values(
        'user__username', 'user__first_name'
    ).annotate(best_score=Max('earned_points')).order_by('-best_score')[:10])


def test_keyboard():
    """Test vaqtidagi menyu"""
    keyboard = [
        [KeyboardButton("⏭ Keyingisi"), KeyboardButton("⏩ O'tkazib yuborish")],
        [KeyboardButton("🏁 Yakunlash"), KeyboardButton("🏠 Asosiy menyu")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def format_timer(seconds):
    """Vaqtni formatlash"""
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"


async def test_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test tafsilotlari"""
    query = update.callback_query
    await query.answer()

    user = await get_user_or_none(update.effective_user.id)
    test_id = int(query.data.split('_')[-1])

    test = await get_test(test_id)
    if not test:
        await query.edit_message_text("❌ Test topilmadi.")
        return

    if user:
        is_unlocked = await is_test_unlocked(test, user)
        if not is_unlocked:
            await query.answer("🔒 Bu test hali ochilmagan!", show_alert=True)
            return

    best_result = await get_best_result(user, test) if user else None
    questions_count = await get_questions_count(test)
    max_points = await get_max_points(test)

    text = f"📝 *{test.title}*\n\n"
    text += f"📑 Mavzu: {test.topic.name}\n"
    text += f"❓ Savollar: {questions_count} ta\n"
    text += f"⏱ Vaqt: {test.time_limit} daqiqa\n"
    text += f"✅ O'tish balli: {test.passing_score}%\n"
    text += f"🏆 Maksimal ball: {max_points}\n\n"

    if best_result:
        status = "✅ O'tdi" if best_result.passed else "❌ O'tmadi"
        text += f"📊 *Sizning eng yaxshi natijangiz:*\n"
        text += f"Ball: {best_result.score}% {status}\n"
        text += f"To'g'ri javoblar: {best_result.correct_answers}/{best_result.total_questions}\n"

    context.user_data['current_test_id'] = test_id

    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=test_start_keyboard(test_id)
    )


async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Testni boshlash"""
    query = update.callback_query
    await query.answer()

    user = await get_user_or_none(update.effective_user.id)
    if not user:
        await query.answer("❌ Xatolik yuz berdi!", show_alert=True)
        return

    test_id = int(query.data.split('_')[-1])
    test = await get_test(test_id)
    if not test:
        await query.edit_message_text("❌ Test topilmadi.")
        return

    questions = await get_test_questions(test)
    if not questions:
        await query.answer("❌ Bu testda savollar yo'q!", show_alert=True)
        return

    # Test sessiyasini boshlash
    context.user_data['test_session'] = {
        'test_id': test_id,
        'test_type': 'regular',
        'questions': [q.id for q in questions],
        'current_index': 0,
        'answers': {},
        'start_time': time.time(),
        'time_limit': test.time_limit * 60,  # sekundlarda
        'correct_count': 0,
        'earned_points': 0
    }

    # Eski xabarni o'chirish
    await query.message.delete()

    # Test menyusini ko'rsatish
    await query.message.reply_text(
        "📝 Test boshlandi!\n\nJavobni tanlash uchun A, B, C, D harflarini yuboring.",
        reply_markup=test_keyboard()
    )

    # Birinchi savolni ko'rsatish
    await show_question(update, context, questions[0], 1, len(questions))


async def show_question(update: Update, context: ContextTypes.DEFAULT_TYPE, question, num: int, total: int):
    """Savolni ko'rsatish"""
    session = context.user_data.get('test_session')
    if not session:
        return

    answers = list(question.answers.all())
    
    # Qolgan vaqtni hisoblash
    elapsed = time.time() - session['start_time']
    remaining = max(0, session['time_limit'] - elapsed)
    timer_str = format_timer(int(remaining))

    text = f"⏱ *Vaqt: {timer_str}*\n\n"
    text += f"❓ *Savol {num}/{total}*\n\n"
    text += f"{question.text}\n\n"
    
    # Javob variantlari
    for i, answer in enumerate(answers):
        letter = chr(65 + i)  # A, B, C, D
        text += f"*{letter})* {answer.text}\n"
    
    text += f"\n💎 Ball: {question.points}"

    # Javob variantlarini saqlash
    context.user_data['current_answers'] = {chr(65 + i): ans.id for i, ans in enumerate(answers)}
    context.user_data['current_question'] = question

    # Callback query yoki message ekanligini aniqlash
    if update.callback_query:
        message = update.callback_query.message
    else:
        message = update.message

    await message.reply_text(text, parse_mode='Markdown')


async def handle_test_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test javobini qabul qilish (A, B, C, D)"""
    session = context.user_data.get('test_session')
    if not session or session.get('test_type') != 'regular':
        return

    user_answer = update.message.text.upper().strip()
    
    # Faqat A, B, C, D qabul qilish
    if user_answer not in ['A', 'B', 'C', 'D']:
        return

    current_answers = context.user_data.get('current_answers', {})
    current_question = context.user_data.get('current_question')
    
    if not current_answers or not current_question or user_answer not in current_answers:
        await update.message.reply_text("❌ Javob topilmadi. Qaytadan urinib ko'ring.")
        return

    answer_id = current_answers[user_answer]

    try:
        answer = await get_answer(answer_id, current_question)
        correct_answer = await get_correct_answer(current_question)

        # Javobni saqlash
        session['answers'][str(current_question.id)] = {
            'answer_id': answer_id,
            'is_correct': answer.is_correct
        }

        if answer.is_correct:
            session['correct_count'] += 1
            session['earned_points'] += current_question.points
            result_text = "✅ To'g'ri!"
        else:
            correct_letter = None
            for letter, ans_id in current_answers.items():
                if correct_answer and ans_id == correct_answer.id:
                    correct_letter = letter
                    break
            result_text = f"❌ Noto'g'ri! To'g'ri javob: {correct_letter}"

        await update.message.reply_text(result_text)

        # Keyingi savol
        await next_question(update, context)

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {str(e)}")


async def next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Keyingi savolga o'tish"""
    session = context.user_data.get('test_session')
    if not session:
        return

    session['current_index'] += 1

    if session['current_index'] < len(session['questions']):
        next_question_id = session['questions'][session['current_index']]
        question = await get_question(next_question_id)
        await show_question(
            update, context, question,
            session['current_index'] + 1,
            len(session['questions'])
        )
    else:
        await finish_test(update, context)


async def skip_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Savolni o'tkazib yuborish"""
    session = context.user_data.get('test_session')
    if not session:
        await update.message.reply_text("❌ Faol test topilmadi.")
        return

    current_question = context.user_data.get('current_question')
    if current_question:
        # Javobsiz saqlash
        session['answers'][str(current_question.id)] = {
            'answer_id': None,
            'is_correct': False,
            'skipped': True
        }

    await update.message.reply_text("⏩ Savol o'tkazib yuborildi")
    await next_question(update, context)


async def finish_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Testni yakunlash"""
    session = context.user_data.get('test_session')
    if not session:
        await update.message.reply_text("❌ Faol test topilmadi.", reply_markup=main_menu_keyboard())
        return

    user = await get_user_or_none(update.effective_user.id)
    test = await get_test(session['test_id'])

    total = len(session['questions'])
    correct = session['correct_count']
    score = int((correct / total) * 100) if total > 0 else 0
    passed = score >= test.passing_score
    time_taken = int(time.time() - session['start_time'])

    # Natijani saqlash
    if user:
        await save_test_result(
            user, test, score, total, correct, passed,
            time_taken, session['earned_points'], session['answers']
        )

    status = "✅ O'TDINGIZ!" if passed else "❌ O'TMADINGIZ"

    text = f"🏁 *Test yakunlandi!*\n\n"
    text += f"📝 Test: {test.title}\n"
    text += f"━━━━━━━━━━━━━━━\n"
    text += f"📊 *Natija: {status}*\n\n"
    text += f"✅ To'g'ri javoblar: {correct}/{total}\n"
    text += f"📈 Ball: {score}%\n"
    text += f"🏆 Olingan ball: {session['earned_points']}\n"
    text += f"⏱ Sarflangan vaqt: {time_taken // 60}:{time_taken % 60:02d}\n"

    if passed:
        text += "\n🎉 Tabriklaymiz! Keyingi test ochildi!"
    else:
        text += f"\n💪 O'tish uchun {test.passing_score}% kerak. Qayta urinib ko'ring!"

    # Sessiyani tozalash
    context.user_data.pop('test_session', None)
    context.user_data.pop('current_answers', None)
    context.user_data.pop('current_question', None)

    keyboard = [
        [InlineKeyboardButton("🔄 Qayta yechish", callback_data=f"start_test_{test.id}")],
        [InlineKeyboardButton("🏆 Reyting", callback_data=f"test_leaderboard_{test.id}")],
        [InlineKeyboardButton("⬅️ Mavzuga qaytish", callback_data=f"topic_{test.topic.id}")]
    ]

    await update.message.reply_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    # Asosiy menyuni qaytarish
    await update.message.reply_text("Menyu:", reply_markup=main_menu_keyboard())


async def handle_test_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test menyu tugmalarini qayta ishlash"""
    text = update.message.text
    session = context.user_data.get('test_session')

    if text == "⏭ Keyingisi":
        if session:
            await next_question(update, context)
        else:
            await update.message.reply_text("❌ Faol test topilmadi.")
    
    elif text == "⏩ O'tkazib yuborish":
        if session:
            await skip_question(update, context)
        else:
            await update.message.reply_text("❌ Faol test topilmadi.")
    
    elif text == "🏁 Yakunlash":
        if session:
            await finish_test(update, context)
        else:
            await update.message.reply_text("❌ Faol test topilmadi.", reply_markup=main_menu_keyboard())


async def test_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test reytingi"""
    query = update.callback_query
    await query.answer()

    test_id = int(query.data.split('_')[-1])
    test = await get_test(test_id)
    if not test:
        await query.edit_message_text("❌ Test topilmadi.")
        return

    top_results = await get_test_leaderboard(test)

    text = f"🏆 *{test.title} - Reyting*\n\n"

    medals = ['🥇', '🥈', '🥉']
    for i, result in enumerate(top_results):
        medal = medals[i] if i < 3 else f"{i+1}."
        name = result['user__first_name'] or result['user__username']
        text += f"{medal} {name}: {result['best_score']} ball\n"

    if not top_results:
        text += "Hali natijalar yo'q."

    keyboard = [[InlineKeyboardButton("⬅️ Orqaga", callback_data=f"test_{test_id}")]]

    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


async def back_to_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Testlar ro'yxatiga qaytish"""
    query = update.callback_query
    await query.answer()

    topic_id = context.user_data.get('current_topic_id')
    if topic_id:
        query.data = f"topic_{topic_id}"
        from telegram_bot.handlers.subjects import topic_detail
        await topic_detail(update, context)


def register_handlers(app):
    """Test handlerlarini ro'yxatdan o'tkazish"""
    app.add_handler(CallbackQueryHandler(test_detail, pattern=r"^test_\d+$"))
    app.add_handler(CallbackQueryHandler(start_test, pattern=r"^start_test_\d+$"))
    app.add_handler(CallbackQueryHandler(test_leaderboard, pattern=r"^test_leaderboard_\d+$"))
    app.add_handler(CallbackQueryHandler(back_to_tests, pattern="^back_to_tests$"))
