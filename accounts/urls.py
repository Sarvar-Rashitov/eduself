from django.urls import path
from . import views
from . import onboarding_views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/<uuid:token>/', views.reset_password_view, name='reset_password'),
    path('profile/', views.profile_view, name='profile'),
    path('verify-email/<uuid:token>/', views.verify_email_view, name='verify_email'),
    path('resend-verification/', views.resend_verification_view, name='resend_verification'),
    path('auth/google/', views.google_auth_view, name='google_auth'),
    path('auth/telegram/', views.telegram_auth_view, name='telegram_auth'),
    path('telegram-callback/', views.telegram_callback_view, name='telegram_callback'),
    path('auth/telegram-miniapp/', views.telegram_miniapp_auth_view, name='telegram_miniapp_auth'),
    
    # Onboarding URLs
    path('onboarding/', onboarding_views.onboarding_view, name='onboarding'),
    path('onboarding/save/', onboarding_views.save_onboarding, name='save_onboarding'),
    path('onboarding/skip/', onboarding_views.skip_onboarding, name='skip_onboarding'),
    path('onboarding/show-all/', onboarding_views.show_all_platform, name='show_all_platform'),
    path('onboarding/return-to-interests/', onboarding_views.return_to_interests, name='return_to_interests'),
    path('onboarding/reset/', onboarding_views.reset_onboarding, name='reset_onboarding'),
]
