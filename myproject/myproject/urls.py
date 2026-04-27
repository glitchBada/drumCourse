from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from blog.views import post_list, post_detail

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth API
    path('api/auth/', include('accounts.urls', namespace='accounts')),

    # Store API
    path('api/', include('store.urls')),

    # Applications API (пользователь + администратор)
    path('api/applications/', include('applications.urls', namespace='applications')),

    # Reviews API
    path('reviews/', include('reviews.urls')),

    # Blog API
    path('api/posts/', post_list, name='post-list'),
    path('api/posts/<int:pk>/', post_detail, name='post-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
