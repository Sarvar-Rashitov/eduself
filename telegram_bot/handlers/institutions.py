"""Ta'lim muassasalari handlerlari"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters, ConversationHandler, CommandHandler
from asgiref.sync import sync_to_async
from telegram_bot.keyboards import institutions_keyboard
from telegram_bot.decorators import require_subscription
import time

SEARCH_INSTITUTION = 1


@sync_to_async
def get_institutions():
    from core.models import Institution
    return list(Institution.objects.filter(is_active=True).order_by('order', 'name'))


@sync_to_async
def get_institution(inst_id):
    from core.models import Institution
    try:
        return Institution.objects.get(id=inst_id, is_active=True)
    except Institution.DoesNotExist:
        return None


@sync_to_async
def get_institution_directions(inst):
    return list(inst.directions.filter(is_active=True).order_by('order', 'name'))


@sync_to_async
def get_direction_exams(direction):
    """Yo'nalish imtihonlarini olish"""
    return list(direction.exams.filter(is_active=True).order_by('order', '-created_at'))


@sync_to_async
def get_direction_exam(exam_id):
    """Yo'nalish imtihonini olish"""
    from core.models import DirectionExam
    try:
        return DirectionExam.objects.select_related('direction__institution').prefetch_related('direction_questions').get(id=exam_id, is_active=True)
    except DirectionExam.DoesNotExist:
        return None


@sync_to_async
def get_direction_exam_questions(exam):
    """Yo'nalish imtihon savollarini olish"""
    return list(exam.direction_questions.all().prefetch_related('direction_answers').order_by('order'))


@sync_to_async
def get_direction_exam_question(question_id):
    """Yo'nalish imtihon savolini olish"""
    from core.models import DirectionExamQuestion
    return DirectionExamQuestion.objects.prefetch_related('direction_answers').get(id=question_id)


@sync_to_async
def get_direction_exam_answer(answer_id, question):
    """Yo'nalish imtihon javobini olish"""
    from core.models import DirectionExamAnswer
    return DirectionExamAnswer.objects.get(id=answer_id, question=question)


@sync_to_async
def get_direction_exam_correct_answer(question):
    """To'g'ri javobni olish"""
    return question.direction_answers.filter(is_correct=True).first()


@sync_to_async
def get_direction_exam_best_result(user, exam):
    """Eng yaxshi natijani olish"""
    from core.models import DirectionExamResult
    return DirectionExamResult.objects.filter(user=user, exam=exam).order_by('-score').first()


@sync_to_async
def get_direction_exam_questions_count(exam):
    """Yo'nalish imtihon savollar sonini olish"""
    return exam.get_questions_count()


@sync_to_async
def get_direction_exam_max_points(exam):
    """Yo'nalish imtihon maksimal ballini olish"""
    return exam.get_max_points()


@sync_to_async
def save_direction_exam_result(user, exam, score, total, correct, passed, time_taken, earned_points, answers):
    """Natijani saqlash"""
    from core.models import DirectionExamResult
    DirectionExamResult.objects.create(
        user=user, exam=exam, score=score, total_questions=total,
        correct_answers=correct, passed=passed, time_taken=time_taken,
        earned_points=earned_points, user_answers=answers
    )
    user.total_points += int(earned_points)
    user.save()


@sync_to_async
def search_institutions_db(query):
    from core.models import Institution
    institutions = list(Institution.objects.filter(
        is_active=True,
        name__icontains=query
    ).order_by('name')[:10])
    if not institutions:
        institutions = list(Institution.objects.filter(
            is_active=True,
            short_description__icontains=query
        ).order_by('name')[:10])
    return institutions


@sync_to_async
def get_institution_type_name(inst):
    from core.models import InstitutionType
    return dict(InstitutionType.choices).get(inst.institution_type, inst.institution_type)


@sync_to_async
def get_directions_count(inst):
    """Muassasadagi yo'nalishlar sonini olish"""
    return inst.directions.filter(is_active=True).count()


