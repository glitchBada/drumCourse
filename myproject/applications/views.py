from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import Application
import json
from django.conf import settings


@csrf_exempt
def submit_application(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Валидация данных
            errors = {}
            for field in ['firstName', 'lastName', 'phoneNumber', 'email', 'message']:
                if not data.get(field):
                    errors[field] = "Обязательное поле"

            if errors:
                return JsonResponse({'status': 'error', 'errors': errors}, status=400)

            # Сохранение в базу
            application = Application.objects.create(
                first_name=data['firstName'],
                last_name=data['lastName'],
                phone_number=data['phoneNumber'],
                email=data['email'],
                message=data['message']
            )

            # Отправка в Telegram
            try:
                telegram_message = f"Новая заявка:\nИмя: {data['firstName']}\nФамилия: {data['lastName']}\nТелефон: {data['phoneNumber']}\nEmail: {data['email']}\nСообщение: {data['message']}"
                requests.post(
                    f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                    json={'chat_id': settings.TELEGRAM_CHAT_ID, 'text': telegram_message}
                )
            except Exception as e:
                print(f"Ошибка отправки в Telegram: {str(e)}")

            return JsonResponse({'status': 'success', 'id': application.id})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)