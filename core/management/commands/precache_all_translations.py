"""
Management command to pre-cache ALL translations for ALL pages
This will translate and cache all content in advance to avoid delays
"""
from django.core.management.base import BaseCommand
from django.db.models import Q
from core.models import (
    Subject, Topic, Question, Answer,
    Certificate, CertificateTopic, CertificateTest, CertificateQuestion, CertificateAnswer,
    MockExam, MockExamQuestion, MockExamAnswer,
    Institution, InstitutionDirection,
    News, Course, Lesson,
    TranslationCache
)
from core.translation import translator
import time


class Command(BaseCommand):
    help = 'Pre-cache all translations for all pages and all languages'
    
    LANGUAGES = ['en', 'ru', 'kk', 'kaa', 'tg', 'ky']  # All target languages
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--languages',
            nargs='+',
            default=self.LANGUAGES,
            help='Languages to translate to (default: all)'
        )
        parser.add_argument(
            '--pages',
            nargs='+',
            choices=['subjects', 'certificates', 'mock_exams', 'institutions', 'news', 'courses', 'all'],
            default=['all'],
            help='Which pages to cache (default: all)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limit number of items per model (for testing)'
        )
    
    def handle(self, *args, **options):
        languages = options['languages']
        pages = options['pages']
        limit = options['limit']
        
        if 'all' in pages:
            pages = ['subjects', 'certificates', 'mock_exams', 'institutions', 'news', 'courses']
        
        self.stdout.write(self.style.SUCCESS(f'\n🚀 Starting pre-cache for languages: {", ".join(languages)}'))
        self.stdout.write(self.style.SUCCESS(f'📄 Pages: {", ".join(pages)}\n'))
        
        total_cached = 0
        start_time = time.time()
        
        # 1. SUBJECTS & TOPICS & QUESTIONS
        if 'subjects' in pages:
            total_cached += self.cache_subjects(languages, limit)
        
        # 2. CERTIFICATES
        if 'certificates' in pages:
            total_cached += self.cache_certificates(languages, limit)
        
        # 3. MOCK EXAMS
        if 'mock_exams' in pages:
            total_cached += self.cache_mock_exams(languages, limit)
        
        # 4. INSTITUTIONS
        if 'institutions' in pages:
            total_cached += self.cache_institutions(languages, limit)
        
        # 5. NEWS
        if 'news' in pages:
            total_cached += self.cache_news(languages, limit)
        
        # 6. COURSES
        if 'courses' in pages:
            total_cached += self.cache_courses(languages, limit)
        
        elapsed_time = time.time() - start_time
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Pre-caching completed!'))
        self.stdout.write(self.style.SUCCESS(f'📊 Total translations cached: {total_cached}'))
        self.stdout.write(self.style.SUCCESS(f'⏱️  Time taken: {elapsed_time:.2f} seconds'))
        self.stdout.write(self.style.SUCCESS(f'💾 Database cache entries: {TranslationCache.objects.count()}'))
    
    def cache_subjects(self, languages, limit):
        """Cache all subjects, topics, questions and answers"""
        self.stdout.write(self.style.WARNING('\n📚 Caching SUBJECTS...'))
        cached = 0
        
        subjects = Subject.objects.filter(is_active=True)
        if limit:
            subjects = subjects[:limit]
        
        for subject in subjects:
            self.stdout.write(f'  Subject: {subject.name}')
            
            # Cache subject name and description
            for lang in languages:
                translator.translate(subject.name, 'uz', lang, 'subjects')
                if subject.description:
                    translator.translate(subject.description, 'uz', lang, 'subjects')
                cached += 2
            
            # Cache topics
            topics = subject.topics.filter(is_active=True)
            if limit:
                topics = topics[:limit]
            
            for topic in topics:
                self.stdout.write(f'    Topic: {topic.name}')
                
                for lang in languages:
                    translator.translate(topic.name, 'uz', lang, 'topic_test')
                    if topic.description:
                        translator.translate(topic.description, 'uz', lang, 'topic_test')
                    cached += 2
                
                # Cache questions and answers
                questions = topic.questions.all()
                if limit:
                    questions = questions[:limit]
                
                for question in questions:
                    for lang in languages:
                        translator.translate(question.text, 'uz', lang, 'topic_test')
                        cached += 1
                        
                        # Cache answers
                        for answer in question.answers.all():
                            translator.translate(answer.text, 'uz', lang, 'topic_test')
                            cached += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ Subjects cached: {cached} translations'))
        return cached
    
    def cache_certificates(self, languages, limit):
        """Cache all certificates, topics, tests, questions and answers"""
        self.stdout.write(self.style.WARNING('\n🎓 Caching CERTIFICATES...'))
        cached = 0
        
        certificates = Certificate.objects.filter(is_active=True)
        if limit:
            certificates = certificates[:limit]
        
        for cert in certificates:
            self.stdout.write(f'  Certificate: {cert.name}')
            
            for lang in languages:
                translator.translate(cert.name, 'uz', lang, 'certificates')
                if cert.description:
                    translator.translate(cert.description, 'uz', lang, 'certificates')
                cached += 2
            
            # Cache topics
            topics = cert.cert_topics.filter(is_active=True)
            if limit:
                topics = topics[:limit]
            
            for topic in topics:
                for lang in languages:
                    translator.translate(topic.name, 'uz', lang, 'cert_test')
                    if topic.description:
                        translator.translate(topic.description, 'uz', lang, 'cert_test')
                    cached += 2
                
                # Cache tests
                tests = topic.cert_tests.filter(is_active=True)
                if limit:
                    tests = tests[:limit]
                
                for test in tests:
                    for lang in languages:
                        translator.translate(test.title, 'uz', lang, 'cert_test')
                        if test.description:
                            translator.translate(test.description, 'uz', lang, 'cert_test')
                        cached += 2
                    
                    # Cache questions
                    questions = test.cert_questions.all()
                    if limit:
                        questions = questions[:limit]
                    
                    for question in questions:
                        for lang in languages:
                            translator.translate(question.text, 'uz', lang, 'cert_test')
                            cached += 1
                            
                            for answer in question.cert_answers.all():
                                translator.translate(answer.text, 'uz', lang, 'cert_test')
                                cached += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ Certificates cached: {cached} translations'))
        return cached
    
    def cache_mock_exams(self, languages, limit):
        """Cache all mock exams, questions and answers"""
        self.stdout.write(self.style.WARNING('\n📝 Caching MOCK EXAMS...'))
        cached = 0
        
        exams = MockExam.objects.filter(is_active=True)
        if limit:
            exams = exams[:limit]
        
        for exam in exams:
            self.stdout.write(f'  Mock Exam: {exam.title}')
            
            for lang in languages:
                translator.translate(exam.title, 'uz', lang, 'mock_exam')
                if exam.description:
                    translator.translate(exam.description, 'uz', lang, 'mock_exam')
                cached += 2
            
            # Cache questions
            questions = exam.mock_questions.all()
            if limit:
                questions = questions[:limit]
            
            for question in questions:
                for lang in languages:
                    translator.translate(question.text, 'uz', lang, 'mock_exam')
                    cached += 1
                    
                    for answer in question.mock_answers.all():
                        translator.translate(answer.text, 'uz', lang, 'mock_exam')
                        cached += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ Mock exams cached: {cached} translations'))
        return cached
    
    def cache_institutions(self, languages, limit):
        """Cache all institutions and directions"""
        self.stdout.write(self.style.WARNING('\n🏛️  Caching INSTITUTIONS...'))
        cached = 0
        
        institutions = Institution.objects.filter(is_active=True)
        if limit:
            institutions = institutions[:limit]
        
        for inst in institutions:
            self.stdout.write(f'  Institution: {inst.name}')
            
            for lang in languages:
                translator.translate(inst.name, 'uz', lang, 'institutions')
                
                if inst.short_description:
                    translator.translate(inst.short_description, 'uz', lang, 'institutions')
                
                # Split long description into chunks
                if inst.description:
                    desc_length = len(inst.description)
                    if desc_length > 1000:
                        for i in range(0, desc_length, 900):
                            chunk = inst.description[i:i+900]
                            translator.translate(chunk, 'uz', lang, 'institutions')
                            cached += 1
                    else:
                        translator.translate(inst.description, 'uz', lang, 'institutions')
                        cached += 1
                
                cached += 2
            
            # Cache directions
            for direction in inst.directions.filter(is_active=True):
                for lang in languages:
                    translator.translate(direction.name, 'uz', lang, 'institutions')
                    if direction.description:
                        translator.translate(direction.description, 'uz', lang, 'institutions')
                    cached += 2
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ Institutions cached: {cached} translations'))
        return cached
    
    def cache_news(self, languages, limit):
        """Cache all news articles"""
        self.stdout.write(self.style.WARNING('\n📰 Caching NEWS...'))
        cached = 0
        
        news_list = News.objects.filter(is_published=True)
        if limit:
            news_list = news_list[:limit]
        
        for news in news_list:
            self.stdout.write(f'  News: {news.title}')
            
            for lang in languages:
                translator.translate(news.title, 'uz', lang, 'news')
                translator.translate(news.summary, 'uz', lang, 'news')
                
                # Split long content into chunks
                if news.content:
                    content_length = len(news.content)
                    if content_length > 1000:
                        for i in range(0, content_length, 900):
                            chunk = news.content[i:i+900]
                            translator.translate(chunk, 'uz', lang, 'news')
                            cached += 1
                    else:
                        translator.translate(news.content, 'uz', lang, 'news')
                        cached += 1
                
                cached += 2
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ News cached: {cached} translations'))
        return cached
    
    def cache_courses(self, languages, limit):
        """Cache all courses and lessons"""
        self.stdout.write(self.style.WARNING('\n🎯 Caching COURSES...'))
        cached = 0
        
        courses = Course.objects.filter(is_active=True)
        if limit:
            courses = courses[:limit]
        
        for course in courses:
            self.stdout.write(f'  Course: {course.title}')
            
            for lang in languages:
                translator.translate(course.title, 'uz', lang, 'courses')
                if course.description:
                    translator.translate(course.description, 'uz', lang, 'courses')
                cached += 2
            
            # Cache lessons
            lessons = course.lessons.filter(is_active=True)
            if limit:
                lessons = lessons[:limit]
            
            for lesson in lessons:
                for lang in languages:
                    translator.translate(lesson.title, 'uz', lang, 'courses')
                    
                    # Split long content
                    if lesson.content:
                        content_length = len(lesson.content)
                        if content_length > 1000:
                            for i in range(0, content_length, 900):
                                chunk = lesson.content[i:i+900]
                                translator.translate(chunk, 'uz', lang, 'courses')
                                cached += 1
                        else:
                            translator.translate(lesson.content, 'uz', lang, 'courses')
                            cached += 1
                    
                    cached += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ Courses cached: {cached} translations'))
        return cached