@sync_to_async
def get_contract_price_range(inst):
    """Kontrakt narxini olish"""
    return inst.get_contract_price_range()


@sync_to_async
def get_admission_period(inst):
    """Qabul muddatini olish"""
    return inst.get_admission_period()


@require_subscription("institutions")
async def institutions_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muassasalar menyusi"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        message = query.message
        edit = True
    else:
        message = update.message
        edit = False

    institutions = await get_institutions()

    if not institutions:
        text = "🏫 Hozircha muassasalar mavjud emas."
        if edit:
            await message.edit_text(text)
        else:
            await message.reply_text(text)
        return

    text = "🏫 *Ta'lim Muassasalari*\n\n"
    text += f"Jami: {len(institutions)} ta muassasa\n\n"
    text += "Muassasani tanlang yoki qidiring:"

    if edit:
        await message.edit_text(text, parse_mode='Markdown', reply_markup=institutions_keyboard(institutions))
    else:
        await message.reply_text(text, parse_mode='Markdown', reply_markup=institutions_keyboard(institutions))


async def institutions_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muassasalar sahifalash"""
    query = update.callback_query
    await query.answer()

    page = int(query.data.split('_')[-1])
    institutions = await get_institutions()

    await query.edit_message_reply_markup(reply_markup=institutions_keyboard(institutions, page))


async def institution_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muassasa tafsilotlari"""
    query = update.callback_query
    await query.answer()

    inst_id = int(query.data.split('_')[-1])

    inst = await get_institution(inst_id)
    if not inst:
        await query.edit_message_text("❌ Muassasa topilmadi.")
        return

    type_name = await get_institution_type_name(inst)

    text = f"🏫 *{inst.name}*\n\n"
    text += f"📋 Turi: {type_name}\n"

    if inst.short_description:
        text += f"\n📝 {inst.short_description}\n"

    if inst.address:
        text += f"\n📍 Manzil: {inst.address}\n"

    if inst.phone:
        text += f"📞 Tel: {inst.phone}\n"

    if inst.email:
        text += f"📧 Email: {inst.email}\n"

    if inst.website:
        text += f"🌐 Sayt: {inst.website}\n"

    price_range = await get_contract_price_range(inst)
    if price_range != "Narx ko'rsatilmagan":
        text += f"\n💰 Kontrakt: {price_range}\n"

    admission = await get_admission_period(inst)
    if admission != "Qabul muddati ko'rsatilmagan":
        text += f"📅 Qabul: {admission}\n"

    directions_count = await get_directions_count(inst)
    if directions_count > 0:
        text += f"\n📚 Yo'nalishlar: {directions_count} ta\n"

    keyboard = []

    if directions_count > 0:
        keyboard.append([InlineKeyboardButton(
            "📚 Yo'nalishlar",
            callback_data=f"inst_directions_{inst_id}"
        )])

    social_row = []
    if inst.telegram:
        social_row.append(InlineKeyboardButton("📱 Telegram", url=inst.telegram))
    if inst.instagram:
        social_row.append(InlineKeyboardButton("📷 Instagram", url=inst.instagram))
    if social_row:
        keyboard.append(social_row)

    if inst.website:
        keyboard.append([InlineKeyboardButton("🌐 Saytga o'tish", url=inst.website)])

    keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="institutions")])

    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def institution_directions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muassasa yo'nalishlari"""
    query = update.callback_query
    await query.answer()

    inst_id = int(query.data.split('_')[-1])

    inst = await get_institution(inst_id)
    if not inst:
        await query.edit_message_text("❌ Muassasa topilmadi.")
        return

    directions = await get_institution_directions(inst)

    text = f"📚 *{inst.name}*\n"
    text += f"*Yo'nalishlar:*\n\n"

    keyboard = []
    for i, direction in enumerate(directions, 1):
        text += f"{i}. *{direction.name}*\n"
        if direction.contract_price:
            text += f"   💰 {direction.contract_price:,.0f} so'm\n"
        text += f"   📖 {direction.get_education_language_display()}\n"
        text += f"   🎓 {direction.get_education_form_display()}\n"
        if direction.passing_score:
            text += f"   ✅ O'tish bali: {direction.passing_score}\n"
        
        # Yo'nalish imtihonlarini tekshirish
        exams = await get_direction_exams(direction)
        if exams:
            text += f"   📝 Imtihonlar: {len(exams)} ta\n"
            keyboard.append([InlineKeyboardButton(
                f"📝 {direction.name} - Imtihonlar",
                callback_data=f"direction_exams_{direction.id}"
            )])
        text += "\n"

    if not directions:
        text += "Yo'nalishlar haqida ma'lumot yo'q."

    keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data=f"institution_{inst_id}")])

    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def search_institutions_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muassasa qidirish boshlash"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🔍 *Muassasa qidirish*\n\n"
        "Muassasa nomini yoki kalit so'zni kiriting:\n\n"
        "_Bekor qilish uchun /cancel_",
        parse_mode='Markdown'
    )
    return SEARCH_INSTITUTION


