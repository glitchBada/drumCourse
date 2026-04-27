"""
Система заявок DrumCourse.

Бизнес-правила:
  - Пользователь не может иметь более 5 активных заявок (pending/processing).
  - Пользователь не может подать более 2 заявок на пробный урок за 3 недели.
  - Статусная машина:
      pending    → processing  (только Admin)
      pending    → cancelled   (только Admin, комментарий обязателен)
      processing → delivered   (только Пользователь-владелец)
      cancelled, delivered — финальные статусы (нельзя изменить)

Telegram-уведомления делегированы в applications/bot.py.
"""

import logging
from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .bot import send_new_application_to_admins, send_status_change_to_admins
from .models import Application
from .serializers import (
    AdminApplicationSerializer,
    AdminStatusUpdateSerializer,
    ApplicationCreateSerializer,
    ApplicationSerializer,
)

logger = logging.getLogger(__name__)

# ── Константы лимитов ────────────────────────────────────────────────────────
ACTIVE_LIMIT      = 5   # макс. активных заявок на пользователя
TRIAL_LIMIT       = 2   # макс. заявок на пробный урок за окно
TRIAL_WINDOW_DAYS = 21  # 3 недели


# ── Вспомогательные функции ──────────────────────────────────────────────────

def _active_count(user) -> int:
    return Application.objects.filter(
        user=user,
        status__in=Application.ACTIVE_STATUSES,
    ).count()


def _trial_count_in_window(user) -> tuple[int, 'Application | None']:
    window_start = timezone.now() - timedelta(days=TRIAL_WINDOW_DAYS)
    qs = Application.objects.filter(
        user=user,
        type=Application.Type.TRIAL,
        created_at__gte=window_start,
    ).order_by('-created_at')
    return qs.count(), qs.first()


# ── Миксин для извлечения заявки ─────────────────────────────────────────────

class _GetApplicationMixin:
    def _get_own(self, request, pk):
        try:
            return Application.objects.get(pk=pk, user=request.user)
        except Application.DoesNotExist:
            return None

    def _get_any(self, pk):
        try:
            return Application.objects.select_related('user', 'product').get(pk=pk)
        except Application.DoesNotExist:
            return None


# ── Пользовательские эндпоинты ───────────────────────────────────────────────

