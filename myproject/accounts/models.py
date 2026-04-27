import secrets
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    Используем email как основной идентификатор входа.
    Аккаунт неактивен (is_active=False) до подтверждения email и телефона.
    """

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    # Заполняется автоматически при подключении администратора через /start в боте.
    # null=True + unique=True: в большинстве СУБД несколько NULL не нарушают уникальность.
    telegram_chat_id = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Telegram Chat ID',
        help_text='Заполняется автоматически при подключении через бот (/start).',
    )

    # username не используется для входа, но поле обязательно для AbstractUser.
    # Мы записываем туда email при регистрации.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self) -> str:
        return f"{self.get_full_name()} <{self.email}>"


class OTPCode(models.Model):
    """
    Одноразовый код подтверждения (6 цифр).
    Используется для верификации email и номера телефона при регистрации.
    """

    class Purpose(models.TextChoices):
        EMAIL = 'email', 'Email'
        PHONE = 'phone', 'Телефон'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='otp_codes',
    )
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=10, choices=Purpose.choices)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    # Счётчик неверных попыток; при превышении MAX_ATTEMPTS код блокируется
    attempts = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    MAX_ATTEMPTS = 3
    EXPIRY_MINUTES = 10

    class Meta:
        verbose_name = 'OTP-код'
        verbose_name_plural = 'OTP-коды'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"OTP [{self.purpose}] для {self.user.email}"

    @classmethod
    def generate(cls, user: User, purpose: str) -> 'OTPCode':
        """
        Инвалидирует все предыдущие неиспользованные коды данного типа
        и создаёт новый с криптографически стойкой случайностью.
        """
        # Помечаем старые коды как использованные одним запросом к БД
        cls.objects.filter(user=user, purpose=purpose, is_used=False).update(is_used=True)

        # secrets.randbelow гарантирует равномерное распределение без bias
        code = f"{secrets.randbelow(1_000_000):06d}"
        expires_at = timezone.now() + timedelta(minutes=cls.EXPIRY_MINUTES)

        return cls.objects.create(
            user=user,
            code=code,
            purpose=purpose,
            expires_at=expires_at,
        )

    def is_valid(self) -> bool:
        """Код действителен, если не использован, не истёк и есть попытки."""
        return (
            not self.is_used
            and self.attempts < self.MAX_ATTEMPTS
            and timezone.now() < self.expires_at
        )

    def verify(self, submitted_code: str) -> bool:
        """
        Проверяет код. Увеличивает счётчик попыток при каждом вызове.
        Возвращает True только при верном коде.
        Использует сравнение через secrets.compare_digest для защиты от timing-атак.
        """
        if not self.is_valid():
            return False

        self.attempts += 1
        # Сравниваем за постоянное время, чтобы нельзя было угадать код по задержке
        match = secrets.compare_digest(self.code, submitted_code)

        if match:
            self.is_used = True

        self.save(update_fields=['attempts', 'is_used'])
        return match