async def search_institutions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muassasa qidirish"""
    search_query = update.message.text.strip()

    institutions = await search_institutions_db(search_query)

    if not institutions:
        await update.message.reply_text(
            f"❌ '{search_query}' bo'yicha muassasa topilmadi.\n"
            "Boshqa so'z bilan qidiring yoki /cancel buyrug'ini yuboring."
        )
        return SEARCH_INSTITUTION

    text = f"🔍 *'{search_query}' bo'yicha natijalar:*\n\n"
    text += f"Topildi: {len(institutions)} ta\n\n"

    keyboard = []
    for inst in institutions:
        keyboard.append([InlineKeyboardButton(
            f"🏫 {inst.name[:40]}",
            callback_data=f"institution_{inst.id}"
        )])
    keyboard.append([InlineKeyboardButton("🔍 Qayta qidirish", callback_data="search_institutions")])
    keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="institutions")])

    await update.message.reply_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return ConversationHandler.END


async def cancel_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Qidiruvni bekor qilish"""
    await update.message.reply_text("❌ Qidiruv bekor qilindi.")
    return ConversationHandler.END


async def handle_institutions_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muassasalar tugmasi"""
    if update.message.text == "🏫 Muassasalar":
        await institutions_menu(update, context)


def format_timer(seconds):
    """Vaqtni formatlash"""
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"


async def direction_exams_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yo'nalish imtihonlari ro'yxati"""
    query = update.callback_query
    await query.answer()

    direction_id = int(query.data.split('_')[-1])
    
    # Direction obyektini olish uchun
    from core.models import InstitutionDirection
    try:
        direction = await sync_to_async(InstitutionDirection.objects.select_related('institution').get)(id=direction_id, is_active=True)
    except InstitutionDirection.DoesNotExist:
        await query.edit_message_text("❌ Yo'nalish topilmadi.")
        return

    exams = await get_direction_exams(direction)

    text = f"📝 *{direction.institution.name}*\n"
    text += f"*{direction.name} - Imtihonlar*\n\n"

    if not exams:
        text += "Bu yo'nalish uchun imtihonlar mavjud emas."
        keyboard = [[InlineKeyboardButton("⬅️ Orqaga", callback_data=f"inst_directions_{direction.institution.id}")]]
    else:
        keyboard = []
        for exam in exams:
            text += f"📝 *{exam.title}*\n"
            if exam.description:
                text += f"   {exam.description[:100]}...\n"
            text += f"   📚 Fanlar: {exam.subjects}\n"
            text += f"   ⏱ Vaqt: {exam.time_limit} daqiqa\n"
            text += f"   ✅ O'tish bali: {exam.passing_score}\n\n"
            
            keyboard.append([InlineKeyboardButton(
                f"📝 {exam.title}",
                callback_data=f"direction_exam_{exam.id}"
            )])
        
        keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data=f"inst_directions_{direction.institution.id}")])

    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def direction_exam_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yo'nalish imtihon tafsilotlari"""
    query = update.callback_query
    await query.answer()

    try:
        exam_id = int(query.data.split('_')[-1])
        exam = await get_direction_exam(exam_id)
        
        if not exam:
            await query.edit_message_text("❌ Imtihon topilmadi.")
            return

        from telegram_bot.utils import get_user_or_none
        user = await get_user_or_none(update.effective_user.id)
        best_result = await get_direction_exam_best_result(user, exam) if user else None
        
        print(f"Debug: exam object: {exam}")
        print(f"Debug: calling get_direction_exam_questions_count")
        questions_count = await get_direction_exam_questions_count(exam)
        print(f"Debug: questions_count = {questions_count}")
        
        max_points = await get_direction_exam_max_points(exam)

        text = f"📝 *{exam.title}*\n\n"
        text += f"🏫 {exam.direction.institution.name}\n"
        text += f"📚 Yo'nalish: {exam.direction.name}\n\n"
        
        if exam.description:
            text += f"📄 {exam.description}\n\n"
        
        text += f"📚 Fanlar: {exam.subjects}\n"
        text += f"❓ Savollar: {questions_count} ta\n"
        text += f"⏱ Vaqt: {exam.time_limit} daqiqa\n"
        text += f"✅ O'tish bali: {exam.passing_score}\n"
        text += f"🏆 Maksimal ball: {max_points}\n\n"

        if best_result:
            status = "✅ O'tdi" if best_result.passed else "❌ O'tmadi"
            text += f"📊 *Sizning natijangiz:*\n"
            text += f"Ball: {best_result.score:.1f} {status}\n"
            text += f"Olingan ball: {best_result.earned_points}\n\n"

        keyboard = []
        
        if questions_count > 0:
            keyboard.append([InlineKeyboardButton("▶️ Imtihonni boshlash", callback_data=f"start_direction_exam_{exam_id}")])
        
        if exam.application_url and best_result and best_result.passed:
            keyboard.append([InlineKeyboardButton("📝 Ariza qoldirish", url=exam.application_url)])
        
        keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data=f"direction_exams_{exam.direction.id}")])

        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        print(f"Debug: Exception in direction_exam_detail: {e}")
        import traceback
        traceback.print_exc()
        await query.edit_message_text(f"❌ Xatolik: {str(e)}")


