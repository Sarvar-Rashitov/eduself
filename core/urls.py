from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    
    path('subjects/', views.subjects_view, name='subjects'),
    path('subjects/<int:pk>/', views.subject_detail_view, name='subject_detail'),
    path('topics/<int:pk>/', views.topic_detail_view, name='topic_detail'),
    path('tests/<int:pk>/', views.take_test_view, name='take_test'),
    path('tests/<int:pk>/result/', views.test_result_view, name='test_result'),
    
    path('certificates/', views.certificates_view, name='certificates'),
    path('certificates/<int:pk>/', views.certificate_detail_view, name='certificate_detail'),
    path('cert-topics/<int:pk>/', views.cert_topic_detail_view, name='cert_topic_detail'),
    path('cert-tests/<int:pk>/', views.take_cert_test_view, name='take_cert_test'),
    path('cert-tests/<int:pk>/result/', views.cert_test_result_view, name='cert_test_result'),
    
    path('mock-exams/', views.mock_exams_view, name='mock_exams'),
    path('mock-exams/<int:pk>/', views.take_mock_exam_view, name='take_mock_exam'),
    path('mock-exams/<int:pk>/result/', views.mock_exam_result_view, name='mock_exam_result'),
    
    path('institutions/', views.institutions_view, name='institutions'),
    path('institutions/<int:pk>/', views.institution_detail_view, name='institution_detail'),
]
