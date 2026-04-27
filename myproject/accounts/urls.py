from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/',      views.RegisterView.as_view(),     name='register'),
    path('verify-otp/',    views.VerifyOTPView.as_view(),    name='verify-otp'),
    path('resend-otp/',    views.ResendOTPView.as_view(),    name='resend-otp'),
    path('login/',         views.LoginView.as_view(),        name='login'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/',        views.LogoutView.as_view(),       name='logout'),
    path('me/',            views.MeView.as_view(),           name='me'),
]
