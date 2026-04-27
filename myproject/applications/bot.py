"""
Telegram-бот DrumCourse.

Функциональность:
  /start → запрашивает номер телефона → проверяет в БД (is_staff=True) → сохраняет chat_id

  При создании новой заявки (вызывается из views.py):
    → отправляет сообщение с кнопками [✅ Одобрить] [❌ Отменить] ВСЕМ подключённым админам
    → сохраняет ID каждого сообщения в AdminNotification

  Администратор нажимает кнопку:
    → атомарная блокировка через OneToOneField (BotPendingAction)
    → если заблокировать не удалось — другой уже среагировал, кнопки убираются
    → кнопки убираются у ВСЕХ остальных админов
    → бот просит ввести комментарий

  Администратор вводит комментарий:
    → статус заявки меняется
    → уведомление об изменении летит всем подключённым админам

Запуск (разработка):
    python manage.py run_bot

Запуск (продакшен):
    Настроить webhook: python manage.py set_webhook --url https://ваш-домен.com/api/telegram/webhook/
"""

import asyncio
import logging

import requests as sync_requests
from asgiref.sync import sync_to_async
from django.conf import settings
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════
# Синхронные DB-хелперы
# (вызываются через sync_to_async из async-обработчиков бота)
# ═══════════════════════════════════════════════════════════════════════════

def _db_get_admin_by_phone(phone: str):
    """Ищет staff-пользователя по номеру телефона."""
    from accounts.models import User
    if not phone.startswith('+'):
        phone = '+' + phone
    return User.objects.filter(phone_number=phone, is_staff=True).first()


def _db_save_admin_chat_id(user, chat_id: str) -> None:
    user.telegram_chat_id = chat_id
    user.save(update_fields=['telegram_chat_id'])


def _db_get_all_admin_chat_ids() -> list[str]:
    """Возвращает chat_id всех подключённых (is_staff) администраторов."""
    from accounts.models import User
    return list(
        User.objects.filter(is_staff=True)
        .exclude(telegram_chat_id__isnull=True)
        .exclude(telegram_chat_id='')
        .values_list('telegram_chat_id', flat=True)
    )


def _db_try_claim_application(app_id: int, chat_id: str, action: str):
    """
    Атомарная операция захвата заявки одним администратором.

    Алгоритм:
      1. select_for_update — блокируем строку от параллельных изменений
      2. Проверяем статус == pending
      3. Создаём BotPendingAction (OneToOne → IntegrityError если кто-то уже создал)
      4. Деактивируем все AdminNotification для этой заявки

    Возвращает:
      (application, [notifications]) — при успехе
      (None, None)                   — при неудаче (уже обработана)
    """
    from django.db import IntegrityError, transaction
    from applications.models import AdminNotification, Application, BotPendingAction

    with transaction.atomic():
        try:
            app = Application.objects.select_for_update(nowait=True).get(
                pk=app_id,
                status=Application.Status.PENDING,
            )
        except Application.DoesNotExist:
            return None, None
        except Exception:
            # nowait: строка уже заблокирована другой транзакцией
            return None, None

        try:
            BotPendingAction.objects.create(
                application=app,
                chat_id=chat_id,
                action=action,
            )
        except IntegrityError:
            # Другой администратор уже создал BotPendingAction для этой заявки
            return None, None

        notifications = list(
            AdminNotification.objects.filter(application=app, is_active=True)
        )
        AdminNotification.objects.filter(application=app, is_active=True).update(is_active=False)

        return app, notifications


def _db_get_pending_action(chat_id: str):
    """Возвращает ожидающее действие для данного chat_id или None."""
    from applications.models import BotPendingAction
    return (
        BotPendingAction.objects
        .select_related('application__user')
        .filter(chat_id=chat_id)
        .first()
    )


def _db_apply_approve(pending, comment: str):
    from applications.models import Application
    app = pending.application
    app.status = Application.Status.PROCESSING
    app.admin_comment = comment
    app.save(update_fields=['status', 'admin_comment', 'updated_at'])
    pending.delete()
    return app


