from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from core.sitemaps import (
    StaticViewSitemap, SubjectSitemap, TopicSitemap, TestSitemap,
    CertificateSitemap, CertificateTopicSitemap, CertificateTestSitemap,
    MockExamSitemap, InstitutionSitemap, NewsSitemap, CourseSitemap
)

sitemaps = {
    'static': StaticViewSitemap,
    'subjects': SubjectSitemap,
    'topics': TopicSitemap,
    'tests': TestSitemap,
    'certificates': CertificateSitemap,
    'cert_topics': CertificateTopicSitemap,
    'cert_tests': CertificateTestSitemap,
    'mock_exams': MockExamSitemap,
    'institutions': InstitutionSitemap,
    'news': NewsSitemap,
    'courses': CourseSitemap,
}

urlpatterns = [
    path('nokia/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
    path('humans.txt', TemplateView.as_view(template_name='humans.txt', content_type='text/plain'), name='humans'),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('ai-hamroh/', include('ai_assistant.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
