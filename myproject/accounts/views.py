"""
Auth views для DrumCourse.

Эндпоинты:
  POST /api/auth/register/       — регистрация
  POST /api/auth/verify-otp/     — подтверждение OTP (email или телефон)
  POST /api/auth/resend-otp/     — повторная отправка OTP
  POST /api/auth/login/          — вход (возвращает access-токен, refresh в httpOnly-cookie)
  POST /api/auth/token/refresh/  — обновление access-токена по refresh-cookie
  POST /api/auth/logout/         — выход (инвалидирует refresh-токен)
  GET  /api/auth/me/             — данные текущего пользователя
"""

import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTPCode
from .serializers import (
    LoginSerializer,
    OTPVerifySerializer,
    RegisterSerializer,
    ResendOTPSerializer,
    UserSerializer,
)
from .services import send_email_otp, send_whatsapp_otp
from .throttles import (
    LoginThrottle,
    OTPResendThrottle,
    OTPVerifyThrottle,
    RegisterThrottle,
)

logger = logging.getLogger(__name__)
User = get_user_model()

# Время (в секундах) до которого нельзя снова запрашивать OTP
OTP_RESEND_COOLDOWN_SECONDS = 60


# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------

def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    """Записывает refresh-токен в httpOnly-cookie."""
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=not settings.DEBUG,   # только HTTPS в продакшене
        samesite='Lax',
        max_age=7 * 24 * 60 * 60,   # 7 дней
    )


def _delete_refresh_cookie(response: Response) -> None:
    response.delete_cookie('refresh_token')


# ---------------------------------------------------------------------------
# Регистрация
# ---------------------------------------------------------------------------

class RegisterView(APIView):
    """
    Создаёт аккаунт (is_active=False) и отправляет OTP на email и WhatsApp.
    Аккаунт активируется только после подтверждения обоих каналов.
    """

    throttle_classes = [RegisterThrottle]
    permission_classes = []  # Регистрация доступна без авторизации

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        email_otp = OTPCode.generate(user, OTPCode.Purpose.EMAIL)
        phone_otp = OTPCode.generate(user, OTPCode.Purpose.PHONE)

        failed_channels = []

        try:
            send_email_otp(user, email_otp)
        except Exception as exc:
            logger.error(f"Не удалось отправить email OTP для {user.email}: {exc}")
            failed_channels.append('email')

        try:
            send_whatsapp_otp(user, phone_otp)
        except Exception as exc:
            logger.error(f"Не удалось отправить WhatsApp OTP для {user.phone_number}: {exc}")
            failed_channels.append('whatsapp')

        response_data = {
            'message': (
                'Регистрация успешна. Введите коды подтверждения из email и WhatsApp.'
            ),
            'email': user.email,
        }

        if failed_channels:
            response_data['warning'] = (
                f'Не удалось отправить код через: {", ".join(failed_channels)}. '
                f'Используйте "Отправить повторно".'
            )

        return Response(response_data, status=status.HTTP_201_CREATED)


# ---------------------------------------------------------------------------
# Верификация OTP
# ---------------------------------------------------------------------------

