from django.urls import path
from .views import ReviewListAPIView

urlpatterns = ([
    path('api/reviews/', ReviewListAPIView.as_view(), name='reviews-api'),
])
               # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))