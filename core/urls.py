from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    
    path('subjects/', views.subjects_view, name='subjects'),
    path('subjects/<int:pk>/', views.subject_detail_view, name='subject_detail'),
    path('topics/<int:pk>/', views.topic_detail_view, name='topic_detail'),
    path('tests/<int:pk>/leaderboard/', views.test_leaderboard_view, name='test_leaderboard'),
    path('tests/<int:pk>/', views.take_test_view, name='take_test'),
    path('tests/<int:pk>/result/', views.test_result_view, name='test_result'),
    path('tests/<int:pk>/analysis/', views.test_analysis_view, name='test_analysis'),
    path('check-answer/<int:question_id>/<int:answer_id>/', views.check_answer_view, name='check_answer'),
    
    path('certificates/', views.certificates_view, name='certificates'),
    path('certificates/<int:pk>/', views.certificate_detail_view, name='certificate_detail'),
    path('cert-topics/<int:pk>/', views.cert_topic_detail_view, name='cert_topic_detail'),
    path('cert-tests/<int:pk>/leaderboard/', views.cert_test_leaderboard_view, name='cert_test_leaderboard'),
    path('cert-tests/<int:pk>/', views.take_cert_test_view, name='take_cert_test'),
    path('cert-tests/<int:pk>/result/', views.cert_test_result_view, name='cert_test_result'),
    path('cert-tests/<int:pk>/analysis/', views.cert_test_analysis_view, name='cert_test_analysis'),
    path('check-cert-answer/<int:question_id>/<int:answer_id>/', views.check_cert_answer_view, name='check_cert_answer'),
    
    path('mock-exams/', views.mock_exams_view, name='mock_exams'),
    path('mock-exams/<int:pk>/leaderboard/', views.mock_exam_leaderboard_view, name='mock_exam_leaderboard'),
    path('mock-exams/<int:pk>/', views.take_mock_exam_view, name='take_mock_exam'),
    path('mock-exams/<int:pk>/result/', views.mock_exam_result_view, name='mock_exam_result'),
    path('mock-exams/<int:pk>/analysis/', views.mock_exam_analysis_view, name='mock_exam_analysis'),
    path('check-mock-answer/<int:question_id>/<int:answer_id>/', views.check_mock_answer_view, name='check_mock_answer'),
    
    path('leaderboard/', views.global_leaderboard_view, name='global_leaderboard'),
    
    path('institutions/', views.institutions_view, name='institutions'),
    path('institutions/<int:pk>/', views.institution_detail_view, name='institution_detail'),
    path('directions/<int:pk>/', views.direction_detail_view, name='direction_detail'),
    
    # Yo'nalish imtihonlari
    path('direction-exam/<int:pk>/intro/', views.direction_exam_intro_view, name='direction_exam_intro'),
    path('direction-exam/<int:pk>/', views.take_direction_exam_view, name='take_direction_exam'),
    path('direction-exam/<int:pk>/result/', views.direction_exam_result_view, name='direction_exam_result'),
    path('direction-exam/<int:pk>/analysis/', views.direction_exam_analysis_view, name='direction_exam_analysis'),
    
    path('news/', views.news_list_view, name='news_list'),
    path('news/<slug:slug>/', views.news_detail_view, name='news_detail'),
    
    path('courses/', views.courses_view, name='courses'),
    path('courses/<slug:slug>/', views.course_detail_view, name='course_detail'),
    path('courses/<slug:course_slug>/lesson/<int:lesson_id>/', views.lesson_detail_view, name='lesson_detail'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('courses/<int:course_id>/enroll-paid/', views.enroll_paid_course, name='enroll_paid_course'),
    
    path('notification/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]