async def start_direction_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yo'nalish imtihonini boshlash"""
    query = update.callback_query
    await query.answer()

    from telegram_bot.utils import get_user_or_none
    user = await get_user_or_none(update.effective_user.id)
    if not user:
        await query.answer("❌ Xatolik yuz berdi!", show_alert=True)
        return

    exam_id = int(query.data.split('_')[-1])
    exam = await get_direction_exam(exam_id)
    if not exam:
        await query.edit_message_text("❌ Imtihon topilmadi.")
        return

    questions = await get_direction_exam_questions(exam)
    if not questions:
        await query.answer("❌ Bu imtihonda savollar yo'q!", show_alert=True)
        return

    context.user_data['test_session'] = {
        'test_id': exam_id,
        'test_type': 'direction_exam',
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
        f"🏫 {exam.direction.institution.name}\n"
        f"📚 {exam.direction.name}\n\n"
        f"❓ Savollar soni: {len(questions)}\n"
        f"⏱ Vaqt: {exam.time_limit} daqiqa\n\n"
        f"Javobni tanlash uchun tugmalarni bosing.",
        parse_mode='Markdown'
    )

    await show_direction_exam_question(query, context, questions[0], 1, len(questions))


async def show_direction_exam_question(query, context: ContextTypes.DEFAULT_TYPE, question, num, total):
    """Yo'nalish imtihon savolini ko'rsatish"""
    session = context.user_data.get('test_session')
    if not session:
        return

    answers = list(question.direction_answers.all())

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
        row.append(InlineKeyboardButton(letter, callback_data=f"dir_exam_ans_{question.id}_{answer.id}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([
        InlineKeyboardButton("⏩ O'tkazib yuborish", callback_data=f"dir_exam_skip_{question.id}"),
        InlineKeyboardButton("🏁 Yakunlash", callback_data="dir_exam_finish")
    ])

    msg = await query.message.reply_text(
        text, 
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    context.user_data['question_messages'].append(msg.message_id)


async def handle_direction_exam_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yo'nalish imtihon javobini qabul qilish"""
    query = update.callback_query
    await query.answer()
    
    session = context.user_data.get('test_session')
    if not session or session.get('test_type') != 'direction_exam':
        await query.answer("❌ Faol imtihon topilmadi!", show_alert=True)
        return
    
    parts = query.data.split('_')
    if len(parts) != 5:
        return
    
    question_id = int(parts[3])
    answer_id = int(parts[4])
    
    current_question = context.user_data.get('current_question')
    current_answers = context.user_data.get('current_answers', {})
    
    if not current_question or current_question.id != question_id:
        await query.answer("❌ Bu savol endi aktiv emas!", show_alert=True)
        return
    
    try:
        answer = await get_direction_exam_answer(answer_id, current_question)
        correct_answer = await get_direction_exam_correct_answer(current_question)
        
        session['answers'][str(current_question.id)] = {
            'answer_id': answer_id,
            'is_correct': answer.is_correct
        }
        
        answers = list(current_question.direction_answers.all())
        
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
            session['earned_points'] += float(current_question.points)
            text += "\n\n✅ *To'g'ri javob!*"
        else:
            correct_letter = None
            for letter, ans_id in current_answers.items():
                if correct_answer and ans_id == correct_answer.id:
                    correct_letter = letter
                    break
            text += f"\n\n❌ *Noto'g'ri!* To'g'ri javob: *{correct_letter}*"
        
        keyboard = [[InlineKeyboardButton("➡️ Keyingi savol", callback_data="dir_exam_next")]]
        
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
        
    except Exception as e:
        await query.answer(f"❌ Xatolik: {str(e)}", show_alert=True)


async def handle_direction_exam_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yo'nalish imtihon savolni o'tkazib yuborish"""
    query = update.callback_query
    await query.answer()
    
    session = context.user_data.get('test_session')
    if not session or session.get('test_type') != 'direction_exam':
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
        question = await get_direction_exam_question(next_q_id)
        
        # Hozirgi savolni o'chirish
        try:
            await query.message.delete()
        except:
            pass
        
        await show_direction_exam_question(query, context, question, session['current_index'] + 1, len(session['questions']))
    else:
        await finish_direction_exam(query, context)


async def handle_direction_exam_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Keyingi yo'nalish imtihon savol"""
    query = update.callback_query
    await query.answer()
    
    session = context.user_data.get('test_session')
    if not session or session.get('test_type') != 'direction_exam':
        await query.answer("❌ Faol imtihon topilmadi!", show_alert=True)
        return
    
    session['current_index'] += 1
    
    if session['current_index'] < len(session['questions']):
        next_q_id = session['questions'][session['current_index']]
        question = await get_direction_exam_question(next_q_id)
        
        # Hozirgi savolni o'chirish
        try:
            await query.message.delete()
        except:
            pass
        
        await show_direction_exam_question(query, context, question, session['current_index'] + 1, len(session['questions']))
    else:
        await finish_direction_exam(query, context)


async def finish_direction_exam(query, context: ContextTypes.DEFAULT_TYPE):
    """Yo'nalish imtihonni yakunlash"""
    session = context.user_data.get('test_session')
    if not session:
        from telegram_bot.keyboards import main_menu_keyboard
        await query.message.reply_text("❌ Faol imtihon topilmadi.", reply_markup=main_menu_keyboard())
        return

    from telegram_bot.utils import get_user_or_none
    user = await get_user_or_none(query.from_user.id)
    exam = await get_direction_exam(session['test_id'])

    total = len(session['questions'])
    correct = session['correct_count']
    score = (correct / total) * 100 if total > 0 else 0
    passed = score >= exam.passing_score
    time_taken = int(time.time() - session['start_time'])

    if user:
        await save_direction_exam_result(
            user, exam, score, total, correct, passed,
            time_taken, session['earned_points'], session['answers']
        )

    status = "✅ O'TDINGIZ!" if passed else "❌ O'TMADINGIZ"

    text = f"🏁 *Yo'nalish imtihoni yakunlandi!*\n\n"
    text += f"🏫 {exam.direction.institution.name}\n"
    text += f"📚 {exam.direction.name}\n"
    text += f"📝 {exam.title}\n"
    text += f"━━━━━━━━━━━━━━━\n"
    text += f"📊 *Natija: {status}*\n\n"
    text += f"✅ To'g'ri: {correct}/{total}\n"
    text += f"📈 Ball: {score:.1f}%\n"
    text += f"🏆 Olingan ball: {session['earned_points']}\n"
    text += f"⏱ Vaqt: {time_taken // 60}:{time_taken % 60:02d}\n"

    if passed:
        text += "\n🎉 Tabriklaymiz! Imtihondan o'tdingiz!"
        if exam.application_url:
            text += "\nEndi ariza qoldirish mumkin."
    else:
        text += f"\n💪 O'tish uchun {exam.passing_score} ball kerak."

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
        [InlineKeyboardButton("🔄 Qayta yechish", callback_data=f"start_direction_exam_{exam.id}")],
        [InlineKeyboardButton("⬅️ Imtihonga qaytish", callback_data=f"direction_exam_{exam.id}")]
    ]

    if passed and exam.application_url:
        keyboard.insert(1, [InlineKeyboardButton("📝 Ariza qoldirish", url=exam.application_url)])

    try:
        await query.message.delete()
    except:
        pass

    await query.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    from telegram_bot.keyboards import main_menu_keyboard
    await query.message.reply_text("Menyu:", reply_markup=main_menu_keyboard())