def _db_apply_cancel(pending, comment: str):
    from applications.models import Application
    app = pending.application
    app.status = Application.Status.CANCELLED
    app.admin_comment = comment
    app.save(update_fields=['status', 'admin_comment', 'updated_at'])
    pending.delete()
    return app


# ═══════════════════════════════════════════════════════════════════════════
# Форматирование сообщений
# ═══════════════════════════════════════════════════════════════════════════

def _format_new_application(application) -> str:
    user = application.user
    emoji = '🛒' if application.type == 'product' else '🥁'
    lines = [
        f"{emoji} <b>Новая заявка #{application.id}</b> — {application.get_type_display()}",
        "━━━━━━━━━━━━━━━━━━",
        f"👤 {user.first_name} {user.last_name}",
        f"📱 {user.phone_number or '—'}",
        f"📧 {user.email}",
        "━━━━━━━━━━━━━━━━━━",
    ]
    if application.type == 'product':
        lines.append(f"📦 Товар: {application.display_product_name}")
    if application.message:
        lines.append(f"💬 {application.message}")
    return "\n".join(lines)


def _format_status_change(application) -> str:
    emoji_map = {
        'processing': '✅',
        'cancelled':  '❌',
        'delivered':  '📬',
    }
    emoji = emoji_map.get(application.status, 'ℹ️')
    lines = [
        f"{emoji} <b>Заявка #{application.id}</b> — статус изменён",
        f"Новый статус: <b>{application.get_status_display()}</b>",
    ]
    if application.admin_comment:
        lines.append(f"Комментарий: {application.admin_comment}")
    return "\n".join(lines)


def _make_inline_keyboard(app_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Одобрить", callback_data=f"approve_{app_id}"),
        InlineKeyboardButton("❌ Отменить", callback_data=f"cancel_{app_id}"),
    ]])


# ═══════════════════════════════════════════════════════════════════════════
# Async-рассылка уведомлений об изменении статуса всем подключённым админам
# ═══════════════════════════════════════════════════════════════════════════

async def _broadcast_status_change(bot, application) -> None:
    chat_ids = await sync_to_async(_db_get_all_admin_chat_ids)()
    text = _format_status_change(application)
    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
        except Exception as exc:
            logger.warning(f"Не удалось отправить уведомление о статусе в {chat_id}: {exc}")


