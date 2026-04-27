from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import OTPCode, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'email', 'first_name', 'last_name',
        'phone_number', 'email_verified', 'phone_verified',
        'telegram_connected', 'is_active', 'is_staff', 'date_joined',
    ]
    list_filter = ['email_verified', 'phone_verified', 'is_active', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name', 'phone_number']
    ordering = ['-date_joined']
    readonly_fields = ['date_joined', 'last_login']

    def telegram_connected(self, obj):
        from django.utils.html import format_html
        if obj.telegram_chat_id:
            return format_html('<span style="color:#5cb85c;font-weight:bold;">✔ Подключён</span>')
        return format_html('<span style="color:#d9534f;">✘ Не подключён</span>')
    telegram_connected.short_description = 'Telegram'

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Личные данные', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Верификация', {'fields': ('email_verified', 'phone_verified')}),
        ('Telegram', {'fields': ('telegram_chat_id',)}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name',
                'phone_number', 'password1', 'password2',
                'is_active', 'is_staff',
            ),
        }),
    )


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'purpose', 'is_used', 'attempts', 'expires_at', 'created_at']
    list_filter = ['purpose', 'is_used']
    search_fields = ['user__email', 'user__phone_number']
    readonly_fields = ['user', 'code', 'purpose', 'expires_at', 'attempts', 'is_used', 'created_at']
    ordering = ['-created_at']

    def has_add_permission(self, request) -> bool:
        # OTP-коды создаются только программно, не через админку
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False
