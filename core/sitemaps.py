from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import (
    Subject, Topic, Test,
    Certificate, CertificateTopic, CertificateTest,
    MockExam, MockExamCategory,
    Institution, InstitutionCategory,
    News, Course
)


class StaticViewSitemap(Sitemap):
    """Statik sahifalar uchun sitemap"""
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['core:home', 'core:subjects', 'core:certificates', 
                'core:mock_exams', 'core:institutions', 'core:courses',
                'core:news_list', 'core:global_leaderboard']

    def location(self, item):
        return reverse(item)


class SubjectSitemap(Sitemap):
    """Fanlar uchun sitemap"""
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Subject.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('core:subject_detail', args=[obj.pk])


class TopicSitemap(Sitemap):
    """Mavzular uchun sitemap"""
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Topic.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('core:topic_detail', args=[obj.pk])


class TestSitemap(Sitemap):
    """Testlar uchun sitemap"""
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Test.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('core:take_test', args=[obj.pk])


class CertificateSitemap(Sitemap):
    """Sertifikatlar uchun sitemap"""
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Certificate.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('core:certificate_detail', args=[obj.pk])


class CertificateTopicSitemap(Sitemap):
    """Sertifikat mavzulari uchun sitemap"""
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return CertificateTopic.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('core:cert_topic_detail', args=[obj.pk])


class CertificateTestSitemap(Sitemap):
    """Sertifikat testlari uchun sitemap"""
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return CertificateTest.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('core:take_cert_test', args=[obj.pk])


class MockExamSitemap(Sitemap):
    """Mock imtihonlar uchun sitemap"""
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return MockExam.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('core:take_mock_exam', args=[obj.pk])


class InstitutionSitemap(Sitemap):
    """Ta'lim muassasalari uchun sitemap"""
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Institution.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('core:institution_detail', args=[obj.pk])


class NewsSitemap(Sitemap):
    """Yangiliklar uchun sitemap"""
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        return News.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('core:news_detail', args=[obj.slug])


class CourseSitemap(Sitemap):
    """Kurslar uchun sitemap"""
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Course.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('core:course_detail', args=[obj.slug])