# ═══════════════════════════════════════════════════════════════════════════
# Обработчики бота
# ═══════════════════════════════════════════════════════════════════════════

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /start — приветствие и запрос номера телефона.
    Телефон нужен для сверки с БД и выдачи прав на получение уведомлений.
    """
    keyboard = [[KeyboardButton("📱 Поделиться номером телефона", request_contact=True)]]
    await update.message.reply_text(
        "👋 <b>Панель уведомлений DrumCourse</b>\n\n"
        "Для подключения отправьте ваш номер телефона.\n"
        "Он будет сверен с базой данных администраторов системы.",
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True),
    )


async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Пользователь отправил контакт.
    Проверяем телефон в БД → если is_staff → сохраняем chat_id.
    """
    contact = update.message.contact
    phone = contact.phone_number
    if not phone.startswith('+'):
        phone = '+' + phone

    chat_id = str(update.message.chat_id)

    admin = await sync_to_async(_db_get_admin_by_phone)(phone)

    if admin is None:
        await update.message.reply_text(
            "❌ Номер телефона не найден среди администраторов системы.\n\n"
            "Убедитесь, что ваш номер указан в учётной записи администратора "
            "в формате <code>+996XXXXXXXXX</code>.",
            parse_mode='HTML',
            reply_markup=ReplyKeyboardRemove(),
        )
        return

    await sync_to_async(_db_save_admin_chat_id)(admin, chat_id)

    await update.message.reply_text(
        f"✅ <b>Авторизация успешна!</b>\n\n"
        f"Добро пожаловать, {admin.first_name} {admin.last_name}.\n"
        f"Теперь вы будете получать уведомления о новых заявках.",
        parse_mode='HTML',
        reply_markup=ReplyKeyboardRemove(),
    )
    logger.info(f"Администратор подключён: {admin.email} → chat_id={chat_id}")


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик нажатий inline-кнопок [Одобрить] и [Отменить].

    При нажатии:
      1. Атомарно захватываем заявку (BotPendingAction).
      2. Убираем кнопки у ВСЕХ сообщений этой заявки.
      3. Просим у нажавшего комментарий.
    """
    query = update.callback_query
    await query.answer()

    data = query.data or ''
    if '_' not in data:
        return

    action, app_id_str = data.split('_', 1)
    if action not in ('approve', 'cancel'):
        return

    try:
        app_id = int(app_id_str)
    except ValueError:
        return

    chat_id = str(query.message.chat_id)

    # Атомарный захват
    application, notifications = await sync_to_async(_db_try_claim_application)(
        app_id, chat_id, action
    )

    if application is None:
        # Кто-то другой уже среагировал — убираем кнопки только у текущего сообщения
        try:
            await query.edit_message_reply_markup(reply_markup=None)
        except Exception:
            pass
        await query.message.reply_text(
            "⚠️ Эта заявка уже обрабатывается другим администратором.\n"
            "Дождитесь уведомления о результате."
        )
        return

    # Убираем кнопки у ВСЕХ сообщений этой заявки (у всех подключённых админов)
    for notif in notifications:
        try:
            await context.bot.edit_message_reply_markup(
                chat_id=notif.chat_id,
                message_id=int(notif.message_id),
                reply_markup=None,
            )
        except Exception as exc:
            logger.warning(
                f"Не удалось убрать кнопки: msg={notif.message_id} chat={notif.chat_id}: {exc}"
            )

    # Запрашиваем комментарий у нажавшего
    if action == 'approve':
        await query.message.reply_text(
            f"✅ Вы одобряете заявку <b>#{app_id}</b>.\n\n"
            f"Введите комментарий для пользователя\n"
            f"(или отправьте <code>-</code> чтобы пропустить):",
            parse_mode='HTML',
        )
    else:
        await query.message.reply_text(
            f"❌ Вы отменяете заявку <b>#{app_id}</b>.\n\n"
            f"Укажите причину отмены <b>(обязательно)</b>:",
            parse_mode='HTML',
        )


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик текстовых сообщений.
    Если у администратора есть ожидающее действие — это его комментарий.
    """
    chat_id = str(update.message.chat_id)
    text = update.message.text.strip()

    pending = await sync_to_async(_db_get_pending_action)(chat_id)
    if pending is None:
        return  # Нет ожидающего действия — игнорируем сообщение

    action = pending.action

    if action == BotPendingActionAction.APPROVE:
        comment = '' if text == '-' else text
        app = await sync_to_async(_db_apply_approve)(pending, comment)

        msg = f"✅ Заявка <b>#{app.id}</b> одобрена — статус: <b>В оформлении и доставке</b>"
        if comment:
            msg += f"\nКомментарий: {comment}"
        await update.message.reply_text(msg, parse_mode='HTML')

    elif action == BotPendingActionAction.CANCEL:
        if not text or text == '-':
            await update.message.reply_text(
                "⚠️ Причина отмены обязательна.\nПожалуйста, введите причину:"
            )
            return
        app = await sync_to_async(_db_apply_cancel)(pending, text)
        await update.message.reply_text(
            f"❌ Заявка <b>#{app.id}</b> отменена.\nПричина: {text}",
            parse_mode='HTML',
        )

    else:
        return

    # Оповещаем всех подключённых администраторов об изменении статуса
    await _broadcast_status_change(context.bot, app)


# Локальный алиас чтобы не импортировать модель на уровне модуля
class BotPendingActionAction:
    APPROVE = 'approve'
    CANCEL  = 'cancel'


# ═══════════════════════════════════════════════════════════════════════════
# Синхронная отправка уведомлений из Django view (через HTTP API Telegram)
# ═══════════════════════════════════════════════════════════════════════════

