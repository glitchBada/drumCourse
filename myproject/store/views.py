from rest_framework import generics
from .models import Category, Product, Brand
from .serializers import CategorySerializer, ProductSerializer, BrandSerializer
# from python_telegram_bot import Bot
import telegram
from django.db.models import Q
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

class NewProductsList(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.order_by('-created_at')[:10]

class BrandList(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        brand = self.request.query_params.get('brand', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        if brand:
            queryset = queryset.filter(brand__slug=brand)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(category__name__icontains=search) | Q(brand__name__icontains=search)
            )
        return queryset

class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class ApplicationView(APIView):
    def post(self, request):
        # Extract data from the request
        product_name = request.data.get('product_name')
        name = request.data.get('name')
        surname = request.data.get('surname')
        phone = request.data.get('phone')
        email = request.data.get('email')

        # Validate required fields
        errors = {}
        for field, value in {
            'product_name': product_name,
            'name': name,
            'surname': surname,
            'phone': phone,
            'email': email
        }.items():
            if not value:
                errors[field] = "Обязательное поле"

        if errors:
            return Response({'status': 'error', 'errors': errors}, status=400)

        # Prepare the Telegram message
        message = (
            f"Новый заказ на:{product_name}\n"
            f"Имя покупателя: {name}\n"
            f"Фамилия: {surname}\n"
            f"Телефон: {phone}\n"
            f"Email: {email}"
        )

        # Send the message to Telegram
        try:
            telegram_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': settings.TELEGRAM_CHAT_ID,
                'text': message
            }
            response = requests.post(telegram_url, json=payload)
            if response.status_code != 200:
                print(f"Failed to send Telegram message: {response.text}")
        except Exception as e:
            print(f"Error sending to Telegram: {str(e)}")

        # Return success response
        return Response({'status': 'Заказ успешно отправлен на расмотрение. Скоро с вами свяжется продавец.'})
# views.py
# from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.conf import settings
# import requests

