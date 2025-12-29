"""Test handlerlari - Topic asosida"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from asgiref.sync import sync_to_async
from telegram_bot.keyboards import main_menu_keyboard
from telegram_bot.utils import get_user_or_none
import time


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

    # Test boshlandi xabari
    await query.message.reply_text(
        f"📝 *{test.title}* testi boshlandi!\n\n"
        f"❓ Savollar soni: {len(questions)}\n"
        f"⏱ Vaqt: {test.time_limit} daqiqa\n\n"
        f"Javobni tanlash uchun A, B, C, D tugmalarini bosing.",
        parse_mode='Markdown'
    )

    # Birinchi savolni ko'rsatish
    await show_question(update, context, questions[0], 1, len(questions))


async def show_question(update: Update, context: ContextTypes.DEFAULT_TYPE, question, num: int, total: int):
    """Savolni ko'rsatish - inline tugmalar bilan"""
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

    # Inline tugmalar yaratish - platformadagidek
    keyboard = []
    row = []
    for i, answer in enumerate(answers):
        letter = chr(65 + i)  # A, B, C, D
        row.append(InlineKeyboardButton(letter, callback_data=f"ans_{question.id}_{answer.id}"))
        if len(row) == 2:  # Har qatorda 2 ta tugma
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    # Qo'shimcha tugmalar
    keyboard.append([
        InlineKeyboardButton("⏩ O'tkazib yuborish", callback_data=f"skip_{question.id}"),
        InlineKeyboardButton("🏁 Yakunlash", callback_data="finish_test")
    ])

    # Callback query yoki message ekanligini aniqlash
    if update.callback_query:
        message = update.callback_query.message
    else:
        message = update.message

    await message.reply_text(
        text, 
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def handle_test_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test javobini qabul qilish (A, B, C, D) - matn orqali"""
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


async def handle_inline_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inline tugma orqali javobni qabul qilish - platformadagidek"""
    query = update.callback_query
    await query.answer()
    
    session = context.user_data.get('test_session')
    if not session:
        await query.answer("❌ Faol test topilmadi!", show_alert=True)
        return
    
    data = query.data
    
    # ans_questionId_answerId formatida
    parts = data.split('_')
    if len(parts) != 3:
        return
    
    question_id = int(parts[1])
    answer_id = int(parts[2])
    
    current_question = context.user_data.get('current_question')
    current_answers = context.user_data.get('current_answers', {})
    
    if not current_question or current_question.id != question_id:
        await query.answer("❌ Bu savol endi aktiv emas!", show_alert=True)
        return
    
    try:
        answer = await get_answer(answer_id, current_question)
        correct_answer = await get_correct_answer(current_question)
        
        # Tanlangan javob harfini topish
        selected_letter = None
        for letter, ans_id in current_answers.items():
            if ans_id == answer_id:
                selected_letter = letter
                break
        
        # Javobni saqlash
        session['answers'][str(current_question.id)] = {
            'answer_id': answer_id,
            'is_correct': answer.is_correct
        }
        
        # Natijani ko'rsatish - tugmalarni yangilash
        answers = list(current_question.answers.all())
        
        # Qolgan vaqtni hisoblash
        elapsed = time.time() - session['start_time']
        remaining = max(0, session['time_limit'] - elapsed)
        timer_str = format_timer(int(remaining))
        
        num = session['current_index'] + 1
        total = len(session['questions'])
        
        text = f"⏱ *Vaqt: {timer_str}*\n\n"
        text += f"❓ *Savol {num}/{total}*\n\n"
        text += f"{current_question.text}\n\n"
        
        # Javob variantlarini ko'rsatish - to'g'ri/noto'g'ri belgilash bilan
        for i, ans in enumerate(answers):
            letter = chr(65 + i)
            if ans.is_correct:
                text += f"✅ *{letter})* {ans.text}\n"
            elif ans.id == answer_id and not ans.is_correct:
                text += f"❌ *{letter})* {ans.text}\n"
            else:
                text += f"*{letter})* {ans.text}\n"
        
        text += f"\n💎 Ball: {current_question.points}"
        
        if answer.is_correct:
            session['correct_count'] += 1
            session['earned_points'] += current_question.points
            text += "\n\n✅ *To'g'ri javob!*"
        else:
            correct_letter = None
            for letter, ans_id in current_answers.items():
                if correct_answer and ans_id == correct_answer.id:
                    correct_letter = letter
                    break
            text += f"\n\n❌ *Noto'g'ri!* To'g'ri javob: *{correct_letter}*"
        
        # Keyingi savol tugmasi
        keyboard = [[InlineKeyboardButton("➡️ Keyingi savol", callback_data="next_question")]]
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
    except Exception as e:
        await query.answer(f"❌ Xatolik: {str(e)}", show_alert=True)


async def handle_skip_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inline tugma orqali savolni o'tkazib yuborish"""
    query = update.callback_query
    await query.answer()
    
    session = context.user_data.get('test_session')
    if not session:
        await query.answer("❌ Faol test topilmadi!", show_alert=True)
        return
    
    current_question = context.user_data.get('current_question')
    if current_question:
        # Javobsiz saqlash
        session['answers'][str(current_question.id)] = {
            'answer_id': None,
            'is_correct': False,
            'skipped': True
        }
    
    await query.answer("⏩ Savol o'tkazib yuborildi")
    
    # Keyingi savolga o'tish
    session['current_index'] += 1
    
    if session['current_index'] < len(session['questions']):
        next_question_id = session['questions'][session['current_index']]
        question = await get_question(next_question_id)
        
        # Eski xabarni o'chirish va yangi savol ko'rsatish
        await query.message.delete()
        await show_question_from_callback(query, context, question, session['current_index'] + 1, len(session['questions']))
    else:
        await finish_test_from_callback(query, context)


async def handle_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Keyingi savol tugmasi bosilganda"""
    query = update.callback_query
    await query.answer()
    
    session = context.user_data.get('test_session')
    if not session:
        await query.answer("❌ Faol test topilmadi!", show_alert=True)
        return
    
    session['current_index'] += 1
    
    if session['current_index'] < len(session['questions']):
        next_question_id = session['questions'][session['current_index']]
        question = await get_question(next_question_id)
        
        # Eski xabarni o'chirish va yangi savol ko'rsatish
        await query.message.delete()
        await show_question_from_callback(query, context, question, session['current_index'] + 1, len(session['questions']))
    else:
        await finish_test_from_callback(query, context)


async def show_question_from_callback(query, context: ContextTypes.DEFAULT_TYPE, question, num: int, total: int):
    """Callback query dan savol ko'rsatish"""
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
        letter = chr(65 + i)
        text += f"*{letter})* {answer.text}\n"
    
    text += f"\n💎 Ball: {question.points}"

    # Javob variantlarini saqlash
    context.user_data['current_answers'] = {chr(65 + i): ans.id for i, ans in enumerate(answers)}
    context.user_data['current_question'] = question

    # Inline tugmalar yaratish
    keyboard = []
    row = []
    for i, answer in enumerate(answers):
        letter = chr(65 + i)
        row.append(InlineKeyboardButton(letter, callback_data=f"ans_{question.id}_{answer.id}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([
        InlineKeyboardButton("⏩ O'tkazib yuborish", callback_data=f"skip_{question.id}"),
        InlineKeyboardButton("🏁 Yakunlash", callback_data="finish_test")
    ])

    await query.message.reply_text(
        text, 
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def finish_test_from_callback(query, context: ContextTypes.DEFAULT_TYPE):
    """Callback query dan testni yakunlash"""
    session = context.user_data.get('test_session')
    if not session:
        await query.message.reply_text("❌ Faol test topilmadi.", reply_markup=main_menu_keyboard())
        return

    user = await get_user_or_none(query.from_user.id)
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

    # Eski xabarni o'chirish
    try:
        await query.message.delete()
    except:
        pass

    await query.message.reply_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    # Asosiy menyuni qaytarish
    await query.message.reply_text("Menyu:", reply_markup=main_menu_keyboard())


async def handle_finish_test_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inline tugma orqali testni yakunlash"""
    query = update.callback_query
    await query.answer()
    await finish_test_from_callback(query, context)


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
    
    # Inline tugmalar uchun handlerlar
    app.add_handler(CallbackQueryHandler(handle_inline_answer, pattern=r"^ans_\d+_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_skip_question, pattern=r"^skip_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_next_question, pattern="^next_question$"))
    app.add_handler(CallbackQueryHandler(handle_finish_test_callback, pattern="^finish_test$"))
