from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import uuid


class Level(models.Model):
    """Dinamik level tizimi"""
    name = models.CharField(max_length=100, verbose_name="Level nomi")
    level_number = models.PositiveIntegerField(unique=True, verbose_name="Level raqami")
    required_xp = models.PositiveIntegerField(verbose_name="Kerakli XP")
    icon = models.ImageField(upload_to='levels/', blank=True, null=True, verbose_name="Level ikonkasi")
    color = models.CharField(max_length=7, default='#6366f1', verbose_name="Rang (hex)")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['level_number']
        verbose_name = "Level"
        verbose_name_plural = "Levellar"
    
    def __str__(self):
        return f"{self.name} (Level {self.level_number}) - {self.required_xp} XP"


class Badge(models.Model):
    """Dinamik badge tizimi"""
    BADGE_TYPE_CHOICES = [
        ('level', 'Level Badge'),
        ('streak', 'Streak Badge'),
        ('achievement', 'Achievement Badge'),
        ('special', 'Special Badge'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Badge nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPE_CHOICES, default='achievement', verbose_name="Badge turi")
    image = models.ImageField(upload_to='badges/', blank=True, null=True, verbose_name="Badge rasmi")
    
    # Level badge uchun
    required_level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True, related_name='badges', verbose_name="Kerakli level")
    
    # Streak badge uchun
    required_streak_days = models.PositiveIntegerField(null=True, blank=True, verbose_name="Kerakli streak kunlari")
    
    # Achievement badge uchun
    required_xp = models.PositiveIntegerField(null=True, blank=True, verbose_name="Kerakli XP")
    required_tests_passed = models.PositiveIntegerField(null=True, blank=True, verbose_name="Kerakli o'tgan testlar")
    
    # Umumiy
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Badge"
        verbose_name_plural = "Badge'lar"
    
    def __str__(self):
        return f"{self.name} ({self.get_badge_type_display()})"
    
    def is_unlocked_for_user(self, user):
        """Foydalanuvchi uchun badge ochilganmi?"""
        if self.badge_type == 'level' and self.required_level:
            return user.total_points >= self.required_level.required_xp
        elif self.badge_type == 'streak' and self.required_streak_days:
            return user.streak_days >= self.required_streak_days
        elif self.badge_type == 'achievement':
            if self.required_xp and user.total_points < self.required_xp:
                return False
            if self.required_tests_passed and user.get_passed_tests() < self.required_tests_passed:
                return False
            return True
        return False


class UserBadge(models.Model):
    """Foydalanuvchi badge'lari"""
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True, verbose_name="Ochilgan vaqt")
    
    class Meta:
        unique_together = ['user', 'badge']
        ordering = ['-unlocked_at']
        verbose_name = "Foydalanuvchi Badge'i"
        verbose_name_plural = "Foydalanuvchi Badge'lari"
    
    def __str__(self):
        return f"{self.user.get_display_name()} - {self.badge.name}"


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
    avatar_number = models.PositiveIntegerField(default=0, verbose_name="Avatar raqami")  # 1-18 oralig'ida
    bio = models.TextField(blank=True, verbose_name="Bio")
    total_points = models.PositiveIntegerField(default=0, verbose_name="Umumiy XP")
    
    # Gamification fields
    streak_days = models.PositiveIntegerField(default=0, verbose_name="Kunlik streak")
    last_active_date = models.DateField(null=True, blank=True, verbose_name="Oxirgi faol kun")
    level = models.PositiveIntegerField(default=1, verbose_name="Level")
    
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
    
    # Language preference
    language = models.CharField(
        max_length=10, 
        choices=[
            ('uz', 'O\'zbekcha'),
            ('en', 'English'),
            ('ru', 'Русский'),
            ('kk', 'Қазақша'),
            ('kaa', 'Qaraqalpaqsha'),
            ('tg', 'Тоҷикӣ'),
            ('ky', 'Кыргызча'),
        ],
        default='uz',
        verbose_name="Til"
    )
    
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
        
        # Agar avatar_number 0 bo'lsa, tasodifiy raqam berish
        if self.avatar_number == 0:
            import random
            self.avatar_number = random.randint(1, 18)
        
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
    
    def get_avatar_url(self):
        """
        Profil rasmini qaytaradi. Agar foydalanuvchi rasm yuklamagan bo'lsa,
        lokal avatar rasmlaridan birini qaytaradi.
        """
        if self.profile_image:
            return self.profile_image.url
        
        # Lokal avatar rasmlaridan foydalanish
        avatar_num = self.avatar_number if 1 <= self.avatar_number <= 18 else 1
        
        # Static URL dan foydalanish
        from django.templatetags.static import static
        return static(f'images/avatars/avatar-{avatar_num}.png')
    
    def get_current_level(self):
        """Foydalanuvchining hozirgi levelini qaytaradi"""
        levels = Level.objects.filter(is_active=True, required_xp__lte=self.total_points).order_by('-required_xp')
        if levels.exists():
            return levels.first()
        return None
    
    def get_next_level(self):
        """Keyingi levelni qaytaradi"""
        levels = Level.objects.filter(is_active=True, required_xp__gt=self.total_points).order_by('required_xp')
        if levels.exists():
            return levels.first()
        return None
    
    def update_level(self):
        """Foydalanuvchi levelini yangilaydi"""
        current_level = self.get_current_level()
        if current_level:
            self.level = current_level.level_number
        else:
            self.level = 0
        self.save(update_fields=['level'])
    
    def check_and_unlock_badges(self):
        """Yangi badge'larni tekshiradi va ochadi"""
        all_badges = Badge.objects.filter(is_active=True)
        
        # Foydalanuvchining mavjud badge'lari
        user_badge_ids = self.user_badges.values_list('badge_id', flat=True)
        
        newly_unlocked = []
        for badge in all_badges:
            if badge.id not in user_badge_ids and badge.is_unlocked_for_user(self):
                UserBadge.objects.create(user=self, badge=badge)
                newly_unlocked.append(badge)
        
        return newly_unlocked
    
    def add_xp(self, points):
        """XP qo'shish va avtomatik badge ochish"""
        self.total_points += points
        self.save(update_fields=['total_points'])
        
        # Level va badge'larni yangilash
        self.update_level()
        newly_unlocked = self.check_and_unlock_badges()
        
        return newly_unlocked


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
