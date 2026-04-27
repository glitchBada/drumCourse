from django.contrib import admin
from django.utils.html import format_html

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'colored_status',
        'type',
        'display_product_name',
        'user_full_name',
        'user_phone',
        'user_email',
        'created_at',
        'updated_at',
    ]
    list_filter  = ['status', 'type', 'created_at']
    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__email',
        'user__phone_number',
        'product_name',
        'message',
    ]
    ordering = ['-created_at']
    readonly_fields = [
        'id', 'user', 'type', 'product', 'product_name',
        'display_product_name', 'message', 'telegram_message_id',
        'created_at', 'updated_at',
    ]
    fieldsets = (
        ('Заявка', {
            'fields': ('id', 'type', 'display_product_name', 'message', 'created_at', 'updated_at'),
        }),
        ('Пользователь', {
            'fields': ('user',),
        }),
        ('Управление статусом', {
            'fields': ('status', 'admin_comment'),
            'description': (
                'Допустимые переходы: '
                '<b>В ожидании → В оформлении</b> или <b>В ожидании → Отменён</b>. '
                'При отмене комментарий обязателен.'
            ),
        }),
        ('Telegram', {
            'fields': ('telegram_message_id',),
            'classes': ('collapse',),
        }),
    )

    # ── Отображение ─────────────────────────────────────────────────────

    def colored_status(self, obj: Application) -> str:
        colors = {
            Application.Status.PENDING:    '#f0ad4e',   # жёлтый
            Application.Status.PROCESSING: '#5bc0de',   # синий
            Application.Status.CANCELLED:  '#d9534f',   # красный
            Application.Status.DELIVERED:  '#5cb85c',   # зелёный
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}</span>',
            color,
            obj.get_status_display(),
        )
    colored_status.short_description = 'Статус'

    def user_full_name(self, obj: Application) -> str:
        return f"{obj.user.first_name} {obj.user.last_name}"
    user_full_name.short_description = 'Имя'

    def user_phone(self, obj: Application) -> str:
        return obj.user.phone_number or '—'
    user_phone.short_description = 'Телефон'

    def user_email(self, obj: Application) -> str:
        return obj.user.email
    user_email.short_description = 'Email'

    # ── Валидация при сохранении через админку ──────────────────────────

    def save_model(self, request, obj: Application, form, change):
        if change:
            original = Application.objects.get(pk=obj.pk)

            # Финальные статусы нельзя менять
            if original.status in (Application.Status.CANCELLED, Application.Status.DELIVERED):
                self.message_user(
                    request,
                    f'Статус "{original.get_status_display()}" является финальным и не может быть изменён.',
                    level='ERROR',
                )
                return

            # Пользователь не может менять статус через admin — только admin
            # Валидируем переходы статусов
            allowed_transitions = {
                Application.Status.PENDING: [
                    Application.Status.PROCESSING,
                    Application.Status.CANCELLED,
                ],
            }
            allowed_next = allowed_transitions.get(original.status, [])
            if obj.status != original.status and obj.status not in allowed_next:
                self.message_user(
                    request,
                    f'Недопустимый переход: "{original.get_status_display()}" → "{obj.get_status_display()}".',
                    level='ERROR',
                )
                return

            # При отмене комментарий обязателен
            if obj.status == Application.Status.CANCELLED and not obj.admin_comment.strip():
                self.message_user(
                    request,
                    'При отмене заявки необходимо указать причину в поле "Комментарий администратора".',
                    level='ERROR',
                )
                return

        super().save_model(request, obj, form, change)
