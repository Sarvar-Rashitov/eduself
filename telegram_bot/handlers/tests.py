"""Topic test handlerlari - ReplyKeyboard bilan"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from asgiref.sync import sync_to_async
from telegram_bot.keyboards import main_menu_keyboard
from telegram_bot.utils import get_user_or_none
import time


@sync_to_async
def get_topic(topic_id):
    from core.models import Topic
    try:
        return Topic.objects.select_related('subject').get(id=topic_id)
    except Topic.DoesNotExist:
        return None


@sync_to_async
def get_topic_questions(topic):
    return list(topic.questions.all().prefetch_related('answers').order_by('order'))


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
def get_best_result(user, topic):
    from core.models import TopicResult
    return TopicResult.objects.filter(user=user, topic=topic).order_by('-score').first()


@sync_to_async
def get_questions_count(topic):
    return topic.questions.count()


@sync_to_async
def get_max_points(topic):
    from django.db.models import Sum
    return topic.questions.aggregate(total=Sum('points'))['total'] or 0


@sync_to_async
def save_topic_result(user, topic, score, total, correct, passed, time_taken, earned_points, answers):
    from core.models import TopicResult
    TopicResult.objects.create(
        user=user, topic=topic, score=score, total_questions=total,
        correct_answers=correct, passed=passed, time_taken=time_taken,
        earned_points=earned_points, user_answers=answers
    )
    user.total_points += earned_points
    user.save()


@sync_to_async
def get_topic_leaderboard(topic):
    from core.models import TopicResult
    from django.db.models import Max
    return list(TopicResult.objects.filter(topic=topic).values(
        'user__username', 'user__first_name'
    ).annotate(best_score=Max('earned_points')).order_by('-best_score')[:10])


def topic_test_keyboard():
    """Topic test vaqtidagi menyu"""
    keyboard = [
        [KeyboardButton("🅰️"), KeyboardButton("🅱️"), KeyboardButton("🅲"), KeyboardButton("🅳")],
        [KeyboardButton("⏩ O'tkazib yuborish"), KeyboardButton("🏁 Yakunlash")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def format_timer(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"


async def start_topic_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Topic testini boshlash"""
    query = update.callback_query
    await query.answer()

    user = await get_user_or_none(update.effective_user.id)
    if not user:
        await query.answer("❌ Xatolik yuz berdi!", show_alert=True)
        return

    topic_id = int(query.data.split('_')[-1])
    topic = await get_topic(topic_id)
    if not topic:
        await query.edit_message_text("❌ Mavzu topilmadi.")
        return

    questions = await get_topic_questions(topic)
    if not questions:
        await query.answer("❌ Bu mavzuda savollar yo'q!", show_alert=True)
        return

    context.user_data['test_session'] = {
        'topic_id': topic_id,
        'test_type': 'topic',
        'questions': [q.id for q in questions],
        'current_index': 0,
        'answers': {},
        'start_time': time.time(),
        'time_limit': topic.time_limit * 60,
        'correct_count': 0,
        'earned_points': 0
    }

    await query.message.delete()

    await query.message.reply_text(
        f"📝 *{topic.name}* testi boshlandi!\n\n"
        f"❓ Savollar soni: {len(questions)}\n"
        f"⏱ Vaqt: {topic.time_limit} daqiqa\n\n"
        f"Javobni tanlash uchun menyudagi tugmalarni bosing.",
        parse_mode='Markdown',
        reply_markup=topic_test_keyboard()
    )

    await show_topic_question(update, context, questions[0], 1, len(questions))


async def show_topic_question(update: Update, context: ContextTypes.DEFAULT_TYPE, question, num, total):
    """Topic savolini ko'rsatish"""
    session = context.user_data.get('test_session')
    if not session:
        return

    answers = list(question.answers.all())

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

    if update.callback_query:
        message = update.callback_query.message
    else:
        message = update.message

    await message.reply_text(text, parse_mode='Markdown')


async def handle_topic_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Topic javobini qabul qilish (A, B, C, D)"""
    session = context.user_data.get('test_session')
    if not session or session.get('test_type') != 'topic':
        return

    text = update.message.text.strip()
    
    # Emoji harflarni oddiy harflarga o'girish
    answer_map = {'🅰️': 'A', '🅱️': 'B', '🅲': 'C', '🅳': 'D', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'}
    user_answer = answer_map.get(text.upper(), text.upper())

    if user_answer not in ['A', 'B', 'C', 'D']:
        return

    current_answers = context.user_data.get('current_answers', {})
    current_question = context.user_data.get('current_question')

    if not current_answers or not current_question or user_answer not in current_answers:
        await update.message.reply_text("❌ Javob topilmadi.")
        return

    answer_id = current_answers[user_answer]

    try:
        answer = await get_answer(answer_id, current_question)
        correct_answer = await get_correct_answer(current_question)

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
        await next_topic_question(update, context)

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {str(e)}")


async def next_topic_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Keyingi topic savoliga o'tish"""
    session = context.user_data.get('test_session')
    if not session:
        return

    session['current_index'] += 1

    if session['current_index'] < len(session['questions']):
        next_q_id = session['questions'][session['current_index']]
        question = await get_question(next_q_id)
        await show_topic_question(
            update, context, question,
            session['current_index'] + 1,
            len(session['questions'])
        )
    else:
        await finish_topic_test(update, context)


