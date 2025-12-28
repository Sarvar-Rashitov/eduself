"""Telegram bot konfiguratsiyasi"""
import os
from dotenv import load_dotenv

load_dotenv()

# Bot sozlamalari
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BOT_USERNAME = os.getenv('TELEGRAM_BOT_USERNAME', 'edu_self_bot')
SITE_URL = os.getenv('SITE_URL', 'https://eduself.uz')

# Django sozlamalari
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduself.settings')
django.setup()
