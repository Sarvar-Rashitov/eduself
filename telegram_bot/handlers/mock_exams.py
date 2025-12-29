"""Mock imtihonlar handlerlari"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from asgiref.sync import sync_to_async
from telegram_bot.keyboards import mock_exams_keyboard, main_menu_keyboard
from telegram_bot.utils import get_user_or_none
from telegram_bot.decorators import require_subscription
import time


@sync_to_async
def get_mock_exams(user):
    from core.models import MockExam
    exams = list(MockExam.objects.filter(is_active=True).order_by('order', 'created_at'))
    for exam in exams:
        exam.is_unlocked = exam.is_unlocked_for_user(user) if user else False
    return exams


@sync_to_async
def get_mock_exam(exam_id):
    from core.models import MockExam
    try:
        return MockExam.objects.get(id=exam_id, is_active=True)
    except MockExam.DoesNotExist:
        return None


@sync_to_async
def get_mock_questions(exam):
    return list(exam.mock_questions.all().prefetch_related('mock_answers').order_by('order'))


@sync_to_async
def get_mock_question(question_id):
    from core.models import MockExamQuestion
    return MockExamQuestion.objects.prefetch_related('mock_answers').get(id=question_id)


@sync_to_async
def get_mock_answer(answer_id, question):
    from core.models import MockExamAnswer
    return MockExamAnswer.objects.get(id=answer_id, question=question)


@sync_to_async
def get_mock_correct_answer(question):
    return question.mock_answers.filter(is_correct=True).first()


@sync_to_async
def is_mock_unlocked(exam, user):
    return exam.is_unlocked_for_user(user)


@sync_to_async
def get_mock_best_result(user, exam):
    from core.models import MockExamResult
    return MockExamResult.objects.filter(user=user, exam=exam).order_by('-score').first()


@sync_to_async
def get_mock_questions_count(exam):
    return exam.mock_questions.count()


@sync_to_async
def get_mock_max_points(exam):
    return exam.get_max_points()


@sync_to_async
def save_mock_result(user, exam, score, total, correct, passed, time_taken, earned_points, answers):
    from core.models import MockExamResult
    MockExamResult.objects.create(
        user=user, exam=exam, score=score, total_questions=total,
        correct_answers=correct, passed=passed, time_taken=time_taken,
        earned_points=earned_points, user_answers=answers
    )
    user.total_points += earned_points
    user.save()


@sync_to_async
def get_mock_leaderboard(exam):
    from core.models import MockExamResult
    from django.db.models import Max
    return list(MockExamResult.objects.filter(exam=exam).values(
        'user__username', 'user__first_name'
    ).annotate(best_score=Max('earned_points')).order_by('-best_score')[:10])


def mock_test_keyboard():
    """Mock test vaqtidagi menyu"""
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


@require_subscription("mock")
async def mock_exams_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mock imtihonlar menyusi"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        message = query.message
        edit = True
    else:
        message = update.message
        edit = False

    user = await get_user_or_none(update.effective_user.id)
    exams = await get_mock_exams(user)

    if not exams:
        text = "📝 Hozircha mock imtihonlar mavjud emas."
        if edit:
            await message.edit_text(text)
        else:
            await message.reply_text(text)
        return

    text = "📝 *Mock Imtihonlar*\n\n"
    text += "DTM uslubidagi sinov imtihonlari.\n"
    text += "Imtihonni tanlang:"

    if edit:
        await message.edit_text(text, parse_mode='Markdown', reply_markup=mock_exams_keyboard(exams))
    else:
        await message.reply_text(text, parse_mode='Markdown', reply_markup=mock_exams_keyboard(exams))


async def mock_exam_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mock imtihon tafsilotlari"""
    query = update.callback_query
    await query.answer()

    user = await get_user_or_none(update.effective_user.id)
    exam_id = int(query.data.split('_')[-1])

    exam = await get_mock_exam(exam_id)
    if not exam:
        await query.edit_message_text("❌ Imtihon topilmadi.")
        return

    if user:
        is_unlocked = await is_mock_unlocked(exam, user)
        if not is_unlocked:
            await query.answer("🔒 Bu imtihon hali ochilmagan!", show_alert=True)
            return

    best_result = await get_mock_best_result(user, exam) if user else None
    questions_count = await get_mock_questions_count(exam)
    max_points = await get_mock_max_points(exam)

    text = f"📝 *{exam.title}*\n\n"
    if exam.description:
        text += f"{exam.description}\n\n"
    text += f"❓ Savollar: {questions_count} ta\n"
    text += f"⏱ Vaqt: {exam.time_limit} daqiqa\n"
    text += f"✅ O'tish balli: {exam.passing_score}%\n"
    text += f"🏆 Maksimal ball: {max_points}\n\n"

    if best_result:
        status = "✅ O'tdi" if best_result.passed else "❌ O'tmadi"
        text += f"📊 *Sizning natijangiz:*\n"
        text += f"Ball: {best_result.score}% {status}\n"
        text += f"Olingan ball: {best_result.earned_points}\n"

    context.user_data['current_mock_id'] = exam_id

    keyboard = [
        [InlineKeyboardButton("▶️ Imtihonni boshlash", callback_data=f"start_mock_{exam_id}")],
        [InlineKeyboardButton("🏆 Reyting", callback_data=f"mock_leaderboard_{exam_id}")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="mock_exams")]
    ]

    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


