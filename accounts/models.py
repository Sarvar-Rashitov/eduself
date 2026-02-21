from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import uuid

class User(AbstractUser):
    # Username ni optional qilamiz - faqat backend uchun
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    
    # Email va telefon - unique identifiers
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Telefon raqam")
    
    # Majburiy maydonlar
    first_name = models.CharField(max_length=150, verbose_name="Ism")
    last_name = models.CharField(max_length=150, verbose_name="Familiya")
    
    # Qo'shimcha maydonlar
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name="Profil rasmi")
    bio = models.TextField(blank=True, verbose_name="Bio")
    total_points = models.PositiveIntegerField(default=0, verbose_name="Umumiy ball")
    
    # Email verification
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    
    # Phone verification
    phone_verified = models.BooleanField(default=False)
    
    # Social auth
    google_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    telegram_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    telegram_username = models.CharField(max_length=255, blank=True, null=True, verbose_name="Telegram username")
    telegram_chat_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="Telegram Chat ID")
    auth_provider = models.CharField(max_length=50, default='email')  # email, phone, google, telegram
    
    # Certificate file
    certificate_file = models.FileField(upload_to='user_certificates/', blank=True, null=True, verbose_name="Sertifikat fayli")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Email yoki telefon bilan login qilish uchun
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def save(self, *args, **kwargs):
        # Agar username bo'lmasa, email yoki telefon dan yaratamiz
        if not self.username:
            if self.email:
                base_username = self.email.split('@')[0]
            elif self.phone:
                base_username = f"user_{self.phone[-6:]}"
            elif self.telegram_id:
                base_username = f"tg_{self.telegram_id}"
            else:
                base_username = f"user_{uuid.uuid4().hex[:8]}"
            
            # Unique username yaratish
            username = base_username
            counter = 1
            # Exclude current instance from uniqueness check
            qs = User.objects.filter(username=username)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            while qs.exists():
                username = f"{base_username}{counter}"
                counter += 1
                qs = User.objects.filter(username=username)
                if self.pk:
                    qs = qs.exclude(pk=self.pk)
            self.username = username
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username or self.email or self.phone or str(self.id)
    
    def get_display_name(self):
        """Foydalanuvchi nomini ko'rsatish"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        return self.username or self.email or self.phone
    
    def get_progress_percentage(self):
        from core.models import TopicResult, CertificateResult, MockExamResult
        total_tests = TopicResult.objects.filter(user=self).count()
        total_tests += CertificateResult.objects.filter(user=self).count()
        total_tests += MockExamResult.objects.filter(user=self).count()
        if total_tests == 0:
            return 0
        passed_tests = TopicResult.objects.filter(user=self, passed=True).count()
        passed_tests += CertificateResult.objects.filter(user=self, passed=True).count()
        passed_tests += MockExamResult.objects.filter(user=self, passed=True).count()
        return int((passed_tests / total_tests) * 100)
    
    def get_total_tests_taken(self):
        from core.models import TopicResult, CertificateResult, MockExamResult
        total = TopicResult.objects.filter(user=self).count()
        total += CertificateResult.objects.filter(user=self).count()
        total += MockExamResult.objects.filter(user=self).count()
        return total
    
    def get_passed_tests(self):
        from core.models import TopicResult, CertificateResult, MockExamResult
        passed = TopicResult.objects.filter(user=self, passed=True).count()
        passed += CertificateResult.objects.filter(user=self, passed=True).count()
        passed += MockExamResult.objects.filter(user=self, passed=True).count()
        return passed
    
    def get_total_points(self):
        """
        Get the total points earned by the user across all test types.
        This method returns the current value of total_points field.
        """
        return self.total_points


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)
    
    def is_valid(self):
        if self.used:
            return False
        if not self.expires_at:
            return False
        if timezone.now() > self.expires_at:
            return False
        return True
    
    def __str__(self):
        return f"Reset token for {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']


class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=48)
        super().save(*args, **kwargs)
    
    def is_valid(self):
        if self.used:
            return False
        if not self.expires_at:
            return False
        if timezone.now() > self.expires_at:
            return False
        return True
    
    def __str__(self):
        return f"Email verification for {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']


class TelegramLoginToken(models.Model):
    """Telegram login uchun vaqtinchalik tokenlar - database'da saqlash"""
    telegram_id = models.CharField(max_length=255, db_index=True)
    token = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)
    
    def is_valid(self):
        """Token hali ham amal qiladimi?"""
        if self.used:
            return False
        if timezone.now() > self.expires_at:
            return False
        return True
    
    def mark_as_used(self):
        """Tokenni ishlatilgan deb belgilash"""
        self.used = True
        self.save()
    
    @classmethod
    def cleanup_expired(cls):
        """Eskirgan tokenlarni tozalash"""
        cls.objects.filter(expires_at__lt=timezone.now()).delete()
    
    def __str__(self):
        return f"Telegram login token for {self.telegram_id}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['telegram_id', 'token']),
            models.Index(fields=['expires_at']),
        ]


class LoginHistory(models.Model):
    """Foydalanuvchi kirish tarixi - yangi qurilmalarni aniqlash uchun"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    ip_address = models.GenericIPAddressField(verbose_name="IP manzil")
    user_agent = models.TextField(verbose_name="User Agent")
    device_type = models.CharField(max_length=50, blank=True, verbose_name="Qurilma turi")  # mobile, desktop, tablet
    browser = models.CharField(max_length=100, blank=True, verbose_name="Brauzer")
    os = models.CharField(max_length=100, blank=True, verbose_name="Operatsion tizim")
    location = models.CharField(max_length=255, blank=True, verbose_name="Joylashuv")
    is_new_device = models.BooleanField(default=False, verbose_name="Yangi qurilma")
    login_time = models.DateTimeField(auto_now_add=True, verbose_name="Kirish vaqti")
    
    def __str__(self):
        return f"{self.user.username} - {self.device_type} - {self.login_time}"
    
    class Meta:
        ordering = ['-login_time']
        verbose_name = "Kirish tarixi"
        verbose_name_plural = "Kirish tarixi"
        indexes = [
            models.Index(fields=['user', '-login_time']),
            models.Index(fields=['ip_address']),
        ]
