"""
Сервисный слой для отправки OTP-кодов.
Поддерживает два канала: email (Django SMTP) и WhatsApp (Twilio / console).

Для переключения провайдера WhatsApp измените WHATSAPP_PROVIDER в .env:
  console — выводит код в терминал (только для разработки)
  twilio  — отправляет через Twilio WhatsApp Business API
"""

import logging

from django.conf import settings
from django.core.mail import send_mail

from .models import OTPCode, User

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Email OTP
# ---------------------------------------------------------------------------

def send_email_otp(user: User, otp: OTPCode) -> None:
    """
    Отправляет OTP-код на email пользователя.
    В режиме DEBUG используется EmailBackend=console (см. settings.py).
    """
    subject = 'Код подтверждения — DrumCourse'
    body = (
        f'Здравствуйте, {user.first_name}!\n\n'
        f'Ваш код подтверждения: {otp.code}\n\n'
        f'Код действителен {otp.EXPIRY_MINUTES} минут.\n'
        f'Никому не сообщайте этот код.\n\n'
        f'Если вы не создавали аккаунт на DrumCourse — проигнорируйте это письмо.'
    )
    # Исключения намеренно не перехватываются здесь:
    # вызывающий код (view) решает, как реагировать на ошибку отправки.
    send_mail(
        subject=subject,
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
    logger.info(f"Email OTP отправлен: {user.email}")


# ---------------------------------------------------------------------------
# WhatsApp OTP
# ---------------------------------------------------------------------------

def send_whatsapp_otp(user: User, otp: OTPCode) -> None:
    """
    Отправляет OTP-код через WhatsApp.
    Провайдер выбирается через настройку WHATSAPP_PROVIDER.
    """
    provider = getattr(settings, 'WHATSAPP_PROVIDER', 'console')

    if provider == 'console':
        _send_console(user, otp)
    elif provider == 'twilio':
        _send_twilio(user.phone_number, otp.code)
    else:
        raise ValueError(f"Неизвестный WHATSAPP_PROVIDER: '{provider}'")


def _send_console(user: User, otp: OTPCode) -> None:
    """Режим разработки: код выводится в терминал."""
    separator = '=' * 50
    logger.info(
        f"\n{separator}\n"
        f"  WhatsApp OTP [CONSOLE MODE]\n"
        f"  Пользователь : {user.get_full_name()} ({user.email})\n"
        f"  Телефон      : {user.phone_number}\n"
        f"  Код          : {otp.code}\n"
        f"  Истекает     : {otp.expires_at.strftime('%H:%M:%S')}\n"
        f"{separator}"
    )


def _send_twilio(phone_number: str, code: str) -> None:
    """Отправка через Twilio WhatsApp Business API."""
    try:
        from twilio.rest import Client  # noqa: PLC0415
    except ImportError as exc:
        raise RuntimeError(
            "Пакет 'twilio' не установлен. Выполните: pip install twilio"
        ) from exc

    message_body = (
        f"DrumCourse: ваш код подтверждения — *{code}*\n"
        f"Код действителен 10 минут. Никому его не сообщайте."
    )
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message_body,
        from_=settings.TWILIO_WHATSAPP_FROM,
        to=f'whatsapp:{phone_number}',
    )
    logger.info(f"WhatsApp OTP отправлен через Twilio: {phone_number}")
