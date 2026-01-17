from django.urls import path
from . import webhook

app_name = 'telegram_bot'

urlpatterns = [
    path('webhook/', webhook.webhook_handler, name='webhook'),
    path('set-webhook/', webhook.set_webhook_view, name='set_webhook'),
    path('delete-webhook/', webhook.delete_webhook_view, name='delete_webhook'),
    path('webhook-info/', webhook.webhook_info_view, name='webhook_info'),
]
