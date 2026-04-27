"""
Команда для запуска Telegram-бота в режиме polling (разработка).

Использование:
    python manage.py run_bot

Для продакшена настройте webhook:
    python manage.py set_webhook --url https://ваш-домен.com/api/telegram/webhook/
"""

import asyncio
import logging

from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Запустить Telegram-бота в режиме polling (для разработки)'

    def handle(self, *args, **options):
        from applications.bot import run_polling

        self.stdout.write(self.style.SUCCESS('Запуск Telegram-бота (polling)...'))
        self.stdout.write('Нажмите Ctrl+C для остановки.\n')

        try:
            asyncio.run(run_polling())
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nБот остановлен.'))
