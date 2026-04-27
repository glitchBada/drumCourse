# DrumCourse — План реализации

## Фаза 1 — Безопасность ✅ ГОТОВО

- [x] Вынести секреты в `.env` через `python-decouple`
- [x] Создать `.env.example` и `.gitignore`
- [x] Исправить `settings.py`: DEBUG, ALLOWED_HOSTS, CORS, CSRF, security headers
- [x] Убрать `@csrf_exempt` — конвертировать `SubmitApplicationView` в DRF APIView
- [x] Защитить blog write-endpoints (POST/PUT/DELETE) — только `is_staff`
- [x] Исправить порядок `CorsMiddleware` (должен быть первым)
- [x] Настроить DRF throttling (rate limiting) для всех auth-эндпоинтов
- [x] Настроить JWT (access 15 мин, refresh 7 дней, blacklist при logout)
- [x] Настроить логирование по уровням (DEBUG в dev, WARNING в prod)

---

## Фаза 2 — Система авторизации ✅ ГОТОВО

- [x] Кастомная модель `User` (AbstractUser + phone_number, email_verified, phone_verified)
- [x] Модель `OTPCode` (6 цифр, 10 мин, макс 3 попытки, timing-safe сравнение)
- [x] Validator номера телефона (E.164: +996XXXXXXXXX)
- [x] Throttle-классы (register/login/otp_verify/otp_resend)
- [x] Сервисы отправки OTP: email (Django SMTP) + WhatsApp (console / Twilio)
- [x] Serializers: Register, Login, OTPVerify, ResendOTP, User
- [x] Views: Register, VerifyOTP, ResendOTP, Login, TokenRefresh, Logout, Me
- [x] URLs: `api/auth/...`
- [x] Admin: UserAdmin, OTPCodeAdmin (readonly, без ручного создания)
- [x] Миграция `0001_initial` для app `accounts`

**Эндпоинты:**
```
POST /api/auth/register/
POST /api/auth/verify-otp/
POST /api/auth/resend-otp/
POST /api/auth/login/
POST /api/auth/token/refresh/
POST /api/auth/logout/
GET  /api/auth/me/
PATCH /api/auth/me/
```

---

## Фаза 3 — Система заявок (с привязкой к аккаунту) ✅ ГОТОВО

### Бэкенд

- [x] Переработать модель `Application`:
  - Добавить `user` (ForeignKey → User)
  - Добавить `type`: `product` (заказ товара) | `trial` (пробный урок)
  - Добавить `product` (ForeignKey → Product, nullable)
  - Добавить `status`: `pending` | `processing` | `cancelled` | `delivered`
  - Добавить `admin_comment` (TextField, обязателен при `cancelled`)
  - Добавить `telegram_message_id` (для редактирования сообщения в Telegram)
  - [x] Добавить `updated_at`
- [x] Логика лимитов:
  - [x] Макс. 5 активных заявок на пользователя (статус не `delivered`)
  - [x] Макс. 2 заявки на пробный урок за 3 недели (с момента последней)
- [x] Логика смены статусов:
  - [x] `pending` → `processing` или `cancelled` — только **Админ**
  - [x] `processing` → `delivered` — только **Пользователь**
  - [x] При `cancelled` — комментарий обязателен
  - [x] `cancelled` и `delivered` — финальные, изменить нельзя
- [x] API эндпоинты:
  ```
  GET  /api/applications/                     — список своих заявок
  POST /api/applications/                     — создать заявку (с проверкой лимитов)
  GET  /api/applications/<id>/                — детали заявки
  POST /api/applications/<id>/confirm/        — подтвердить получение (→ delivered)
  GET  /api/applications/admin/               — все заявки (только staff)
  POST /api/applications/admin/<id>/approve/  — одобрить + комментарий
  POST /api/applications/admin/<id>/cancel/   — отменить + обязательный комментарий
  ```
- [x] Данные пользователя заполняются из `request.user` (не из тела запроса)
- [x] Admin-панель Django: цветные статусы, фильтры, данные пользователей, валидация переходов

---

## Фаза 4 — Telegram-бот с кнопками одобрения/отмены ✅ ГОТОВО

- [x] Авторизация через `/start` + отправка контакта → проверка phone в БД (is_staff)
- [x] Поле `telegram_chat_id` на модели User (заполняется автоматически)
- [x] При создании заявки — сообщение с кнопками [✅ Одобрить] [❌ Отменить] всем подключённым администраторам
- [x] Модель `AdminNotification` — хранит message_id для каждого админа по каждой заявке
- [x] Атомарный захват заявки через `BotPendingAction` (OneToOneField + select_for_update)
- [x] При нажатии кнопки — кнопки убираются у ВСЕХ остальных админов одновременно
- [x] Запрос комментария в диалоге; при отмене комментарий обязателен
- [x] После смены статуса — уведомление всем подключённым администраторам
- [x] Фолбэк: если ни один админ не подключён → сообщение на TELEGRAM_CHAT_ID из .env
- [x] Management command `python manage.py run_bot` для polling-режима (разработка)

---

## Фаза 5 — Фронтенд (React) ✅ ГОТОВО

### Новые страницы
- [x] `/register` — форма регистрации (имя, фамилия, email, телефон, пароль)
- [x] `/verify` — ввод OTP кодов (email + WhatsApp, с кнопкой "Отправить повторно")
- [x] `/login` — форма входа
- [x] `/cabinet` — личный кабинет (защищённый маршрут) + редактирование профиля
- [x] `/cabinet/orders` — история заявок с цветовыми статусами
- [x] `/cabinet/orders/:id` — детали заявки + комментарий администратора

### Компоненты и логика
- [x] `ProtectedRoute` — редирект на `/login` если нет токена
- [x] Axios interceptor — автоматическое обновление access-токена через refresh-cookie
- [x] AuthContext — хранение access-токена в памяти (не localStorage)
- [x] Попап подтверждения получения заказа
- [x] Переработать форму заказа товара — требовать авторизацию
- [x] Переработать контактную форму (пробный урок) — требовать авторизацию

### Безопасность фронтенда
- [x] Установить `dompurify` и применить к `dangerouslySetInnerHTML` в блоге
- [x] Перенести захардкоженные URL в `.env` (`REACT_APP_API_URL`)

---

## Фаза 6 — OTP через WhatsApp (продакшен) ⏳

- [ ] Выбрать провайдера: **Twilio** (международный) или **Wazzup** (популярен в СНГ)
- [ ] Зарегистрировать WhatsApp Business аккаунт (одобрение Meta — 1–4 недели)
- [ ] Добавить `twilio` в requirements.txt
- [ ] Установить `WHATSAPP_PROVIDER=twilio` в `.env` на продакшене
- [ ] Протестировать полный флоу регистрации

---

## Деплой ⏳ (после всех фаз)

- [ ] Мигрировать с SQLite на PostgreSQL
- [ ] Настроить `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` под реальный домен
- [ ] Настроить HTTPS / SSL-сертификат (Let's Encrypt)
- [ ] Настроить SMTP для email (`EMAIL_HOST_USER` и `EMAIL_HOST_PASSWORD` в `.env`)
- [ ] Установить `DEBUG=False` в `.env`
- [ ] Запустить `python manage.py collectstatic`
- [ ] Настроить Nginx + Gunicorn (или uWSGI)

---

## Текущее состояние БД

После каждого изменения моделей запускать:
```bash
python manage.py makemigrations
python manage.py migrate
```

Если меняется `AUTH_USER_MODEL` — нужно пересоздать БД:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```