async def start_mock_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mock imtihonni boshlash"""
    query = update.callback_query
    await query.answer()

    user = await get_user_or_none(update.effective_user.id)
    if not user:
        await query.answer("❌ Xatolik yuz berdi!", show_alert=True)
        return

    exam_id = int(query.data.split('_')[-1])
    exam = await get_mock_exam(exam_id)
    if not exam:
        await query.edit_message_text("❌ Imtihon topilmadi.")
        return

    questions = await get_mock_questions(exam)
    if not questions:
        await query.answer("❌ Bu imtihonda savollar yo'q!", show_alert=True)
        return

    context.user_data['test_session'] = {
        'test_id': exam_id,
        'test_type': 'mock',
        'questions': [q.id for q in questions],
        'current_index': 0,
        'answers': {},
        'start_time': time.time(),
        'time_limit': exam.time_limit * 60,
        'correct_count': 0,
        'earned_points': 0
    }

    await query.message.delete()

    await query.message.reply_text(
        f"📝 *{exam.title}* imtihoni boshlandi!\n\n"
        f"❓ Savollar soni: {len(questions)}\n"
        f"⏱ Vaqt: {exam.time_limit} daqiqa\n\n"
        f"Javobni tanlash uchun A, B, C, D tugmalarini bosing.",
        parse_mode='Markdown'
    )

    await show_mock_question(update, context, questions[0], 1, len(questions))


async def show_mock_question(update: Update, context: ContextTypes.DEFAULT_TYPE, question, num, total):
    """Mock savolini ko'rsatish - inline tugmalar bilan"""
    session = context.user_data.get('test_session')
    if not session:
        return

    answers = list(question.mock_answers.all())

    elapsed = time.time() - session['start_time']
    remaining = max(0, session['time_limit'] - elapsed)
    timer_str = format_timer(int(remaining))

    text = f"⏱ *Vaqt: {timer_str}*\n\n"
    text += f"❓ *Savol {num}/{total}*\n\n"
    text += f"{question.text}\n\n"

    for i, answer in enumerate(answers):
        letter = chr(65 + i)
        text += f"*{letter})* {answer.text}\n"

    text += f"\n💎 Ball: {question.points}"

    context.user_data['current_answers'] = {chr(65 + i): ans.id for i, ans in enumerate(answers)}
    context.user_data['current_question'] = question

    # Inline tugmalar yaratish - platformadagidek
    keyboard = []
    row = []
    for i, answer in enumerate(answers):
        letter = chr(65 + i)
        row.append(InlineKeyboardButton(letter, callback_data=f"mock_ans_{question.id}_{answer.id}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([
        InlineKeyboardButton("⏩ O'tkazib yuborish", callback_data=f"mock_skip_{question.id}"),
        InlineKeyboardButton("🏁 Yakunlash", callback_data="mock_finish")
    ])

    if update.callback_query:
        message = update.callback_query.message
    else:
        message = update.message

    await message.reply_text(
        text, 
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def handle_mock_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mock javobini qabul qilish - matn orqali (eski usul)"""
    session = context.user_data.get('test_session')
    if not session or session.get('test_type') != 'mock':
        return

    user_answer = update.message.text.upper().strip()

    if user_answer not in ['A', 'B', 'C', 'D']:
        return

    current_answers = context.user_data.get('current_answers', {})
    current_question = context.user_data.get('current_question')

    if not current_answers or not current_question or user_answer not in current_answers:
        await update.message.reply_text("❌ Javob topilmadi.")
        return

    answer_id = current_answers[user_answer]

    try:
        answer = await get_mock_answer(answer_id, current_question)
        correct_answer = await get_mock_correct_answer(current_question)

        session['answers'][str(current_question.id)] = {
            'answer_id': answer_id,
            'is_correct': answer.is_correct
        }

        if answer.is_correct:
            session['correct_count'] += 1
            session['earned_points'] += int(current_question.points)
            result_text = "✅ To'g'ri!"
        else:
            correct_letter = None
            for letter, ans_id in current_answers.items():
                if correct_answer and ans_id == correct_answer.id:
                    correct_letter = letter
                    break
            result_text = f"❌ Noto'g'ri! To'g'ri javob: {correct_letter}"

        await update.message.reply_text(result_text)
        await next_mock_question(update, context)

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {str(e)}")


async def handle_mock_inline_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inline tugma orqali mock javobni qabul qilish"""
    query = update.callback_query
    await query.answer()
    
    session = context.user_data.get('test_session')
    if not session or session.get('test_type') != 'mock':
        await query.answer("❌ Faol imtihon topilmadi!", show_alert=True)
        return
    
    data = query.data
    parts = data.split('_')
    if len(parts) != 4:  # mock_ans_questionId_answerId
        return
    
    question_id = int(parts[2])
    answer_id = int(parts[3])
    
    current_question = context.user_data.get('current_question')
    current_answers = context.user_data.get('current_answers', {})
    
    if not current_question or current_question.id != question_id:
        await query.answer("❌ Bu savol endi aktiv emas!", show_alert=True)
        return
    
    try:
        answer = await get_mock_answer(answer_id, current_question)
        correct_answer = await get_mock_correct_answer(current_question)
        
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
        
        # Natijani ko'rsatish
        answers = list(current_question.mock_answers.all())
        
        elapsed = time.time() - session['start_time']
        remaining = max(0, session['time_limit'] - elapsed)
        timer_str = format_timer(int(remaining))
        
        num = session['current_index'] + 1
        total = len(session['questions'])
        
        text = f"⏱ *Vaqt: {timer_str}*\n\n"
        text += f"❓ *Savol {num}/{total}*\n\n"
        text += f"{current_question.text}\n\n"
        
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
            session['earned_points'] += int(current_question.points)
            text += "\n\n✅ *To'g'ri javob!*"
        else:
            correct_letter = None
            for letter, ans_id in current_answers.items():
                if correct_answer and ans_id == correct_answer.id:
                    correct_letter = letter
                    break
            text += f"\n\n❌ *Noto'g'ri!* To'g'ri javob: *{correct_letter}*"
        
        keyboard = [[InlineKeyboardButton("➡️ Keyingi savol", callback_data="mock_next")]]
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
    except Exception as e:
        await query.answer(f"❌ Xatolik: {str(e)}", show_alert=True)


async def handle_mock_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inline tugma orqali mock savolni o'tkazib yuborish"""
    query = update.callback_query
    await query.answer()
    
    session = context.user_data.get('test_session')
    if not session or session.get('test_type') != 'mock':
        await query.answer("❌ Faol imtihon topilmadi!", show_alert=True)
        return
    
    current_question = context.user_data.get('current_question')
    if current_question:
        session['answers'][str(current_question.id)] = {
            'answer_id': None,
            'is_correct': False,
            'skipped': True
        }
    
    await query.answer("⏩ Savol o'tkazib yuborildi")
    
    session['current_index'] += 1
    
    if session['current_index'] < len(session['questions']):
        next_q_id = session['questions'][session['current_index']]
        question = await get_mock_question(next_q_id)
        
        await query.message.delete()
        await show_mock_question_from_callback(query, context, question, session['current_index'] + 1, len(session['questions']))
    else:
        await finish_mock_from_callback(query, context)


async def handle_mock_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Keyingi mock savol tugmasi"""
    query = update.callback_query
    await query.answer()
    
    session = context.user_data.get('test_session')
    if not session or session.get('test_type') != 'mock':
        await query.answer("❌ Faol imtihon topilmadi!", show_alert=True)
        return
    
    session['current_index'] += 1
    
    if session['current_index'] < len(session['questions']):
        next_q_id = session['questions'][session['current_index']]
        question = await get_mock_question(next_q_id)
        
        await query.message.delete()
        await show_mock_question_from_callback(query, context, question, session['current_index'] + 1, len(session['questions']))
    else:
        await finish_mock_from_callback(query, context)


async def show_mock_question_from_callback(query, context: ContextTypes.DEFAULT_TYPE, question, num, total):
    """Callback dan mock savol ko'rsatish"""
    session = context.user_data.get('test_session')
    if not session:
        return

    answers = list(question.mock_answers.all())

    elapsed = time.time() - session['start_time']
    remaining = max(0, session['time_limit'] - elapsed)
    timer_str = format_timer(int(remaining))

    text = f"⏱ *Vaqt: {timer_str}*\n\n"
    text += f"❓ *Savol {num}/{total}*\n\n"
    text += f"{question.text}\n\n"

    for i, answer in enumerate(answers):
        letter = chr(65 + i)
        text += f"*{letter})* {answer.text}\n"

    text += f"\n💎 Ball: {question.points}"

    context.user_data['current_answers'] = {chr(65 + i): ans.id for i, ans in enumerate(answers)}
    context.user_data['current_question'] = question

    keyboard = []
    row = []
    for i, answer in enumerate(answers):
        letter = chr(65 + i)
        row.append(InlineKeyboardButton(letter, callback_data=f"mock_ans_{question.id}_{answer.id}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([
        InlineKeyboardButton("⏩ O'tkazib yuborish", callback_data=f"mock_skip_{question.id}"),
        InlineKeyboardButton("🏁 Yakunlash", callback_data="mock_finish")
    ])

    await query.message.reply_text(
        text, 
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def finish_mock_from_callback(query, context: ContextTypes.DEFAULT_TYPE):
    """Callback dan mock imtihonni yakunlash"""
    session = context.user_data.get('test_session')
    if not session:
        await query.message.reply_text("❌ Faol imtihon topilmadi.", reply_markup=main_menu_keyboard())
        return

    user = await get_user_or_none(query.from_user.id)
    exam = await get_mock_exam(session['test_id'])

    total = len(session['questions'])
    correct = session['correct_count']
    score = int((correct / total) * 100) if total > 0 else 0
    passed = score >= exam.passing_score
    time_taken = int(time.time() - session['start_time'])

    if user:
        await save_mock_result(
            user, exam, score, total, correct, passed,
            time_taken, session['earned_points'], session['answers']
        )

    status = "✅ O'TDINGIZ!" if passed else "❌ O'TMADINGIZ"

    text = f"🏁 *Mock imtihon yakunlandi!*\n\n"
    text += f"📝 {exam.title}\n"
    text += f"━━━━━━━━━━━━━━━\n"
    text += f"📊 *Natija: {status}*\n\n"
    text += f"✅ To'g'ri: {correct}/{total}\n"
    text += f"📈 Ball: {score}%\n"
    text += f"🏆 Olingan ball: {session['earned_points']}\n"
    text += f"⏱ Vaqt: {time_taken // 60}:{time_taken % 60:02d}\n"

    if passed:
        text += "\n🎉 Ajoyib natija! Keyingi imtihon ochildi!"
    else:
        text += f"\n💪 O'tish uchun {exam.passing_score}% kerak."

    context.user_data.pop('test_session', None)
    context.user_data.pop('current_answers', None)
    context.user_data.pop('current_question', None)

    keyboard = [
        [InlineKeyboardButton("🔄 Qayta yechish", callback_data=f"start_mock_{exam.id}")],
        [InlineKeyboardButton("🏆 Reyting", callback_data=f"mock_leaderboard_{exam.id}")],
        [InlineKeyboardButton("⬅️ Imtihonlarga qaytish", callback_data="mock_exams")]
    ]

    try:
        await query.message.delete()
    except:
        pass

    await query.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    await query.message.reply_text("Menyu:", reply_markup=main_menu_keyboard())


async def handle_mock_finish_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inline tugma orqali mock imtihonni yakunlash"""
    query = update.callback_query
    await query.answer()
    await finish_mock_from_callback(query, context)


async def next_mock_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Keyingi mock savoliga o'tish"""
    session = context.user_data.get('test_session')
    if not session:
        return

    session['current_index'] += 1

    if session['current_index'] < len(session['questions']):
        next_q_id = session['questions'][session['current_index']]
        question = await get_mock_question(next_q_id)
        await show_mock_question(
            update, context, question,
            session['current_index'] + 1,
            len(session['questions'])
        )
    else:
        await finish_mock_exam(update, context)


async def skip_mock_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mock savolini o'tkazib yuborish"""
    session = context.user_data.get('test_session')
    if not session:
        return

    current_question = context.user_data.get('current_question')
    if current_question:
        session['answers'][str(current_question.id)] = {
            'answer_id': None,
            'is_correct': False,
            'skipped': True
        }

    await update.message.reply_text("⏩ Savol o'tkazib yuborildi")
    await next_mock_question(update, context)


async def finish_mock_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mock imtihonni yakunlash"""
    session = context.user_data.get('test_session')
    if not session:
        await update.message.reply_text("❌ Faol imtihon topilmadi.", reply_markup=main_menu_keyboard())
        return

    user = await get_user_or_none(update.effective_user.id)
    exam = await get_mock_exam(session['test_id'])

    total = len(session['questions'])
    correct = session['correct_count']
    score = int((correct / total) * 100) if total > 0 else 0
    passed = score >= exam.passing_score
    time_taken = int(time.time() - session['start_time'])

    if user:
        await save_mock_result(
            user, exam, score, total, correct, passed,
            time_taken, session['earned_points'], session['answers']
        )

    status = "✅ O'TDINGIZ!" if passed else "❌ O'TMADINGIZ"

    text = f"🏁 *Mock imtihon yakunlandi!*\n\n"
    text += f"📝 {exam.title}\n"
    text += f"━━━━━━━━━━━━━━━\n"
    text += f"📊 *Natija: {status}*\n\n"
    text += f"✅ To'g'ri: {correct}/{total}\n"
    text += f"📈 Ball: {score}%\n"
    text += f"🏆 Olingan ball: {session['earned_points']}\n"
    text += f"⏱ Vaqt: {time_taken // 60}:{time_taken % 60:02d}\n"

    if passed:
        text += "\n🎉 Ajoyib natija! Keyingi imtihon ochildi!"
    else:
        text += f"\n💪 O'tish uchun {exam.passing_score}% kerak."

    context.user_data.pop('test_session', None)
    context.user_data.pop('current_answers', None)
    context.user_data.pop('current_question', None)

    keyboard = [
        [InlineKeyboardButton("🔄 Qayta yechish", callback_data=f"start_mock_{exam.id}")],
        [InlineKeyboardButton("🏆 Reyting", callback_data=f"mock_leaderboard_{exam.id}")],
        [InlineKeyboardButton("⬅️ Imtihonlarga qaytish", callback_data="mock_exams")]
    ]

    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    await update.message.reply_text("Menyu:", reply_markup=main_menu_keyboard())


async def handle_mock_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mock test menyu tugmalarini qayta ishlash"""
    text = update.message.text
    session = context.user_data.get('test_session')

    if not session or session.get('test_type') != 'mock':
        return

    if text == "⏭ Keyingisi":
        await next_mock_question(update, context)
    elif text == "⏩ O'tkazib yuborish":
        await skip_mock_question(update, context)
    elif text == "🏁 Yakunlash":
        await finish_mock_exam(update, context)


async def mock_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mock imtihon reytingi"""
    query = update.callback_query
    await query.answer()

    exam_id = int(query.data.split('_')[-1])
    exam = await get_mock_exam(exam_id)
    if not exam:
        await query.edit_message_text("❌ Imtihon topilmadi.")
        return

    top_results = await get_mock_leaderboard(exam)

    text = f"🏆 *{exam.title} - Reyting*\n\n"

    medals = ['🥇', '🥈', '🥉']
    for i, result in enumerate(top_results):
        medal = medals[i] if i < 3 else f"{i+1}."
        name = result['user__first_name'] or result['user__username']
        text += f"{medal} {name}: {result['best_score']} ball\n"

    if not top_results:
        text += "Hali natijalar yo'q."

    keyboard = [[InlineKeyboardButton("⬅️ Orqaga", callback_data=f"mock_{exam_id}")]]

    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_mock_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mock imtihonlar tugmasi"""
    if update.message.text == "📝 Mock Imtihonlar":
        await mock_exams_menu(update, context)


def register_handlers(app):
    """Mock exam handlerlarini ro'yxatdan o'tkazish"""
    app.add_handler(CallbackQueryHandler(mock_exams_menu, pattern="^mock_exams$"))
    app.add_handler(CallbackQueryHandler(mock_exam_detail, pattern=r"^mock_\d+$"))
    app.add_handler(CallbackQueryHandler(start_mock_exam, pattern=r"^start_mock_\d+$"))
    app.add_handler(CallbackQueryHandler(mock_leaderboard, pattern=r"^mock_leaderboard_\d+$"))
    app.add_handler(MessageHandler(filters.Regex("^📝 Mock Imtihonlar$"), handle_mock_text))
    
    # Inline tugmalar uchun handlerlar
    app.add_handler(CallbackQueryHandler(handle_mock_inline_answer, pattern=r"^mock_ans_\d+_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_mock_skip, pattern=r"^mock_skip_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_mock_next, pattern="^mock_next$"))
    app.add_handler(CallbackQueryHandler(handle_mock_finish_callback, pattern="^mock_finish$"))
