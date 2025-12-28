"""Telegram bot klaviaturalari"""
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# Kanal username
CHANNEL_USERNAME = os.getenv('TELEGRAM_CHANNEL_USERNAME', '@eduself_channel')


def main_menu_keyboard():
    """Asosiy menyu klaviaturasi"""
    keyboard = [
        [KeyboardButton("📚 Fanlar"), KeyboardButton("🏆 Sertifikatlar")],
        [KeyboardButton("📝 Mock Imtihonlar"), KeyboardButton("🏫 Muassasalar")],
        [KeyboardButton("🤖 AI Hamroh"), KeyboardButton("👤 Profil")],
        [KeyboardButton("📊 Reyting"), KeyboardButton("⚙️ Sozlamalar")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def back_to_main_keyboard():
    """Asosiy menyuga qaytish"""
    keyboard = [[KeyboardButton("🏠 Asosiy menyu")]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def channel_subscription_keyboard(callback_action: str = "check_subscription"):
    """Kanal obunasi klaviaturasi"""
    channel_link = CHANNEL_USERNAME.replace('@', '')
    keyboard = [
        [InlineKeyboardButton("📢 Kanalga obuna bo'lish", url=f"https://t.me/{channel_link}")],
        [InlineKeyboardButton("✅ Obunani tekshirish", callback_data=f"{callback_action}")]
    ]
    return InlineKeyboardMarkup(keyboard)


def subjects_keyboard(subjects, page=0, per_page=8):
    """Fanlar ro'yxati klaviaturasi"""
    keyboard = []
    start = page * per_page
    end = start + per_page
    page_subjects = subjects[start:end]

    for i in range(0, len(page_subjects), 2):
        row = []
        for subject in page_subjects[i:i+2]:
            row.append(InlineKeyboardButton(
                f"📖 {subject.name}",
                callback_data=f"subject_{subject.id}"
            ))
        keyboard.append(row)

    # Pagination
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"subjects_page_{page-1}"))
    if end < len(subjects):
        nav_row.append(InlineKeyboardButton("Keyingi ➡️", callback_data=f"subjects_page_{page+1}"))
    if nav_row:
        keyboard.append(nav_row)

    keyboard.append([InlineKeyboardButton("🏠 Asosiy menyu", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)


def topics_keyboard(topics, subject_id):
    """Mavzular ro'yxati klaviaturasi"""
    keyboard = []
    for topic in topics:
        keyboard.append([InlineKeyboardButton(
            f"📑 {topic.name}",
            callback_data=f"topic_{topic.id}"
        )])
    keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data=f"subject_{subject_id}")])
    return InlineKeyboardMarkup(keyboard)


def tests_keyboard(tests, topic_id):
    """Testlar ro'yxati klaviaturasi"""
    keyboard = []
    for test in tests:
        status = "🔓" if test.is_unlocked else "🔒"
        keyboard.append([InlineKeyboardButton(
            f"{status} {test.title}",
            callback_data=f"test_{test.id}"
        )])
    keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data=f"topic_{topic_id}")])
    return InlineKeyboardMarkup(keyboard)


def test_start_keyboard(test_id):
    """Test boshlash klaviaturasi"""
    keyboard = [
        [InlineKeyboardButton("▶️ Testni boshlash", callback_data=f"start_test_{test_id}")],
        [InlineKeyboardButton("🏆 Reyting", callback_data=f"test_leaderboard_{test_id}")],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_tests")]
    ]
    return InlineKeyboardMarkup(keyboard)


def certificates_keyboard(certificates):
    """Sertifikatlar ro'yxati"""
    keyboard = []
    for cert in certificates:
        keyboard.append([InlineKeyboardButton(
            f"🏆 {cert.name}",
            callback_data=f"certificate_{cert.id}"
        )])
    keyboard.append([InlineKeyboardButton("🏠 Asosiy menyu", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)


def mock_exams_keyboard(exams, page=0, per_page=6):
    """Mock imtihonlar ro'yxati"""
    keyboard = []
    start = page * per_page
    end = start + per_page
    page_exams = exams[start:end]

    for exam in page_exams:
        status = "🔓" if exam.is_unlocked else "🔒"
        keyboard.append([InlineKeyboardButton(
            f"{status} {exam.title}",
            callback_data=f"mock_{exam.id}"
        )])

    # Pagination
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⬅️", callback_data=f"mocks_page_{page-1}"))
    if end < len(exams):
        nav_row.append(InlineKeyboardButton("➡️", callback_data=f"mocks_page_{page+1}"))
    if nav_row:
        keyboard.append(nav_row)

    keyboard.append([InlineKeyboardButton("🏠 Asosiy menyu", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)


def institutions_keyboard(institutions, page=0, per_page=5):
    """Muassasalar ro'yxati"""
    keyboard = []
    start = page * per_page
    end = start + per_page
    page_institutions = institutions[start:end]

    for inst in page_institutions:
        keyboard.append([InlineKeyboardButton(
            f"🏫 {inst.name[:40]}",
            callback_data=f"institution_{inst.id}"
        )])

    # Pagination
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⬅️", callback_data=f"inst_page_{page-1}"))
    if end < len(institutions):
        nav_row.append(InlineKeyboardButton("➡️", callback_data=f"inst_page_{page+1}"))
    if nav_row:
        keyboard.append(nav_row)

    keyboard.append([InlineKeyboardButton("🔍 Qidirish", callback_data="search_institutions")])
    keyboard.append([InlineKeyboardButton("🏠 Asosiy menyu", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)


def profile_keyboard():
    """Profil klaviaturasi"""
    keyboard = [
        [InlineKeyboardButton("📊 Statistika", callback_data="profile_stats")],
        [InlineKeyboardButton("📜 Test tarixi", callback_data="profile_history")],
        [InlineKeyboardButton("🔗 Saytga o'tish", url="https://eduself.uz/accounts/profile/")],
        [InlineKeyboardButton("🏠 Asosiy menyu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)


def ai_chat_keyboard():
    """AI chat klaviaturasi"""
    keyboard = [
        [InlineKeyboardButton("💬 Yangi suhbat", callback_data="ai_new_chat")],
        [InlineKeyboardButton("📚 Fan bo'yicha yordam", callback_data="ai_subject_help")],
        [InlineKeyboardButton("🏫 Muassasa tanlash", callback_data="ai_institution_help")],
        [InlineKeyboardButton("🏠 Asosiy menyu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)
