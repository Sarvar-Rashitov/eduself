from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    # EduSelf Pro sahifasi
    path('pro/', views.pro_page, name='pro_page'),
    
    # Obuna sotib olish
    path('subscribe/<slug:plan_slug>/', views.subscribe, name='subscribe'),
    
    # Promokod tekshirish
    path('check-promo/', views.check_promo_code, name='check_promo'),
    
    # Referal
    path('referral/', views.referral_page, name='referral'),
    path('referral/invite/', views.send_referral_invite, name='send_invite'),
    
    # To'lov callback'lari
    path('payment/click/prepare/', views.click_prepare, name='click_prepare'),
    path('payment/click/complete/', views.click_complete, name='click_complete'),
    path('payment/payme/callback/', views.payme_callback, name='payme_callback'),
    
    # Donat
    path('donate/', views.donate_page, name='donate'),
    path('donate/process/', views.process_donation, name='process_donation'),
    
    # Foydalanuvchi obunalari
    path('my-subscriptions/', views.my_subscriptions, name='my_subscriptions'),
    
    # API endpoints
    path('api/plans/', views.api_subscription_plans, name='api_subscription_plans'),
]
