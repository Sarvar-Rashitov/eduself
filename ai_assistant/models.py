from django.db import models
from django.conf import settings
from django.utils import timezone


class ChatSession(models.Model):
    """AI Hamroh chat sessiyalari"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=200, verbose_name="Suhbat nomi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Chat sessiyasi"
        verbose_name_plural = "Chat sessiyalari"
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def get_messages_count(self):
        return self.messages.count()


class MessageType(models.TextChoices):
    USER = 'user', 'Foydalanuvchi'
    ASSISTANT = 'assistant', 'AI Hamroh'
    SYSTEM = 'system', 'Tizim'


class ChatMessage(models.Model):
    """Chat xabarlari"""
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MessageType.choices, default=MessageType.USER)
    content = models.TextField(verbose_name="Xabar matni")
    attachment = models.FileField(upload_to='chat_attachments/', blank=True, null=True, verbose_name="Fayl")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # AI javob uchun qo'shimcha ma'lumotlar
    tokens_used = models.PositiveIntegerField(default=0, verbose_name="Ishlatilgan tokenlar")
    response_time = models.FloatField(default=0.0, verbose_name="Javob vaqti (soniya)")
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Chat xabari"
        verbose_name_plural = "Chat xabarlari"
    
    def __str__(self):
        return f"{self.get_message_type_display()}: {self.content[:50]}"
    
    @property
    def is_image(self):
        """Fayl rasm ekanligini tekshirish"""
        if self.attachment:
            return self.attachment.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
        return False
    
    @property
    def file_name(self):
        """Fayl nomini olish"""
        if self.attachment:
            return self.attachment.name.split('/')[-1]
        return None


class AIPromptTemplate(models.Model):
    """AI uchun tayyor shablonlar"""
    name = models.CharField(max_length=100, verbose_name="Shablon nomi")
    category = models.CharField(max_length=50, choices=[
        ('subject_help', 'Fan bo\'yicha yordam'),
        ('institution_advice', 'Muassasa tanlash'),
        ('certificate_guide', 'Sertifikat yo\'riqnomasi'),
        ('general', 'Umumiy'),
    ], verbose_name="Kategoriya")
    prompt_text = models.TextField(verbose_name="Prompt matni")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "AI Prompt shabloni"
        verbose_name_plural = "AI Prompt shablonlari"
    
    def __str__(self):
        return self.name


class AIUsageStatistics(models.Model):
    """AI ishlatish statistikasi"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_usage')
    date = models.DateField(default=timezone.now)
    messages_sent = models.PositiveIntegerField(default=0)
    tokens_used = models.PositiveIntegerField(default=0)
    sessions_created = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
        verbose_name = "AI ishlatish statistikasi"
        verbose_name_plural = "AI ishlatish statistikalari"
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"


class SubjectKnowledgeBase(models.Model):
    """Fanlar bo'yicha bilimlar bazasi"""
    subject = models.ForeignKey('core.Subject', on_delete=models.CASCADE, related_name='knowledge_base')
    topic_name = models.CharField(max_length=200, verbose_name="Mavzu nomi")
    content = models.TextField(verbose_name="Mazmun")
    keywords = models.TextField(blank=True, verbose_name="Kalit so'zlar (vergul bilan ajratilgan)")
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Boshlang\'ich'),
        ('intermediate', 'O\'rta'),
        ('advanced', 'Yuqori'),
    ], default='beginner')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['subject', 'topic_name']
        verbose_name = "Fan bilimlar bazasi"
        verbose_name_plural = "Fan bilimlar bazasi"
    
    def __str__(self):
        return f"{self.subject.name} - {self.topic_name}"


class InstitutionRecommendation(models.Model):
    """Muassasa tavsiya qoidalari"""
    name = models.CharField(max_length=200, verbose_name="Qoida nomi")
    criteria = models.JSONField(verbose_name="Tanlov mezonlari")
    recommended_institutions = models.ManyToManyField('core.Institution', verbose_name="Tavsiya etiladigan muassasalar")
    description = models.TextField(verbose_name="Tavsif")
    priority = models.PositiveIntegerField(default=1, verbose_name="Ustuvorlik")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-priority', 'name']
        verbose_name = "Muassasa tavsiyasi"
        verbose_name_plural = "Muassasa tavsiylari"
    
    def __str__(self):
        return self.name