"""
Создание суперпользователя DrumCourse с запросом номера телефона.

Нормализация номера (+996, Кыргызстан):
  700123456       → +996700123456
  0700123456      → +996700123456
  996700123456    → +996700123456
  +996700123456   → +996700123456

Использование:
    python manage.py createadmin
"""

import getpass
import re

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создать суперпользователя DrumCourse (с именем, фамилией и номером телефона)'

    def add_arguments(self, parser):
        parser.add_argument('--email',      dest='email',      default=None)
        parser.add_argument('--first-name', dest='first_name', default=None)
        parser.add_argument('--last-name',  dest='last_name',  default=None)
        parser.add_argument('--phone',      dest='phone',      default=None)

    def handle(self, *args, **options):
        User = get_user_model()

        self.stdout.write(self.style.MIGRATE_HEADING('\n=== Создание суперпользователя ===\n'))

        email      = options['email']      or self._prompt('Email: ', required=True, validator=self._validate_email)
        first_name = options['first_name'] or self._prompt('Имя: ',   required=True)
        last_name  = options['last_name']  or self._prompt('Фамилия: ', required=True)
        phone      = options['phone']      or self._prompt_phone()
        password   = self._prompt_password()

        if User.objects.filter(email__iexact=email).exists():
            self.stderr.write(self.style.ERROR(f'\nПользователь с email "{email}" уже существует.'))
            return

        user = User.objects.create_superuser(
            username=email.lower(),
            email=email.lower(),
            password=password,
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            phone_number=phone,
            # Суперпользователь считается верифицированным по умолчанию
            email_verified=True,
            phone_verified=True,
        )

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Суперпользователь создан:\n'
            f'   Email   : {user.email}\n'
            f'   Имя     : {user.get_full_name()}\n'
            f'   Телефон : {user.phone_number}\n'
        ))

    # ── Вспомогательные методы ────────────────────────────────────────────

    def _prompt(self, label: str, required: bool = False, validator=None) -> str:
        while True:
            value = input(label).strip()
            if required and not value:
                self.stderr.write('  ⚠ Это поле обязательно.')
                continue
            if validator:
                error = validator(value)
                if error:
                    self.stderr.write(f'  ⚠ {error}')
                    continue
            return value

    def _validate_email(self, value: str):
        if '@' not in value or '.' not in value.split('@')[-1]:
            return 'Введите корректный email.'
        return None

    def _prompt_password(self) -> str:
        self.stdout.write('')
        while True:
            password  = getpass.getpass('Пароль: ')
            password2 = getpass.getpass('Пароль (ещё раз): ')

            if not password:
                self.stderr.write('  ⚠ Пароль не может быть пустым.')
                continue
            if len(password) < 8:
                self.stderr.write('  ⚠ Пароль должен содержать не менее 8 символов.')
                continue
            if password != password2:
                self.stderr.write('  ⚠ Пароли не совпадают. Попробуйте ещё раз.')
                continue
            return password

    def _prompt_phone(self) -> str:
        self.stdout.write(
            '\nНомер телефона (Кыргызстан +996).\n'
            'Можно вводить в любом формате:\n'
            '  700123456       → +996700123456\n'
            '  0700123456      → +996700123456\n'
            '  996700123456    → +996700123456\n'
            '  +996700123456   → +996700123456\n'
        )
        User = get_user_model()

        while True:
            raw = input('Телефон: ').strip()

            if not raw:
                self.stderr.write('  ⚠ Номер телефона обязателен.')
                continue

            phone = _normalize_kg_phone(raw)
            if phone is None:
                self.stderr.write(
                    f'  ⚠ Не удалось распознать номер "{raw}".\n'
                    f'    Пример: 700123456'
                )
                continue

            if User.objects.filter(phone_number=phone).exists():
                self.stderr.write(f'  ⚠ Номер {phone} уже используется другим пользователем.')
                continue

            self.stdout.write(f'  → Номер будет сохранён как: {self.style.SUCCESS(phone)}')
            return phone


# ── Нормализация номера (вынесена для переиспользования) ─────────────────────

def _normalize_kg_phone(raw: str) -> str | None:
    """
    Приводит номер к формату +996XXXXXXXXX (13 символов).
    Возвращает None если формат не распознан.
    """
    # Убираем все незначащие символы
    clean = re.sub(r'[\s\-\(\)\.]', '', raw)

    if clean.startswith('+996'):
        phone = clean
    elif clean.startswith('996'):
        phone = '+' + clean
    elif clean.startswith('0') and len(clean) == 10:
        # 0700123456 → +996700123456
        phone = '+996' + clean[1:]
    elif re.match(r'^\d{9}$', clean):
        # 700123456 → +996700123456
        phone = '+996' + clean
    else:
        return None

    # Финальная проверка: ровно +996 + 9 цифр
    if re.match(r'^\+996\d{9}$', phone):
        return phone

    return None
