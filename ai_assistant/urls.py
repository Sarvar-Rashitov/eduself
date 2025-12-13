from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    # AI Chat
    path('', views.ai_chat_redirect, name='chat_redirect'),
    path('chat/', views.ai_chat_view, name='chat'),
    path('chat/<int:session_id>/', views.ai_chat_view, name='chat_session'),
    
    # API endpoints
    path('api/send-message/', views.send_message, name='send_message'),
    path('api/session/<int:session_id>/messages/', views.get_session_messages, name='session_messages'),
    path('api/session/<int:session_id>/delete/', views.delete_session, name='delete_session'),
    
    # Yordam sahifalari
    path('help/', views.ai_help_center, name='help_center'),
    path('quick-question/', views.quick_question, name='quick_question'),
    path('recommendations/', views.institution_recommendations, name='institution_recommendations'),
]