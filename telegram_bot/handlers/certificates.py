"""Sertifikatlar handlerlari"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from asgiref.sync import sync_to_async
from telegram_bot.keyboards import certificates_keyboard, main_menu_keyboard
from telegram_bot.utils import get_user_or_none
from telegram_bot.decorators import require_subscription
import time


@sync_to_async
def get_certificates():
    from core.models import Certificate
    return list(Certificate.objects.filter(is_active=True).order_by('order', 'name'))


@sync_to_async
def get_certificate(cert_id):
    from core.models import Certificate
    try:
        return Certificate.objects.get(id=cert_id, is_active=True)
    except Certificate.DoesNotExist:
        return None


@sync_to_async
def get_cert_topics(cert):
    return list(cert.cert_topics.filter(is_active=True).order_by('order', 'name'))


@sync_to_async
def get_cert_topic(topic_id):
    from core.models import CertificateTopic
    try:
        return CertificateTopic.objects.select_related('certificate').get(id=topic_id, is_active=True)
    except CertificateTopic.DoesNotExist:
        return None


@sync_to_async
def get_cert_tests(topic, user):
    tests = list(topic.cert_tests.filter(is_active=True).order_by('order', 'created_at'))
    for test in tests:
        test.is_unlocked = test.is_unlocked_for_user(user) if user else False
    return tests


@sync_to_async
def get_cert_test(test_id):
    from core.models import CertificateTest
    try:
        return CertificateTest.objects.select_related('topic__certificate').get(id=test_id, is_active=True)
    except CertificateTest.DoesNotExist:
        return None


@sync_to_async
def get_cert_questions(test):
    return list(test.cert_questions.all().prefetch_related('cert_answers').order_by('order'))


@sync_to_async
def get_cert_question(question_id):
    from core.models import CertificateQuestion
    return CertificateQuestion.objects.prefetch_related('cert_answers').get(id=question_id)


@sync_to_async
def get_cert_answer(answer_id, question):
    from core.models import CertificateAnswer
    return CertificateAnswer.objects.get(id=answer_id, question=question)


@sync_to_async
def get_cert_correct_answer(question):
    return question.cert_answers.filter(is_correct=True).first()


@sync_to_async
def is_cert_test_unlocked(test, user):
    return test.is_unlocked_for_user(user)


@sync_to_async
def get_cert_best_result(user, test):
    from core.models import CertificateResult
    return CertificateResult.objects.filter(user=user, test=test).order_by('-score').first()


@sync_to_async
def get_cert_questions_count(test):
    return test.cert_questions.count()


@sync_to_async
def save_cert_result(user, test, score, total, correct, passed, time_taken, earned_points, answers):
    from core.models import CertificateResult
    CertificateResult.objects.create(
        user=user, test=test, score=score, total_questions=total,
        correct_answers=correct, passed=passed, time_taken=time_taken,
        earned_points=earned_points, user_answers=answers
    )
    user.total_points += earned_points
    user.save()


def cert_test_keyboard():
    """Sertifikat test vaqtidagi menyu"""
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


@require_subscription("certificates")
async def certificates_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sertifikatlar menyusi"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        message = query.message
        edit = True
    else:
        message = update.message
        edit = False

    certificates = await get_certificates()

    if not certificates:
        text = "🏆 Hozircha sertifikatlar mavjud emas."
        if edit:
            await message.edit_text(text)
        else:
            await message.reply_text(text)
        return

    text = "🏆 *Sertifikatlar*\n\nSertifikat dasturini tanlang:"

    if edit:
        await message.edit_text(text, parse_mode='Markdown', reply_markup=certificates_keyboard(certificates))
    else:
        await message.reply_text(text, parse_mode='Markdown', reply_markup=certificates_keyboard(certificates))


async def certificate_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sertifikat tafsilotlari"""
    query = update.callback_query
    await query.answer()

    cert_id = int(query.data.split('_')[-1])
    cert = await get_certificate(cert_id)

    if not cert:
        await query.edit_message_text("❌ Sertifikat topilmadi.")
        return

    topics = await get_cert_topics(cert)

    text = f"🏆 *{cert.name}*\n\n"
    if cert.description:
        text += f"{cert.description}\n\n"
    text += f"📚 Fanlar soni: {len(topics)}\n\nFanni tanlang:"

    keyboard = []
    for topic in topics:
        keyboard.append([InlineKeyboardButton(f"📖 {topic.name}", callback_data=f"cert_topic_{topic.id}")])
    keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="certificates")])

    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