class ApplicationListCreateView(_GetApplicationMixin, APIView):
    """
    GET  /api/applications/  — список заявок текущего пользователя
    POST /api/applications/  — создать новую заявку
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Application.objects.filter(user=request.user).select_related('product')
        return Response(ApplicationSerializer(qs, many=True).data)

    def post(self, request):
        serializer = ApplicationCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        app_type = serializer.validated_data['type']

        # Проверка лимита активных заявок
        active = _active_count(request.user)
        if active >= ACTIVE_LIMIT:
            return Response(
                {
                    'detail': (
                        f'У вас уже {active} активных заявок — это максимум. '
                        f'Дождитесь завершения одной из них.'
                    ),
                    'code': 'active_limit_exceeded',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Проверка лимита пробных уроков
        if app_type == Application.Type.TRIAL:
            trial_count, last_trial = _trial_count_in_window(request.user)
            if trial_count >= TRIAL_LIMIT:
                reset_at = last_trial.created_at + timedelta(days=TRIAL_WINDOW_DAYS)
                return Response(
                    {
                        'detail': (
                            f'Вы исчерпали лимит пробных уроков ({TRIAL_LIMIT} за 3 недели). '
                            f'Следующий можно подать после {reset_at.strftime("%d.%m.%Y %H:%M")} (UTC).'
                        ),
                        'code': 'trial_limit_exceeded',
                        'reset_at': reset_at.isoformat(),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        product = serializer.validated_data.get('product')
        application = Application.objects.create(
            user=request.user,
            type=app_type,
            product=product,
            product_name=product.name if product else '',
            message=serializer.validated_data.get('message', ''),
        )

        # Уведомляем всех подключённых администраторов
        try:
            send_new_application_to_admins(application)
        except Exception as exc:
            logger.error(f"Ошибка отправки Telegram-уведомления для заявки #{application.id}: {exc}")

        return Response(
            ApplicationSerializer(application).data,
            status=status.HTTP_201_CREATED,
        )


class ApplicationDetailView(_GetApplicationMixin, APIView):
    """GET /api/applications/<id>/"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        application = self._get_own(request, pk)
        if application is None:
            return Response({'detail': 'Заявка не найдена.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ApplicationSerializer(application).data)


class ApplicationConfirmView(_GetApplicationMixin, APIView):
    """
    POST /api/applications/<id>/confirm/
    Пользователь подтверждает получение: processing → delivered.
    Фронтенд обязан показать попап-предупреждение перед вызовом.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        application = self._get_own(request, pk)
        if application is None:
            return Response({'detail': 'Заявка не найдена.'}, status=status.HTTP_404_NOT_FOUND)

        if application.status != Application.Status.PROCESSING:
            return Response(
                {
                    'detail': (
                        'Подтвердить получение можно только для заявок '
                        'в статусе "В оформлении и доставке".'
                    ),
                    'current_status': application.status,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        application.status = Application.Status.DELIVERED
        application.save(update_fields=['status', 'updated_at'])

        try:
            send_status_change_to_admins(application)
        except Exception as exc:
            logger.error(f"Ошибка Telegram-уведомления о доставке #{application.id}: {exc}")

        return Response(ApplicationSerializer(application).data)


# ── Административные эндпоинты ───────────────────────────────────────────────

class AdminApplicationListView(APIView):
    """
    GET /api/applications/admin/
    Все заявки. Фильтры: ?status=pending&type=product
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = Application.objects.select_related('user', 'product').all()
        if s := request.query_params.get('status'):
            qs = qs.filter(status=s)
        if t := request.query_params.get('type'):
            qs = qs.filter(type=t)
        return Response(AdminApplicationSerializer(qs, many=True).data)


class AdminApplicationApproveView(APIView):
    """
    POST /api/applications/admin/<id>/approve/
    pending → processing. Тело: { "comment": "..." } (необязательно)
    """
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            application = Application.objects.select_related('user').get(pk=pk)
        except Application.DoesNotExist:
            return Response({'detail': 'Заявка не найдена.'}, status=status.HTTP_404_NOT_FOUND)

        if application.status != Application.Status.PENDING:
            return Response(
                {
                    'detail': 'Одобрить можно только заявки в статусе "В ожидании".',
                    'current_status': application.status,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AdminStatusUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        application.status = Application.Status.PROCESSING
        application.admin_comment = serializer.validated_data.get('comment', '').strip()
        application.save(update_fields=['status', 'admin_comment', 'updated_at'])

        try:
            send_status_change_to_admins(application)
        except Exception as exc:
            logger.error(f"Ошибка Telegram-уведомления об одобрении #{application.id}: {exc}")

        return Response(AdminApplicationSerializer(application).data)


class AdminApplicationCancelView(APIView):
    """
    POST /api/applications/admin/<id>/cancel/
    pending → cancelled. Тело: { "comment": "причина" } (ОБЯЗАТЕЛЬНО)
    """
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            application = Application.objects.select_related('user').get(pk=pk)
        except Application.DoesNotExist:
            return Response({'detail': 'Заявка не найдена.'}, status=status.HTTP_404_NOT_FOUND)

        if application.status != Application.Status.PENDING:
            return Response(
                {
                    'detail': 'Отменить можно только заявки в статусе "В ожидании".',
                    'current_status': application.status,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AdminStatusUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        comment = serializer.validated_data.get('comment', '').strip()
        if not comment:
            return Response(
                {
                    'detail': 'При отмене заявки необходимо указать причину в поле "comment".',
                    'code': 'comment_required',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        application.status = Application.Status.CANCELLED
        application.admin_comment = comment
        application.save(update_fields=['status', 'admin_comment', 'updated_at'])

        try:
            send_status_change_to_admins(application)
        except Exception as exc:
            logger.error(f"Ошибка Telegram-уведомления об отмене #{application.id}: {exc}")

        return Response(AdminApplicationSerializer(application).data)