async def handle_direction_exam_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yo'nalish imtihonni yakunlash tugmasi"""
    query = update.callback_query
    await query.answer()
    await finish_direction_exam(query, context)


def register_handlers(app):
    """Institution handlerlarini ro'yxatdan o'tkazish"""
    search_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(search_institutions_start, pattern="^search_institutions$")],
        states={
            SEARCH_INSTITUTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_institutions)]
        },
        fallbacks=[CommandHandler("cancel", cancel_search)],
        allow_reentry=True,
        per_message=False
    )

    app.add_handler(search_conv)
    app.add_handler(CallbackQueryHandler(institutions_menu, pattern="^institutions$"))
    app.add_handler(CallbackQueryHandler(institutions_page, pattern=r"^inst_page_\d+$"))
    app.add_handler(CallbackQueryHandler(institution_detail, pattern=r"^institution_\d+$"))
    app.add_handler(CallbackQueryHandler(institution_directions, pattern=r"^inst_directions_\d+$"))
    
    # Yo'nalish imtihonlari handlerlari
    app.add_handler(CallbackQueryHandler(direction_exams_list, pattern=r"^direction_exams_\d+$"))
    app.add_handler(CallbackQueryHandler(direction_exam_detail, pattern=r"^direction_exam_\d+$"))
    app.add_handler(CallbackQueryHandler(start_direction_exam, pattern=r"^start_direction_exam_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_direction_exam_answer, pattern=r"^dir_exam_ans_\d+_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_direction_exam_skip, pattern=r"^dir_exam_skip_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_direction_exam_next, pattern="^dir_exam_next$"))
    app.add_handler(CallbackQueryHandler(handle_direction_exam_finish, pattern="^dir_exam_finish$"))
    
    app.add_handler(MessageHandler(filters.Regex("^🏫 Muassasalar$"), handle_institutions_text))
