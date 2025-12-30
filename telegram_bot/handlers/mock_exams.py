"""Mock imtihonlar handlerlari - ReplyKeyboard bilan"""
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
        [KeyboardButton("🅰️"), KeyboardButton("🅱️"), KeyboardButton("🅲"), KeyboardButton("🅳")],
        [KeyboardButton("⏩ O'tkazib yuborish"), KeyboardButton("🏁 Yakunlash")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def format_timer(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"
