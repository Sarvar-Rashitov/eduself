"""Telegram webhook o'rnatish command"""
import os
import asyncio
from django.core.management.base import BaseCommand
from telegram import Bot


class Command(BaseCommand):
    help = 'Telegram bot webhook o\'rnatish'

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, help='Webhook URL')
        parser.add_argument('--delete', action='store_true', help='Webhook o\'chirish')

    def handle(self, *args, **options):
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not bot_token:
            self.stdout.write(self.style.ERROR('TELEGRAM_BOT_TOKEN topilmadi!'))
            return

        bot = Bot(token=bot_token)

        async def set_webhook():
            if options['delete']:
                await bot.delete_webhook()
                self.stdout.write(self.style.SUCCESS('Webhook o\'chirildi'))
                return

            webhook_url = options['url']
            if not webhook_url:
                site_url = os.getenv('SITE_URL', '').rstrip('/')
                if not site_url:
                    self.stdout.write(self.style.ERROR('SITE_URL yoki --url parametri kerak!'))
                    return
                webhook_url = f"{site_url}/telegram/webhook/"

            await bot.set_webhook(url=webhook_url)
            info = await bot.get_webhook_info()
            
            self.stdout.write(self.style.SUCCESS(f'Webhook o\'rnatildi: {info.url}'))
            self.stdout.write(f'Pending updates: {info.pending_update_count}')

        asyncio.run(set_webhook())