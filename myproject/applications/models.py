from django.conf import settings
from django.db import models


class Application(models.Model):

    class Type(models.TextChoices):
        PRODUCT = 'product', 'Заказ товара'
        TRIAL   = 'trial',   'Пробный урок'

    class Status(models.TextChoices):
        PENDING    = 'pending',    'В ожидании'
        PROCESSING = 'processing', 'В оформлении и доставке'
        CANCELLED  = 'cancelled',  'Отменён'
        DELIVERED  = 'delivered',  'Заказ доставлен'

    # Статусы, при которых заявка считается "активной" (учитывается в лимите)
    ACTIVE_STATUSES = [Status.PENDING, Status.PROCESSING]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,   # сохраняем историю заявок при удалении юзера
        related_name='applications',
        verbose_name='Пользователь',
    )
    type = models.CharField(
        max_length=10,
        choices=Type.choices,
        verbose_name='Тип заявки',
    )
    product = models.ForeignKey(
        'store.Product',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='applications',
        verbose_name='Товар',
    )
    # Снапшот названия товара на момент подачи заявки.
    # Нужен, чтобы история не ломалась при переименовании/удалении товара.
    product_name = models.CharField(max_length=200, blank=True, verbose_name='Название товара')
    message = models.TextField(blank=True, verbose_name='Сообщение пользователя')
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
        verbose_name='Статус',
    )
    admin_comment = models.TextField(blank=True, verbose_name='Комментарий администратора')
    # ID сообщения в Telegram — нужен в Фазе 4 для редактирования кнопок
    telegram_message_id = models.CharField(max_length=30, blank=True, verbose_name='ID сообщения Telegram')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Заявка #{self.id} [{self.get_type_display()}] — {self.get_status_display()}"

    @property
    def is_active(self) -> bool:
        return self.status in self.ACTIVE_STATUSES

    @property
    def display_product_name(self) -> str:
        """Название товара: снапшот или актуальное из FK, если снапшот пуст."""
        return self.product_name or (self.product.name if self.product else '—')


class AdminNotification(models.Model):
    """
    Хранит ID Telegram-сообщения для каждого администратора по каждой заявке.
    Нужно для того, чтобы при действии одного админа убрать кнопки у всех остальных.
    """

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='admin_notifications',
        verbose_name='Заявка',
    )
    chat_id = models.CharField(max_length=30, verbose_name='Telegram Chat ID администратора')
    message_id = models.CharField(max_length=30, verbose_name='ID сообщения в Telegram')
    # False = кнопки уже убраны (кто-то среагировал)
    is_active = models.BooleanField(default=True, verbose_name='Кнопки активны')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Уведомление администратора'
        verbose_name_plural = 'Уведомления администраторов'
        unique_together = [('application', 'chat_id')]

    def __str__(self) -> str:
        return f"Уведомление заявки #{self.application_id} → chat {self.chat_id}"


class BotPendingAction(models.Model):
    """
    Промежуточное состояние: администратор нажал кнопку и бот ожидает его комментарий.

    OneToOneField к Application гарантирует: только один админ может обрабатывать
    заявку в один момент времени. Второй получит IntegrityError при попытке создать
    запись — это и есть атомарная блокировка.
    """

    class Action(models.TextChoices):
        APPROVE = 'approve', 'Одобрить'
        CANCEL  = 'cancel',  'Отменить'

    # OneToOne: нельзя создать два PendingAction для одной заявки
    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name='pending_action',
        verbose_name='Заявка',
    )
    chat_id = models.CharField(max_length=30, verbose_name='Telegram Chat ID администратора')
    action = models.CharField(max_length=10, choices=Action.choices, verbose_name='Действие')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ожидающее действие бота'
        verbose_name_plural = 'Ожидающие действия бота'

    def __str__(self) -> str:
        return f"PendingAction [{self.action}] заявка #{self.application_id} ← chat {self.chat_id}"
