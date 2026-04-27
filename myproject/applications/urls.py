from django.urls import path

from . import views

app_name = 'applications'

urlpatterns = [
    # ── Пользовательские эндпоинты ──────────────────────────────────────
    path(
        '',
        views.ApplicationListCreateView.as_view(),
        name='list-create',
    ),
    path(
        '<int:pk>/',
        views.ApplicationDetailView.as_view(),
        name='detail',
    ),
    path(
        '<int:pk>/confirm/',
        views.ApplicationConfirmView.as_view(),
        name='confirm',
    ),

    # ── Административные эндпоинты ───────────────────────────────────────
    path(
        'admin/',
        views.AdminApplicationListView.as_view(),
        name='admin-list',
    ),
    path(
        'admin/<int:pk>/approve/',
        views.AdminApplicationApproveView.as_view(),
        name='admin-approve',
    ),
    path(
        'admin/<int:pk>/cancel/',
        views.AdminApplicationCancelView.as_view(),
        name='admin-cancel',
    ),
]
