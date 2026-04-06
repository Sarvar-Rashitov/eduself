from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import uuid


class SubscriptionPlan(models.Model):
    """Premium ta'riflar"""
    name = models.CharField(max_length=100, verbose_name="Ta'rif nomi")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    
    # Narx va muddat
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narx (so'm)")
    duration_days = models.PositiveIntegerField(verbose_name="Muddat (kunlar)")
    
    # Cheklovlar
    unlimited_lives = models.BooleanField(default=False, verbose_name="Cheksiz yurakchalar")
    ai_analysis_limit = models.IntegerField(default=-1, verbose_name="AI tahlil limiti (-1 = cheksiz)")
    ai_companion_limit = models.IntegerField(default=-1, verbose_name="AI hamroh limiti (-1 = cheksiz)")
    university_exam_limit = models.IntegerField(default=-1, verbose_name="Universitet imtihoni limiti (-1 = cheksiz)")
    mock_exam_limit = models.IntegerField(default=-1, verbose_name="Mock exam limiti (-1 = cheksiz)")
    certificate_test_limit = models.IntegerField(default=-1, verbose_name="Sertifikat test limiti (-1 = cheksiz)")
    
    # Ko'rinish
    icon = models.CharField(max_length=50, default='bi-star', verbose_name="Icon")
    color = models.CharField(max_length=20, default='#6366f1', verbose_name="Rang")
    badge_text = models.CharField(max_length=50, blank=True, verbose_name="Badge matni")
    is_popular = models.BooleanField(default=False, verbose_name="Mashhur")
    
    # Holat
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'price']
        verbose_name = "Ta'rif"
        verbose_name_plural = "Ta'riflar"
    
    def __str__(self):
        return f"{self.name} - {self.price} so'm / {self.duration_days} kun"


class UserSubscription(models.Model):
    """Foydalanuvchi obunalari"""
    STATUS_CHOICES = [
        ('active', 'Faol'),
        ('expired', 'Muddati tugagan'),
        ('cancelled', 'Bekor qilingan'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, verbose_name="Ta'rif")
    
    # Muddat
    start_date = models.DateTimeField(default=timezone.now, verbose_name="Boshlanish sanasi")
    end_date = models.DateTimeField(verbose_name="Tugash sanasi")
    
    # Holat
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Holat")
    is_trial = models.BooleanField(default=False, verbose_name="Sinov muddati")
    
    # Qanday olingan
    acquired_via = models.CharField(max_length=50, default='payment', verbose_name="Qanday olingan")  # payment, referral, promo, admin
    
    # Foydalanish statistikasi
    ai_analysis_used = models.IntegerField(default=0, verbose_name="AI tahlil ishlatilgan")
    ai_companion_used = models.IntegerField(default=0, verbose_name="AI hamroh ishlatilgan")
    university_exam_used = models.IntegerField(default=0, verbose_name="Universitet imtihoni ishlatilgan")
    mock_exam_used = models.IntegerField(default=0, verbose_name="Mock exam ishlatilgan")
    certificate_test_used = models.IntegerField(default=0, verbose_name="Sertifikat test ishlatilgan")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Foydalanuvchi obunasi"
        verbose_name_plural = "Foydalanuvchi obunalari"
    
    def __str__(self):
        return f"{self.user.get_display_name()} - {self.plan.name} ({self.status})"
    
    def save(self, *args, **kwargs):
        # Agar end_date bo'lmasa, avtomatik hisoblash
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)
    
    def is_active(self):
        """Obuna faolmi?"""
        if self.status != 'active':
            return False
        return timezone.now() < self.end_date
    
    def check_and_update_status(self):
        """Obuna holatini tekshirish va yangilash"""
        if self.status == 'active' and timezone.now() >= self.end_date:
            self.status = 'expired'
            self.save(update_fields=['status'])
    
    def can_use_feature(self, feature_name):
        """Xususiyatdan foydalanish mumkinmi?"""
        if not self.is_active():
            return False
        
        feature_map = {
            'ai_analysis': ('ai_analysis_limit', 'ai_analysis_used'),
            'ai_companion': ('ai_companion_limit', 'ai_companion_used'),
            'university_exam': ('university_exam_limit', 'university_exam_used'),
            'mock_exam': ('mock_exam_limit', 'mock_exam_used'),
            'certificate_test': ('certificate_test_limit', 'certificate_test_used'),
        }
        
        if feature_name not in feature_map:
            return False
        
        limit_field, used_field = feature_map[feature_name]
        limit = getattr(self.plan, limit_field)
        used = getattr(self, used_field)
        
        # -1 = cheksiz
        if limit == -1:
            return True
        
        return used < limit
    
    def use_feature(self, feature_name):
        """Xususiyatdan foydalanish"""
        if not self.can_use_feature(feature_name):
            return False
        
        feature_map = {
            'ai_analysis': 'ai_analysis_used',
            'ai_companion': 'ai_companion_used',
            'university_exam': 'university_exam_used',
            'mock_exam': 'mock_exam_used',
            'certificate_test': 'certificate_test_used',
        }
        
        if feature_name in feature_map:
            used_field = feature_map[feature_name]
            setattr(self, used_field, getattr(self, used_field) + 1)
            self.save(update_fields=[used_field])
            return True
        
        return False


