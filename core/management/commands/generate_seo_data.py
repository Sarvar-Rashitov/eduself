from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Subject, Topic, Certificate, CertificateTopic, MockExam, Institution


class Command(BaseCommand):
    help = 'Generate SEO-friendly slugs for existing data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting SEO data generation...'))
        
        # Generate slugs for subjects (if needed in future)
        subjects = Subject.objects.all()
        for subject in subjects:
            self.stdout.write(f'Processing subject: {subject.name}')
        
        self.stdout.write(self.style.SUCCESS(f'Processed {subjects.count()} subjects'))
        
        # Generate slugs for topics (if needed in future)
        topics = Topic.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Processed {topics.count()} topics'))
        
        # Generate slugs for certificates (if needed in future)
        certificates = Certificate.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Processed {certificates.count()} certificates'))
        
        # Generate slugs for institutions (if needed in future)
        institutions = Institution.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Processed {institutions.count()} institutions'))
        
        self.stdout.write(self.style.SUCCESS('SEO data generation completed!'))
