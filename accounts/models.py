from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import uuid

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    total_points = models.PositiveIntegerField(default=0, verbose_name="Umumiy ball")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
    def get_progress_percentage(self):
        from core.models import TestResult
        total_tests = TestResult.objects.filter(user=self).count()
        if total_tests == 0:
            return 0
        passed_tests = TestResult.objects.filter(user=self, passed=True).count()
        return int((passed_tests / total_tests) * 100)
    
    def get_total_tests_taken(self):
        from core.models import TestResult
        return TestResult.objects.filter(user=self).count()
    
    def get_passed_tests(self):
        from core.models import TestResult
        return TestResult.objects.filter(user=self, passed=True).count()
    
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
