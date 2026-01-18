"""Sertifikatlar handlerlari - Mock uslubida"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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
def get_cert_max_points(test):
    from django.db.models import Sum
    return test.cert_questions.aggregate(total=Sum('points'))['total'] or 0


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


@sync_to_async
def get_cert_leaderboard(test):
    from core.models import CertificateResult
    from django.db.models import Max
    return list(CertificateResult.objects.filter(test=test).values(
        'user__username', 'user__first_name'
    ).annotate(best_score=Max('earned_points')).order_by('-best_score')[:10])


def format_timer(seconds):
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
    max_points = await get_cert_max_points(test)

    text = f"📝 *{test.title}*\n\n"
    text += f"🏆 Sertifikat: {test.topic.certificate.name}\n"
    text += f"📖 Fan: {test.topic.name}\n"
    text += f"❓ Savollar: {questions_count} ta\n"
    text += f"⏱ Vaqt: {test.time_limit} daqiqa\n"
    text += f"✅ O'tish balli: {test.passing_score}%\n"
    text += f"🏆 Maksimal ball: {max_points}\n\n"

    if best_result:
        status = "✅ O'tdi" if best_result.passed else "❌ O'tmadi"
        text += f"📊 *Sizning natijangiz:*\nBall: {best_result.score}% {status}\n"

    context.user_data['current_cert_test_id'] = test_id

    keyboard = [
        [InlineKeyboardButton("▶️ Testni boshlash", callback_data=f"start_cert_test_{test_id}")],
        [InlineKeyboardButton("🏆 Reyting", callback_data=f"cert_leaderboard_{test_id}")],
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
        f"🏆 *{test.title}* testi boshlandi!\n\n"
        f"❓ Savollar soni: {len(questions)}\n"
        f"⏱ Vaqt: {test.time_limit} daqiqa\n\n"
        f"Javobni tanlash uchun tugmalarni bosing.",
        parse_mode='Markdown'
    )

    await show_cert_question(query, context, questions[0], 1, len(questions))


async def show_cert_question(query, context: ContextTypes.DEFAULT_TYPE, question, num, total):
    """Sertifikat savolini ko'rsatish - inline tugmalar bilan"""
    session = context.user_data.get('test_session')
    if not session:
        return

    answers = list(question.cert_answers.all())

    elapsed = time.time() - session['start_time']
    remaining = max(0, session['time_limit'] - elapsed)
    timer_str = format_timer(int(remaining))

    # Oldingi xabarlarni o'chirish
    previous_messages = context.user_data.get('question_messages', [])
    for msg_id in previous_messages:
        try:
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=msg_id)
        except:
            pass
    context.user_data['question_messages'] = []

    # Uzun matn mavjud bo'lsa, avval uni yuborish
    if question.long_text and question.long_text.strip():
        long_text_message = f"📖 *Matn o'qing:*\n\n{question.long_text}\n\n"
        long_text_message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        msg = await query.message.reply_text(
            long_text_message,
            parse_mode='Markdown'
        )
        context.user_data['question_messages'].append(msg.message_id)

    # Rasm mavjud bo'lsa, uni yuborish
    if question.image:
        try:
            msg = await query.message.reply_photo(
                photo=question.image.url,
                caption=f"📷 Savol {num}/{total} uchun rasm"
            )
            context.user_data['question_messages'].append(msg.message_id)
        except Exception as e:
            print(f"Rasm yuborishda xatolik: {e}")

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
        row.append(InlineKeyboardButton(letter, callback_data=f"cert_ans_{question.id}_{answer.id}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([
        InlineKeyboardButton("⏩ O'tkazib yuborish", callback_data=f"cert_skip_{question.id}"),
        InlineKeyboardButton("🏁 Yakunlash", callback_data="cert_finish")
    ])

    msg = await query.message.reply_text(
        text, 
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    context.user_data['question_messages'].append(msg.message_id)


async def handle_cert_inline_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inline tugma orqali cert javobni qabul qilish"""
    query = update.callback_query
    await query.answer()
    
    session = context.user_data.get('test_session')
    if not session or session.get('test_type') != 'certificate':
        await query.answer("❌ Faol test topilmadi!", show_alert=True)
        return
    
    parts = query.data.split('_')
    if len(parts) != 4:
        return
    
    question_id = int(parts[2])
    answer_id = int(parts[3])
    
    current_question = context.user_data.get('current_question')
    current_answers = context.user_data.get('current_answers', {})
    
    if not current_question or current_question.id != question_id:
        await query.answer("❌ Bu savol endi aktiv emas!", show_alert=True)
        return
    
    try:
        answer = await get_cert_answer(answer_id, current_question)
        correct_answer = await get_cert_correct_answer(current_question)
        
        session['answers'][str(current_question.id)] = {
            'answer_id': answer_id,
            'is_correct': answer.is_correct
        }
        
        answers = list(current_question.cert_answers.all())
        
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
            session['earned_points'] += current_question.points
            text += "\n\n✅ *To'g'ri javob!*"
        else:
            correct_letter = None
            for letter, ans_id in current_answers.items():
                if correct_answer and ans_id == correct_answer.id:
                    correct_letter = letter
                    break
            text += f"\n\n❌ *Noto'g'ri!* To'g'ri javob: *{correct_letter}*"
        
        keyboard = [[InlineKeyboardButton("➡️ Keyingi savol", callback_data="cert_next")]]
        
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
        
    except Exception as e:
        await query.answer(f"❌ Xatolik: {str(e)}", show_alert=True)


async def handle_cert_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inline tugma orqali cert savolni o'tkazib yuborish"""
    query = update.callback_query
    await query.answer()
    
    session = context.user_data.get('test_session')
    if not session or session.get('test_type') != 'certificate':
        await query.answer("❌ Faol test topilmadi!", show_alert=True)
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
        question = await get_cert_question(next_q_id)
        
        # Hozirgi savolni o'chirish
        try:
            await query.message.delete()
        except:
            pass
        
        await show_cert_question(query, context, question, session['current_index'] + 1, len(session['questions']))
    else:
        await finish_cert_from_callback(query, context)


async def handle_cert_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Keyingi cert savol tugmasi"""
    query = update.callback_query
    await query.answer()
    
    session = context.user_data.get('test_session')
    if not session or session.get('test_type') != 'certificate':
        await query.answer("❌ Faol test topilmadi!", show_alert=True)
        return
    
    session['current_index'] += 1
    
    if session['current_index'] < len(session['questions']):
        next_q_id = session['questions'][session['current_index']]
        question = await get_cert_question(next_q_id)
        
        # Hozirgi savolni o'chirish
        try:
            await query.message.delete()
        except:
            pass
        
        await show_cert_question(query, context, question, session['current_index'] + 1, len(session['questions']))
    else:
        await finish_cert_from_callback(query, context)


async def finish_cert_from_callback(query, context: ContextTypes.DEFAULT_TYPE):
    """Callback dan cert testni yakunlash"""
    session = context.user_data.get('test_session')
    if not session:
        await query.message.reply_text("❌ Faol test topilmadi.", reply_markup=main_menu_keyboard())
        return

    user = await get_user_or_none(query.from_user.id)
    test = await get_cert_test(session['test_id'])

    total = len(session['questions'])
    correct = session['correct_count']
    score = int((correct / total) * 100) if total > 0 else 0
    passed = score >= test.passing_score
    time_taken = int(time.time() - session['start_time'])

    if user:
        await save_cert_result(
            user, test, score, total, correct, passed,
            time_taken, session['earned_points'], session['answers']
        )

    status = "✅ O'TDINGIZ!" if passed else "❌ O'TMADINGIZ"

    text = f"🏁 *Sertifikat testi yakunlandi!*\n\n"
    text += f"🏆 {test.topic.certificate.name}\n"
    text += f"📝 {test.title}\n"
    text += f"━━━━━━━━━━━━━━━\n"
    text += f"📊 *Natija: {status}*\n\n"
    text += f"✅ To'g'ri: {correct}/{total}\n"
    text += f"📈 Ball: {score}%\n"
    text += f"🏆 Olingan ball: {session['earned_points']}\n"
    text += f"⏱ Vaqt: {time_taken // 60}:{time_taken % 60:02d}\n"

    if passed:
        text += "\n🎉 Ajoyib! Keyingi test ochildi!"
    else:
        text += f"\n💪 O'tish uchun {test.passing_score}% kerak."

    # Barcha test xabarlarini o'chirish
    previous_messages = context.user_data.get('question_messages', [])
    for msg_id in previous_messages:
        try:
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=msg_id)
        except:
            pass

    context.user_data.pop('test_session', None)
    context.user_data.pop('current_answers', None)
    context.user_data.pop('current_question', None)
    context.user_data.pop('question_messages', None)

    keyboard = [
        [InlineKeyboardButton("🔄 Qayta yechish", callback_data=f"start_cert_test_{test.id}")],
        [InlineKeyboardButton("🏆 Reyting", callback_data=f"cert_leaderboard_{test.id}")],
        [InlineKeyboardButton("⬅️ Fanga qaytish", callback_data=f"cert_topic_{test.topic.id}")]
    ]

    try:
        await query.message.delete()
    except:
        pass

    await query.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    await query.message.reply_text("Menyu:", reply_markup=main_menu_keyboard())


async def handle_cert_finish_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inline tugma orqali cert testni yakunlash"""
    query = update.callback_query
    await query.answer()
    await finish_cert_from_callback(query, context)


async def cert_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cert test reytingi"""
    query = update.callback_query
    await query.answer()

    test_id = int(query.data.split('_')[-1])
    test = await get_cert_test(test_id)
    if not test:
        await query.edit_message_text("❌ Test topilmadi.")
        return

    top_results = await get_cert_leaderboard(test)

    text = f"🏆 *{test.title} - Reyting*\n\n"

    medals = ['🥇', '🥈', '🥉']
    for i, result in enumerate(top_results):
        medal = medals[i] if i < 3 else f"{i+1}."
        name = result['user__first_name'] or result['user__username']
        text += f"{medal} {name}: {result['best_score']} ball\n"

    if not top_results:
        text += "Hali natijalar yo'q."

    keyboard = [[InlineKeyboardButton("⬅️ Orqaga", callback_data=f"cert_test_{test_id}")]]

    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


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
    app.add_handler(CallbackQueryHandler(cert_leaderboard, pattern=r"^cert_leaderboard_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_cert_inline_answer, pattern=r"^cert_ans_\d+_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_cert_skip, pattern=r"^cert_skip_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_cert_next, pattern="^cert_next$"))
    app.add_handler(CallbackQueryHandler(handle_cert_finish_callback, pattern="^cert_finish$"))
    app.add_handler(MessageHandler(filters.Regex("^🏆 Sertifikatlar$"), handle_certificates_text))