async def cert_topic_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sertifikat fani tafsilotlari"""
    query = update.callback_query
    await query.answer()

    user = await get_user_or_none(update.effective_user.id)
    topic_id = int(query.data.split('_')[-1])

    topic = await get_cert_topic(topic_id)
    if not topic:
        await query.edit_message_text("❌ Fan topilmadi.")
        return

    tests = await get_cert_tests(topic, user)

    text = f"📖 *{topic.name}*\n\n"
    text += f"🏆 Sertifikat: {topic.certificate.name}\n"
    text += f"📝 Testlar soni: {len(tests)}\n\nTestni tanlang:"

    context.user_data['current_cert_topic_id'] = topic_id

    keyboard = []
    for test in tests:
        status = "🔓" if test.is_unlocked else "🔒"
        keyboard.append([InlineKeyboardButton(f"{status} {test.title}", callback_data=f"cert_test_{test.id}")])
    keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data=f"certificate_{topic.certificate.id}")])

    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


async def cert_test_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sertifikat test tafsilotlari"""
    query = update.callback_query
    await query.answer()

    user = await get_user_or_none(update.effective_user.id)
    test_id = int(query.data.split('_')[-1])

    test = await get_cert_test(test_id)
    if not test:
        await query.edit_message_text("❌ Test topilmadi.")
        return

    if user:
        is_unlocked = await is_cert_test_unlocked(test, user)
        if not is_unlocked:
            await query.answer("🔒 Bu test hali ochilmagan!", show_alert=True)
            return

    best_result = await get_cert_best_result(user, test) if user else None
    questions_count = await get_cert_questions_count(test)

    text = f"📝 *{test.title}*\n\n"
    text += f"🏆 Sertifikat: {test.topic.certificate.name}\n"
    text += f"📖 Fan: {test.topic.name}\n"
    text += f"❓ Savollar: {questions_count} ta\n"
    text += f"⏱ Vaqt: {test.time_limit} daqiqa\n"
    text += f"✅ O'tish balli: {test.passing_score}%\n\n"

    if best_result:
        status = "✅ O'tdi" if best_result.passed else "❌ O'tmadi"
        text += f"📊 *Sizning natijangiz:*\nBall: {best_result.score}% {status}\n"

    context.user_data['current_cert_test_id'] = test_id

    keyboard = [
        [InlineKeyboardButton("▶️ Testni boshlash", callback_data=f"start_cert_test_{test_id}")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data=f"cert_topic_{test.topic.id}")]
    ]

    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


async def start_cert_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sertifikat testini boshlash"""
    query = update.callback_query
    await query.answer()

    user = await get_user_or_none(update.effective_user.id)
    if not user:
        await query.answer("❌ Xatolik yuz berdi!", show_alert=True)
        return

    test_id = int(query.data.split('_')[-1])
    test = await get_cert_test(test_id)
    if not test:
        await query.edit_message_text("❌ Test topilmadi.")
        return

    questions = await get_cert_questions(test)
    if not questions:
        await query.answer("❌ Bu testda savollar yo'q!", show_alert=True)
        return

    context.user_data['test_session'] = {
        'test_id': test_id,
        'test_type': 'certificate',
        'questions': [q.id for q in questions],
        'current_index': 0,
        'answers': {},
        'start_time': time.time(),
        'time_limit': test.time_limit * 60,
        'correct_count': 0,
        'earned_points': 0
    }

    await query.message.delete()

    await query.message.reply_text(
        "🏆 Sertifikat testi boshlandi!\n\nJavobni tanlash uchun A, B, C, D harflarini yuboring.",
        reply_markup=cert_test_keyboard()
    )

    await show_cert_question(update, context, questions[0], 1, len(questions))


async def show_cert_question(update: Update, context: ContextTypes.DEFAULT_TYPE, question, num, total):
    """Sertifikat savolini ko'rsatish"""
    session = context.user_data.get('test_session')
    if not session:
        return

    answers = list(question.cert_answers.all())

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