class VerifyOTPView(APIView):
    """
    Принимает OTP-код и помечает email или телефон как подтверждённый.
    Активирует аккаунт (is_active=True) когда оба канала подтверждены.
    """

    throttle_classes = [OTPVerifyThrottle]
    permission_classes = []

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        purpose = serializer.validated_data['purpose']

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            # Не раскрываем, существует ли аккаунт
            return Response(
                {'detail': 'Неверный код или email.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ищем последний действующий (не использованный) OTP нужного типа
        otp = (
            OTPCode.objects
            .filter(user=user, purpose=purpose, is_used=False)
            .order_by('-created_at')
            .first()
        )

        if otp is None or not otp.is_valid():
            return Response(
                {'detail': 'Код недействителен или истёк. Запросите новый код.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not otp.verify(code):
            remaining = otp.MAX_ATTEMPTS - otp.attempts
            if remaining <= 0:
                return Response(
                    {'detail': 'Превышено количество попыток. Запросите новый код.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {'detail': f'Неверный код. Осталось попыток: {remaining}.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Успешная верификация — обновляем поля пользователя
        update_fields = []

        if purpose == OTPCode.Purpose.EMAIL:
            user.email_verified = True
            update_fields.append('email_verified')
        else:
            user.phone_verified = True
            update_fields.append('phone_verified')

        # Активируем аккаунт, если оба канала подтверждены
        if user.email_verified and user.phone_verified and not user.is_active:
            user.is_active = True
            update_fields.append('is_active')

        user.save(update_fields=update_fields)

        if user.is_active:
            message = 'Аккаунт успешно активирован. Теперь вы можете войти.'
        elif purpose == OTPCode.Purpose.EMAIL:
            message = 'Email подтверждён. Введите код из WhatsApp для завершения регистрации.'
        else:
            message = 'Телефон подтверждён. Введите код из email для завершения регистрации.'

        return Response({'message': message})


# ---------------------------------------------------------------------------
# Повторная отправка OTP
# ---------------------------------------------------------------------------

class ResendOTPView(APIView):
    """
    Повторно отправляет OTP-код.
    Ограничен кулдауном 60 секунд (не завязан только на throttle, т.к. throttle
    считается по IP и может обходиться при смене IP).
    """

    throttle_classes = [OTPResendThrottle]
    permission_classes = []

    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        purpose = serializer.validated_data['purpose']

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            # Не раскрываем факт существования аккаунта
            return Response(
                {'message': 'Если аккаунт найден, код будет отправлен повторно.'}
            )

        # Не отправляем, если канал уже верифицирован
        if purpose == OTPCode.Purpose.EMAIL and user.email_verified:
            return Response(
                {'detail': 'Email уже подтверждён.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if purpose == OTPCode.Purpose.PHONE and user.phone_verified:
            return Response(
                {'detail': 'Номер телефона уже подтверждён.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Кулдаун: не разрешаем чаще одного раза в 60 секунд
        last_otp = (
            OTPCode.objects
            .filter(user=user, purpose=purpose)
            .order_by('-created_at')
            .first()
        )
        if last_otp:
            elapsed = (timezone.now() - last_otp.created_at).total_seconds()
            if elapsed < OTP_RESEND_COOLDOWN_SECONDS:
                wait = int(OTP_RESEND_COOLDOWN_SECONDS - elapsed)
                return Response(
                    {'detail': f'Подождите {wait} сек. перед повторной отправкой.'},
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )

        otp = OTPCode.generate(user, purpose)

        try:
            if purpose == OTPCode.Purpose.EMAIL:
                send_email_otp(user, otp)
            else:
                send_whatsapp_otp(user, otp)
        except Exception as exc:
            logger.error(f"Ошибка переотправки OTP ({purpose}) для {email}: {exc}")
            return Response(
                {'detail': 'Ошибка отправки кода. Попробуйте позже.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response({'message': 'Если аккаунт найден, код будет отправлен повторно.'})


# ---------------------------------------------------------------------------
# Вход
# ---------------------------------------------------------------------------

class LoginView(APIView):
    """
    Аутентификация по email + пароль.
    Возвращает access-токен в теле ответа и refresh-токен в httpOnly-cookie.
    """

    throttle_classes = [LoginThrottle]
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        response = Response({
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data,
        })

        _set_refresh_cookie(response, str(refresh))
        return response


# ---------------------------------------------------------------------------
# Обновление access-токена
# ---------------------------------------------------------------------------

class TokenRefreshView(APIView):
    """
    Принимает refresh-токен из httpOnly-cookie,
    возвращает новый access-токен.
    """

    permission_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response(
                {'detail': 'Refresh-токен не найден.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)
        except TokenError:
            return Response(
                {'detail': 'Refresh-токен недействителен или истёк. Войдите снова.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response({'access': new_access})

        # Если ROTATE_REFRESH_TOKENS=True — simplejwt выдаёт новый refresh
        # Обновляем cookie с новым токеном
        if settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS', False):
            _set_refresh_cookie(response, str(refresh))

        return response


# ---------------------------------------------------------------------------
# Выход
# ---------------------------------------------------------------------------

class LogoutView(APIView):
    """
    Инвалидирует refresh-токен (добавляет в blacklist) и удаляет cookie.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass  # Уже инвалидирован — нормально

        response = Response({'message': 'Вы вышли из системы.'})
        _delete_refresh_cookie(response)
        return response


# ---------------------------------------------------------------------------
# Текущий пользователь
# ---------------------------------------------------------------------------

class MeView(APIView):
    """Данные авторизованного пользователя."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        """Частичное обновление профиля (имя, фамилия)."""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)