class PromoCode(models.Model):
    """Promokodlar"""
    code = models.CharField(max_length=50, unique=True, verbose_name="Promokod")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, verbose_name="Ta'rif")
    
    # Chegirma
    discount_percent = models.PositiveIntegerField(default=0, verbose_name="Chegirma (%)")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Chegirma (so'm)")
    
    # Muddat
    valid_from = models.DateTimeField(default=timezone.now, verbose_name="Amal qilish boshlanishi")
    valid_until = models.DateTimeField(verbose_name="Amal qilish tugashi")
    
    # Cheklovlar
    max_uses = models.PositiveIntegerField(default=0, verbose_name="Maksimal foydalanish (0 = cheksiz)")
    current_uses = models.PositiveIntegerField(default=0, verbose_name="Hozirgi foydalanish")
    
    # Holat
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Promokod"
        verbose_name_plural = "Promokodlar"
    
    def __str__(self):
        return f"{self.code} - {self.plan.name}"
    
    def is_valid(self):
        """Promokod amal qiladimi?"""
        if not self.is_active:
            return False
        
        now = timezone.now()
        if now < self.valid_from or now > self.valid_until:
            return False
        
        if self.max_uses > 0 and self.current_uses >= self.max_uses:
            return False
        
        return True
    
    def get_discounted_price(self):
        """Chegirmali narxni hisoblash - Python 3.13 uchun Decimal konversiyasi"""
        original_price = self.plan.price
        
        if self.discount_percent > 0:
            # Decimal va float aralashmasligini ta'minlash
            discount = original_price * (Decimal(str(self.discount_percent)) / Decimal('100'))
            return original_price - discount
        
        if self.discount_amount > 0:
            return max(Decimal('0'), original_price - self.discount_amount)
        
        return original_price
    
    def use(self):
        """Promokodni ishlatish"""
        if not self.is_valid():
            return False
        
        self.current_uses += 1
        self.save(update_fields=['current_uses'])
        return True


class ReferralProgram(models.Model):
    """Referal dasturi"""
    name = models.CharField(max_length=100, verbose_name="Dastur nomi")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, verbose_name="Ta'rif")
    
    # Shartlar
    required_referrals = models.PositiveIntegerField(verbose_name="Kerakli taklif soni")
    referral_deadline_days = models.PositiveIntegerField(verbose_name="Taklif muddati (kunlar)")
    
    # Mukofot
    reward_duration_days = models.PositiveIntegerField(verbose_name="Mukofot muddati (kunlar)")
    
    # Holat
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Referal dasturi"
        verbose_name_plural = "Referal dasturlari"
    
    def __str__(self):
        return f"{self.name} - {self.plan.name}"