async def skip_topic_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Topic savolini o'tkazib yuborish"""
    session = context.user_data.get('test_session')
    if not session or session.get('test_type') != 'topic':
        return

    current_question = context.user_data.get('current_question')
    if current_question:
        session['answers'][str(current_question.id)] = {
            'answer_id': None,
            'is_correct': False,
            'skipped': True
        }

    await update.message.reply_text("⏩ Savol o'tkazib yuborildi")
    await next_topic_question(update, context)


async def finish_topic_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Topic testni yakunlash"""
    session = context.user_data.get('test_session')
    if not session:
        await update.message.reply_text("❌ Faol test topilmadi.", reply_markup=main_menu_keyboard())
        return

    user = await get_user_or_none(update.effective_user.id)
    topic = await get_topic(session['topic_id'])

    total = len(session['questions'])
    correct = session['correct_count']
    score = int((correct / total) * 100) if total > 0 else 0
    passed = score >= topic.passing_score
    time_taken = int(time.time() - session['start_time'])

    if user:
        await save_topic_result(
            user, topic, score, total, correct, passed,
            time_taken, session['earned_points'], session['answers']
        )

    status = "✅ O'TDINGIZ!" if passed else "❌ O'TMADINGIZ"

    text = f"🏁 *Test yakunlandi!*\n\n"
    text += f"📝 Mavzu: {topic.name}\n"
    text += f"━━━━━━━━━━━━━━━\n"
    text += f"📊 *Natija: {status}*\n\n"
    text += f"✅ To'g'ri: {correct}/{total}\n"
    text += f"📈 Ball: {score}%\n"
    text += f"🏆 Olingan ball: {session['earned_points']}\n"
    text += f"⏱ Vaqt: {time_taken // 60}:{time_taken % 60:02d}\n"

    if passed:
        text += "\n🎉 Tabriklaymiz!"
    else:
        text += f"\n💪 O'tish uchun {topic.passing_score}% kerak."

    context.user_data.pop('test_session', None)
    context.user_data.pop('current_answers', None)
    context.user_data.pop('current_question', None)

    keyboard = [
        [InlineKeyboardButton("🔄 Qayta yechish", callback_data=f"start_topic_test_{topic.id}")],
        [InlineKeyboardButton("🏆 Reyting", callback_data=f"topic_leaderboard_{topic.id}")],
        [InlineKeyboardButton("⬅️ Fanga qaytish", callback_data=f"subject_{topic.subject.id}")]
    ]

    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    await update.message.reply_text("Menyu:", reply_markup=main_menu_keyboard())


async def handle_topic_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Topic test menyu tugmalarini qayta ishlash"""
    text = update.message.text
    session = context.user_data.get('test_session')

    if not session or session.get('test_type') != 'topic':
        return

    if text == "⏩ O'tkazib yuborish":
        await skip_topic_question(update, context)
    elif text == "🏁 Yakunlash":
        await finish_topic_test(update, context)


async def topic_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Topic reytingi"""
    query = update.callback_query
    await query.answer()

    topic_id = int(query.data.split('_')[-1])
    topic = await get_topic(topic_id)
    if not topic:
        await query.edit_message_text("❌ Mavzu topilmadi.")
        return

    top_results = await get_topic_leaderboard(topic)

    text = f"🏆 *{topic.name} - Reyting*\n\n"

    medals = ['🥇', '🥈', '🥉']
    for i, result in enumerate(top_results):
        medal = medals[i] if i < 3 else f"{i+1}."
        name = result['user__first_name'] or result['user__username']
        text += f"{medal} {name}: {result['best_score']} ball\n"

    if not top_results:
        text += "Hali natijalar yo'q."

    keyboard = [[InlineKeyboardButton("⬅️ Orqaga", callback_data=f"topic_{topic_id}")]]

    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


def register_handlers(app):
    """Topic test handlerlarini ro'yxatdan o'tkazish"""
    app.add_handler(CallbackQueryHandler(start_topic_test, pattern=r"^start_topic_test_\d+$"))
    app.add_handler(CallbackQueryHandler(topic_leaderboard, pattern=r"^topic_leaderboard_\d+$"))
    # Matn handler'lari webhook.py da qo'shiladi