def send_new_application_to_admins(application) -> None:
    """
    Отправляет уведомление о новой заявке всем подключённым администраторам.
    Вызывается синхронно из Django view (не async).

    Если ни один администратор не подключён к боту — отправляет
    на TELEGRAM_CHAT_ID из настроек (фолбэк, без кнопок).
    """
    from accounts.models import User
    from applications.models import AdminNotification

    admins = list(
        User.objects.filter(is_staff=True)
        .exclude(telegram_chat_id__isnull=True)
        .exclude(telegram_chat_id='')
    )

    text = _format_new_application(application)
    keyboard = _make_inline_keyboard_dict(application.id)

    if not admins:
        # Фолбэк: нет подключённых админов — шлём без кнопок на дефолтный chat_id
        _http_send(
            chat_id=settings.TELEGRAM_CHAT_ID,
            text=text + "\n\n<i>⚠️ Подключите бот через /start для управления заявками.</i>",
            reply_markup=None,
        )
        return

    for admin in admins:
        msg_id = _http_send(
            chat_id=admin.telegram_chat_id,
            text=text,
            reply_markup=keyboard,
        )
        if msg_id:
            AdminNotification.objects.update_or_create(
                application=application,
                chat_id=admin.telegram_chat_id,
                defaults={'message_id': str(msg_id), 'is_active': True},
            )


def send_status_change_to_admins(application) -> None:
    """
    Уведомляет всех подключённых администраторов об изменении статуса.
    Вызывается синхронно из Django view.
    """
    from accounts.models import User

    admins = list(
        User.objects.filter(is_staff=True)
        .exclude(telegram_chat_id__isnull=True)
        .exclude(telegram_chat_id='')
    )
    text = _format_status_change(application)

    for admin in admins:
        _http_send(chat_id=admin.telegram_chat_id, text=text, reply_markup=None)


def _make_inline_keyboard_dict(app_id: int) -> dict:
    return {
        'inline_keyboard': [[
            {'text': '✅ Одобрить', 'callback_data': f'approve_{app_id}'},
            {'text': '❌ Отменить', 'callback_data': f'cancel_{app_id}'},
        ]]
    }


def _http_send(chat_id: str, text: str, reply_markup) -> str | None:
    """
    Отправляет сообщение через Telegram HTTP API (синхронно через requests).
    Возвращает message_id при успехе или None.
    """
    payload = {
        'chat_id':    chat_id,
        'text':       text,
        'parse_mode': 'HTML',
    }
    if reply_markup is not None:
        payload['reply_markup'] = reply_markup

    try:
        resp = sync_requests.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json=payload,
            timeout=5,
        )
        if resp.status_code == 200:
            return str(resp.json().get('result', {}).get('message_id', ''))
        logger.warning(f"Telegram API {resp.status_code}: {resp.text[:200]}")
    except sync_requests.RequestException as exc:
        logger.error(f"Telegram HTTP error → chat {chat_id}: {exc}")
    return None


# ═══════════════════════════════════════════════════════════════════════════
# Точка запуска бота (polling)
# ═══════════════════════════════════════════════════════════════════════════

async def run_polling() -> None:
    """
    Запускает бота в режиме polling (для разработки).
    Для продакшена используйте webhook.
    """
    # ApplicationBuilder — из python-telegram-bot; не путать с Django Application
    ptb_app = (
        ApplicationBuilder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .build()
    )

    ptb_app.add_handler(CommandHandler('start', start_command))
    ptb_app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    ptb_app.add_handler(CallbackQueryHandler(callback_handler))
    # TEXT & ~COMMAND — текстовые сообщения кроме команд (для ввода комментария)
    ptb_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    logger.info("Telegram bot запущен в режиме polling")

    async with ptb_app:
        await ptb_app.start()
        await ptb_app.updater.start_polling(drop_pending_updates=True)
        # Ждём бесконечно — прерывается Ctrl+C (KeyboardInterrupt)
        await asyncio.Event().wait()
