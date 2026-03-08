from django.db import models
from django.conf import settings


class UserInterestPreference(models.Model):
    """Foydalanuvchi qiziqishlari va shaxsiylashtirish"""
    
    ROLE_CHOICES = [
        ('abiturient', 'Abiturient'),
        ('student', 'Talaba'),
        ('teacher', 'O\'qituvchi'),
        ('other', 'Boshqa'),
    ]
    
    SOURCE_CHOICES = [
        ('instagram', 'Instagram'),
        ('telegram', 'Telegram'),
        ('tanishimdan', 'Tanishimdan'),
        ('boshqa', 'Boshqa'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='interest_preference',
        verbose_name="Foydalanuvchi"
    )
    
    # Question 1: Source (Bizni qayerdan topdingiz?)
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        blank=True,
        verbose_name="Manba"
    )
    
    # Question 2: Role
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        blank=True,
        verbose_name="Rol"
    )
    
    # Questions 3-6: Selected categories (stored as JSON)
    selected_categories = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Tanlangan kategoriyalar",
        help_text="Format: {'subjects': [ids], 'certificates': [ids], 'courses': [ids], 'mock_exams': [ids]}"
    )
    
    # Backup of selected categories (when user switches to full platform)
    saved_categories = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Saqlangan kategoriyalar",
        help_text="Avvalgi tanlangan kategoriyalar (to'liq platformaga o'tganda saqlanadi)"
    )
    
    # Onboarding status
    onboarding_completed = models.BooleanField(
        default=False,
        verbose_name="Onboarding tugallangan"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")
    
    class Meta:
        verbose_name = "Foydalanuvchi qiziqishi"
        verbose_name_plural = "Foydalanuvchi qiziqishlari"
    
    def __str__(self):
        return f"{self.user.get_display_name()} - {self.get_role_display()}"
    
    def has_interest_in_subjects(self):
        """Fanlarga qiziqishi bormi?"""
        return bool(self.selected_categories.get('subjects', []))
    
    def has_interest_in_certificates(self):
        """Sertifikatlarga qiziqishi bormi?"""
        return bool(self.selected_categories.get('certificates', []))
    
    def has_interest_in_courses(self):
        """Kurslarga qiziqishi bormi?"""
        return bool(self.selected_categories.get('courses', []))
    
    def has_interest_in_mock_exams(self):
        """Mock imtihonlarga qiziqishi bormi?"""
        return bool(self.selected_categories.get('mock_exams', []))
    
    def get_selected_subject_categories(self):
        """Tanlangan fan kategoriyalarini olish"""
        from core.models import SubjectCategory
        category_ids = self.selected_categories.get('subjects', [])
        if not category_ids:
            return SubjectCategory.objects.none()
        return SubjectCategory.objects.filter(id__in=category_ids, is_active=True)
    
    def get_selected_certificates(self):
        """Tanlangan sertifikatlarni olish"""
        from core.models import Certificate
        cert_ids = self.selected_categories.get('certificates', [])
        if not cert_ids:
            return Certificate.objects.none()
        return Certificate.objects.filter(id__in=cert_ids, is_active=True)
    
    def get_selected_course_categories(self):
        """Tanlangan kurs kategoriyalarini olish"""
        from core.models import CourseCategory
        category_ids = self.selected_categories.get('courses', [])
        if not category_ids:
            return CourseCategory.objects.none()
        return CourseCategory.objects.filter(id__in=category_ids, is_active=True)
    
    def get_selected_mock_exam_categories(self):
        """Tanlangan mock imtihon kategoriyalarini olish"""
        from core.models import MockExamCategory
        category_ids = self.selected_categories.get('mock_exams', [])
        if not category_ids:
            return MockExamCategory.objects.none()
        return MockExamCategory.objects.filter(id__in=category_ids, is_active=True)