async def handle_cert_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sertifikat javobini qabul qilish"""
    session = context.user_data.get('test_session')
    if not session or session.get('test_type') != 'certificate':
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
        answer = await get_cert_answer(answer_id, current_question)
        correct_answer = await get_cert_correct_answer(current_question)

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
        await next_cert_question(update, context)

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {str(e)}")


async def next_cert_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Keyingi sertifikat savoliga o'tish"""
    session = context.user_data.get('test_session')
    if not session:
        return

    session['current_index'] += 1

    if session['current_index'] < len(session['questions']):
        next_q_id = session['questions'][session['current_index']]
        question = await get_cert_question(next_q_id)
        await show_cert_question(
            update, context, question,
            session['current_index'] + 1,
            len(session['questions'])
        )
    else:
        await finish_cert_test(update, context)


async def skip_cert_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sertifikat savolini o'tkazib yuborish"""
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
    await next_cert_question(update, context)


async def finish_cert_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sertifikat testini yakunlash"""
    session = context.user_data.get('test_session')
    if not session:
        await update.message.reply_text("❌ Faol test topilmadi.", reply_markup=main_menu_keyboard())
        return

    user = await get_user_or_none(update.effective_user.id)
    test = await get_cert_test(session['test_id'])

    total = len(session['questions'])
    correct = session['correct_count']
    score = int((correct / total) * 100) if total > 0 else 0
    passed = score >= test.passing_score
    time_taken = int(time.time() - session['start_time'])

    if user:
        await save_cert_result(user, test, score, total, correct, passed, time_taken, session['earned_points'], session['answers'])

    status = "✅ O'TDINGIZ!" if passed else "❌ O'TMADINGIZ"

    text = f"🏁 *Sertifikat testi yakunlandi!*\n\n"
    text += f"🏆 {test.topic.certificate.name}\n📝 {test.title}\n"
    text += f"━━━━━━━━━━━━━━━\n"
    text += f"📊 *Natija: {status}*\n\n"
    text += f"✅ To'g'ri: {correct}/{total}\n📈 Ball: {score}%\n"
    text += f"🏆 Olingan ball: {session['earned_points']}\n⏱ Vaqt: {time_taken // 60}:{time_taken % 60:02d}\n"

    context.user_data.pop('test_session', None)
    context.user_data.pop('current_answers', None)
    context.user_data.pop('current_question', None)

    keyboard = [
        [InlineKeyboardButton("🔄 Qayta yechish", callback_data=f"start_cert_test_{test.id}")],
        [InlineKeyboardButton("⬅️ Fanga qaytish", callback_data=f"cert_topic_{test.topic.id}")]
    ]

    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    await update.message.reply_text("Menyu:", reply_markup=main_menu_keyboard())


async def handle_cert_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sertifikat test menyu tugmalarini qayta ishlash"""
    text = update.message.text
    session = context.user_data.get('test_session')

    if not session or session.get('test_type') != 'certificate':
        return

    if text == "⏭ Keyingisi":
        await next_cert_question(update, context)
    elif text == "⏩ O'tkazib yuborish":
        await skip_cert_question(update, context)
    elif text == "🏁 Yakunlash":
        await finish_cert_test(update, context)


async def handle_certificates_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sertifikatlar tugmasi"""
    if update.message.text == "🏆 Sertifikatlar":
        await certificates_menu(update, context)


def register_handlers(app):
    """Sertifikat handlerlarini ro'yxatdan o'tkazish"""
    app.add_handler(CallbackQueryHandler(certificates_menu, pattern="^certificates$"))
    app.add_handler(CallbackQueryHandler(certificate_detail, pattern=r"^certificate_\d+$"))
    app.add_handler(CallbackQueryHandler(cert_topic_detail, pattern=r"^cert_topic_\d+$"))
    app.add_handler(CallbackQueryHandler(cert_test_detail, pattern=r"^cert_test_\d+$"))
    app.add_handler(CallbackQueryHandler(start_cert_test, pattern=r"^start_cert_test_\d+$"))
    app.add_handler(MessageHandler(filters.Regex("^🏆 Sertifikatlar$"), handle_certificates_text))
