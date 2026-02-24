"""
Management command to populate translation cache
Database cache'ni tarjimalar bilan to'ldirish
"""
from django.core.management.base import BaseCommand
from django.db.models import Q
from core.models import (
    Subject, Topic, Certificate, CertificateTopic, CertificateTest,
    MockExam, Institution, InstitutionDirection, News, Course, Lesson,
    SubjectCategory, MockExamCategory, InstitutionCategory, NewsCategory, CourseCategory
)
from core.translation import translator
import time


class Command(BaseCommand):
    help = 'Populate translation cache with common texts'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--target-lang',
            type=str,
            default='ru',
            help='Target language code (default: ru)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limit number of items to translate per model'
        )
        parser.add_argument(
            '--models',
            type=str,
            nargs='+',
            default=['all'],
            help='Models to translate (subject, topic, certificate, etc.)'
        )
    
    def handle(self, *args, **options):
        target_lang = options['target_lang']
        limit = options['limit']
        models = options['models']
        
        self.stdout.write(self.style.SUCCESS(f'\n🚀 Starting translation cache population'))
        self.stdout.write(self.style.SUCCESS(f'Target language: {target_lang}'))
        self.stdout.write(self.style.SUCCESS(f'Limit per model: {limit or "No limit"}\n'))
        
        total_translated = 0
        
        # Subject Categories
        if 'all' in models or 'subject_category' in models:
            total_translated += self._translate_model(
                SubjectCategory, 
                ['name', 'description'], 
                target_lang, 
                limit,
                'Subject Categories'
            )
        
        # Subjects
        if 'all' in models or 'subject' in models:
            total_translated += self._translate_model(
                Subject, 
                ['name', 'description'], 
                target_lang, 
                limit,
                'Subjects'
            )
        
        # Topics
        if 'all' in models or 'topic' in models:
            total_translated += self._translate_model(
                Topic, 
                ['name', 'description'], 
                target_lang, 
                limit,
                'Topics'
            )
        
        # Certificates
        if 'all' in models or 'certificate' in models:
            total_translated += self._translate_model(
                Certificate, 
                ['name', 'description'], 
                target_lang, 
                limit,
                'Certificates'
            )
        
        # Certificate Topics
        if 'all' in models or 'cert_topic' in models:
            total_translated += self._translate_model(
                CertificateTopic, 
                ['name', 'description'], 
                target_lang, 
                limit,
                'Certificate Topics'
            )
        
        # Certificate Tests
        if 'all' in models or 'cert_test' in models:
            total_translated += self._translate_model(
                CertificateTest, 
                ['title', 'description'], 
                target_lang, 
                limit,
                'Certificate Tests'
            )
        
        # Mock Exam Categories
        if 'all' in models or 'mock_category' in models:
            total_translated += self._translate_model(
                MockExamCategory, 
                ['name', 'description'], 
                target_lang, 
                limit,
                'Mock Exam Categories'
            )
        
        # Mock Exams
        if 'all' in models or 'mock_exam' in models:
            total_translated += self._translate_model(
                MockExam, 
                ['title', 'description'], 
                target_lang, 
                limit,
                'Mock Exams'
            )
        
        # Institution Categories
        if 'all' in models or 'institution_category' in models:
            total_translated += self._translate_model(
                InstitutionCategory, 
                ['name', 'description'], 
                target_lang, 
                limit,
                'Institution Categories'
            )
        
        # Institutions
        if 'all' in models or 'institution' in models:
            total_translated += self._translate_model(
                Institution, 
                ['name', 'short_description', 'description'], 
                target_lang, 
                limit,
                'Institutions'
            )
        
        # Institution Directions
        if 'all' in models or 'direction' in models:
            total_translated += self._translate_model(
                InstitutionDirection, 
                ['name', 'description'], 
                target_lang, 
                limit,
                'Institution Directions'
            )
        
        # News Categories
        if 'all' in models or 'news_category' in models:
            total_translated += self._translate_model(
                NewsCategory, 
                ['name', 'description'], 
                target_lang, 
                limit,
                'News Categories'
            )
        
        # News
        if 'all' in models or 'news' in models:
            total_translated += self._translate_model(
                News, 
                ['title', 'summary'], 
                target_lang, 
                limit,
                'News'
            )
        
        # Course Categories
        if 'all' in models or 'course_category' in models:
            total_translated += self._translate_model(
                CourseCategory, 
                ['name', 'description'], 
                target_lang, 
                limit,
                'Course Categories'
            )
        
        # Courses
        if 'all' in models or 'course' in models:
            total_translated += self._translate_model(
                Course, 
                ['title', 'description', 'instructor'], 
                target_lang, 
                limit,
                'Courses'
            )
        
        # Lessons
        if 'all' in models or 'lesson' in models:
            total_translated += self._translate_model(
                Lesson, 
                ['title', 'description'], 
                target_lang, 
                limit,
                'Lessons'
            )
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Translation cache population completed!'))
        self.stdout.write(self.style.SUCCESS(f'Total texts translated: {total_translated}'))
    
    def _translate_model(self, model, fields, target_lang, limit, model_name):
        """Translate fields for a specific model"""
        self.stdout.write(self.style.WARNING(f'\n📝 Translating {model_name}...'))
        
        queryset = model.objects.filter(is_active=True) if hasattr(model, 'is_active') else model.objects.all()
        
        if limit:
            queryset = queryset[:limit]
        
        count = queryset.count()
        self.stdout.write(f'Found {count} items')
        
        translated_count = 0
        
        for i, obj in enumerate(queryset, 1):
            for field in fields:
                text = getattr(obj, field, None)
                if text and text.strip():
                    try:
                        # Translate and cache
                        translated = translator.translate(
                            text=text,
                            source_lang='uz',
                            target_lang=target_lang,
                            page_name='default'
                        )
                        
                        if translated != text:
                            translated_count += 1
                            self.stdout.write(
                                self.style.SUCCESS(f'  [{i}/{count}] ✓ {field}: {text[:50]}...')
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f'  [{i}/{count}] ⚠ {field}: Already cached or failed')
                            )
                        
                        # Small delay to avoid rate limiting
                        time.sleep(0.1)
                        
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'  [{i}/{count}] ✗ Error translating {field}: {str(e)}')
                        )
        
        self.stdout.write(self.style.SUCCESS(f'✅ {model_name}: {translated_count} texts translated'))
        return translated_count