class UserReferral(models.Model):
    """Foydalanuvchi referallari"""
    referrer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referrals_made', verbose_name="Taklif qiluvchi")
    referred = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referred_by', verbose_name="Taklif qilingan")
    program = models.ForeignKey(ReferralProgram, on_delete=models.CASCADE, verbose_name="Dastur")
    
    # Holat
    is_completed = models.BooleanField(default=False, verbose_name="Bajarilgan")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Bajarilgan vaqt")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Foydalanuvchi referali"
        verbose_name_plural = "Foydalanuvchi referallari"
    
    def __str__(self):
        return f"{self.referrer.get_display_name()} -> {self.referred.get_display_name()}"


class ReferralProgress(models.Model):
    """Referal dasturi jarayoni"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referral_progress')
    program = models.ForeignKey(ReferralProgram, on_delete=models.CASCADE, verbose_name="Dastur")
    
    # Jarayon
    referral_count = models.PositiveIntegerField(default=0, verbose_name="Taklif soni")
    started_at = models.DateTimeField(default=timezone.now, verbose_name="Boshlangan vaqt")
    deadline = models.DateTimeField(verbose_name="Muddat")
    
    # Holat
    is_completed = models.BooleanField(default=False, verbose_name="Bajarilgan")
    reward_given = models.BooleanField(default=False, verbose_name="Mukofot berilgan")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Referal jarayoni"
        verbose_name_plural = "Referal jarayonlari"
    
    def __str__(self):
        return f"{self.user.get_display_name()} - {self.program.name}"
    
    def save(self, *args, **kwargs):
        if not self.deadline:
            self.deadline = self.started_at + timedelta(days=self.program.referral_deadline_days)
        super().save(*args, **kwargs)
    
    def check_completion(self):
        """Bajarilganligini tekshirish"""
        if self.is_completed:
            return True
        
        if self.referral_count >= self.program.required_referrals:
            self.is_completed = True
            self.save(update_fields=['is_completed'])
            return True
        
        return False


class Payment(models.Model):
    """To'lovlar"""
    PAYMENT_METHOD_CHOICES = [
        ('click', 'Click'),
        ('payme', 'Payme'),
        ('admin', 'Admin'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('processing', 'Jarayonda'),
        ('completed', 'Bajarilgan'),
        ('failed', 'Muvaffaqiyatsiz'),
        ('cancelled', 'Bekor qilingan'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(UserSubscription, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, verbose_name="Ta'rif")
    
    # To'lov ma'lumotlari
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="To'lov usuli")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Summa")
    
    # Promokod
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Promokod")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Chegirma summasi")
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Yakuniy summa")
    
    # Holat
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holat")
    
    # To'lov tizimi ma'lumotlari
    transaction_id = models.CharField(max_length=255, blank=True, verbose_name="Tranzaksiya ID")
    payment_data = models.JSONField(default=dict, blank=True, verbose_name="To'lov ma'lumotlari")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Bajarilgan vaqt")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "To'lov"
        verbose_name_plural = "To'lovlar"
    
    def __str__(self):
        return f"{self.user.get_display_name()} - {self.plan.name} - {self.final_amount} so'm"


class Donation(models.Model):
    """Donatlar"""
    PAYMENT_METHOD_CHOICES = [
        ('click', 'Click'),
        ('payme', 'Payme'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('completed', 'Bajarilgan'),
        ('failed', 'Muvaffaqiyatsiz'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donations')
    
    # Donat ma'lumotlari
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Summa")
    message = models.TextField(blank=True, verbose_name="Xabar")
    
    # To'lov
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="To'lov usuli")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holat")
    
    # To'lov tizimi ma'lumotlari
    transaction_id = models.CharField(max_length=255, blank=True, verbose_name="Tranzaksiya ID")
    payment_data = models.JSONField(default=dict, blank=True, verbose_name="To'lov ma'lumotlari")
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Bajarilgan vaqt")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Donat"
        verbose_name_plural = "Donatlar"
    
    def __str__(self):
        return f"{self.user.get_display_name()} - {self.amount} so'm"
