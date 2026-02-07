

from django.db import models
from django.conf import settings
import json

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='EduSelf')
    site_description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    about_text = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Sayt sozlamalari"
        verbose_name_plural = "Sayt sozlamalari"
    
    def __str__(self):
        return self.site_name


class DifficultyLevel(models.Model):
    """Test qiyinlik darajasi"""
    name = models.CharField(max_length=100, verbose_name="Qiyinlik nomi")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    color = models.CharField(max_length=20, default='#6366f1', verbose_name="Rang (HEX)")
    bg_color = models.CharField(max_length=20, default='rgba(99, 102, 241, 0.1)', verbose_name="Fon rangi")
    icon = models.CharField(max_length=50, default='fas fa-signal', verbose_name="Icon")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Qiyinlik darajasi"
        verbose_name_plural = "Qiyinlik darajalari"
    
    def __str__(self):
        return self.name


class SubjectCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name="Kategoriya nomi")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    icon = models.CharField(max_length=50, default='bi-book', verbose_name="Icon")
    image = models.ImageField(upload_to='subject_categories/', blank=True, null=True, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Fan kategoriyasi"
        verbose_name_plural = "Fan kategoriyalari"
    
    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=200, verbose_name="Fan nomi")
    category = models.ForeignKey(SubjectCategory, on_delete=models.CASCADE, related_name='subjects', verbose_name="Kategoriya", null=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Tavsif")
    icon = models.CharField(max_length=50, default='bi-book', verbose_name="Icon")
    image = models.ImageField(upload_to='subjects/', blank=True, null=True, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"
    
    def __str__(self):
        return self.name
    
    def get_topics_count(self):
        return self.topics.count()
    
    def get_questions_count(self):
        return sum(topic.questions.count() for topic in self.topics.all())


class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics', verbose_name="Fan")
    name = models.CharField(max_length=200, verbose_name="Mavzu nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    time_limit = models.PositiveIntegerField(default=30, verbose_name="Vaqt limiti (daqiqa)")
    passing_score = models.PositiveIntegerField(default=60, verbose_name="O'tish balli (%)")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Mavzu"
        verbose_name_plural = "Mavzular"
    
    def __str__(self):
        return f"{self.subject.name} - {self.name}"
    
    def get_questions_count(self):
        return self.questions.count()
    
    def get_max_points(self):
        """Mavzudagi barcha savollar ballarining yig'indisini qaytarish"""
        return self.questions.aggregate(
            total_points=models.Sum('points')
        )['total_points'] or 0


class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='questions', verbose_name="Mavzu", null=True, blank=True)
    long_text = models.TextField(blank=True, null=True, verbose_name="Uzun matn", help_text="Hikoya, she'r yoki uzun matn (ixtiyoriy)")
    text = models.TextField(verbose_name="Savol matni")
    image = models.ImageField(upload_to='questions/', blank=True, null=True, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    points = models.PositiveIntegerField(default=1, verbose_name="Ball")
    
    class Meta:
        ordering = ['order']
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"
    
    def __str__(self):
        return self.text[:50]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name="Savol")
    text = models.CharField(max_length=500, verbose_name="Javob matni")
    image = models.ImageField(upload_to='answers/', blank=True, null=True, verbose_name="Javob rasmi")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javob")
    
    class Meta:
        verbose_name = "Javob"
        verbose_name_plural = "Javoblar"
    
    def __str__(self):
        return self.text[:50]


class TopicResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='topic_results')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='results')
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    time_taken = models.PositiveIntegerField(default=0)
    user_answers = models.JSONField(default=dict, blank=True, verbose_name="Foydalanuvchi javoblari")
    earned_points = models.PositiveIntegerField(default=0, verbose_name="Olingan ball")
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-completed_at']
        verbose_name = "Mavzu natijasi"
        verbose_name_plural = "Mavzu natijalari"
    
    def __str__(self):
        return f"{self.user.username} - {self.topic.name} - {self.score}%"


class Certificate(models.Model):
    name = models.CharField(max_length=200, verbose_name="Sertifikat nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    image = models.ImageField(upload_to='certificates/', blank=True, null=True, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Sertifikat"
        verbose_name_plural = "Sertifikatlar"
    
    def __str__(self):
        return self.name


class CertificateTopic(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, related_name='cert_topics', verbose_name="Sertifikat")
    name = models.CharField(max_length=200, verbose_name="Fan nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Sertifikat fani"
        verbose_name_plural = "Sertifikat fanlari"
    
    def __str__(self):
        return f"{self.certificate.name} - {self.name}"


class CertificateTest(models.Model):
    topic = models.ForeignKey(CertificateTopic, on_delete=models.CASCADE, related_name='cert_tests', verbose_name="Fan")
    title = models.CharField(max_length=200, verbose_name="Test nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    time_limit = models.PositiveIntegerField(default=30, verbose_name="Vaqt limiti (daqiqa)")
    passing_score = models.PositiveIntegerField(default=60, verbose_name="O'tish balli (%)")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    unlock_score = models.PositiveIntegerField(default=60, verbose_name="Ochish uchun kerakli ball (%)")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Sertifikat testi"
        verbose_name_plural = "Sertifikat testlari"
    
    def __str__(self):
        return f"{self.topic.name} - {self.title}"
    
    def get_max_points(self):
        """Testdagi barcha savollar ballarining yig'indisini qaytarish"""
        return self.cert_questions.aggregate(
            total_points=models.Sum('points')
        )['total_points'] or 0
    
    def is_unlocked_for_user(self, user):
        """Foydalanuvchi uchun test ochilganligini tekshirish"""
        if not user.is_authenticated:
            return False
        
        # Birinchi test har doim ochiq
        first_test = self.topic.cert_tests.filter(is_active=True).order_by('order', 'created_at').first()
        if self == first_test:
            return True
        
        # Oldingi testni topish
        previous_tests = self.topic.cert_tests.filter(
            is_active=True,
            order__lt=self.order
        ).order_by('order', 'created_at')
        
        if not previous_tests.exists():
            # Agar order bir xil bo'lsa, created_at bo'yicha
            previous_tests = self.topic.cert_tests.filter(
                is_active=True,
                created_at__lt=self.created_at
            ).order_by('order', 'created_at')
        
        # Barcha oldingi testlar o'tilganligini tekshirish
        for prev_test in previous_tests:
            best_result = CertificateResult.objects.filter(
                user=user,
                test=prev_test
            ).order_by('-score').first()
            
            if not best_result or best_result.score < prev_test.unlock_score:
                return False
        
        return True


class CertificateQuestion(models.Model):
    test = models.ForeignKey(CertificateTest, on_delete=models.CASCADE, related_name='cert_questions', verbose_name="Test")
    long_text = models.TextField(blank=True, null=True, verbose_name="Uzun matn", help_text="Hikoya, she'r yoki uzun matn (ixtiyoriy)")
    text = models.TextField(verbose_name="Savol matni")
    image = models.ImageField(upload_to='cert_questions/', blank=True, null=True, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    points = models.PositiveIntegerField(default=1, verbose_name="Ball")
    
    class Meta:
        ordering = ['order']
        verbose_name = "Sertifikat savoli"
        verbose_name_plural = "Sertifikat savollari"
    
    def __str__(self):
        return self.text[:50]


class CertificateAnswer(models.Model):
    question = models.ForeignKey(CertificateQuestion, on_delete=models.CASCADE, related_name='cert_answers', verbose_name="Savol")
    text = models.CharField(max_length=500, verbose_name="Javob matni")
    image = models.ImageField(upload_to='cert_answers/', blank=True, null=True, verbose_name="Javob rasmi")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javob")
    
    class Meta:
        verbose_name = "Sertifikat javobi"
        verbose_name_plural = "Sertifikat javoblari"
    
    def __str__(self):
        return self.text[:50]


class CertificateResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificate_results')
    test = models.ForeignKey(CertificateTest, on_delete=models.CASCADE, related_name='cert_results')
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    time_taken = models.PositiveIntegerField(default=0)
    user_answers = models.JSONField(default=dict, blank=True, verbose_name="Foydalanuvchi javoblari")
    earned_points = models.PositiveIntegerField(default=0, verbose_name="Olingan ball")
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-completed_at']
        verbose_name = "Sertifikat natijasi"
        verbose_name_plural = "Sertifikat natijalari"
    
    def __str__(self):
        return f"{self.user.username} - {self.test.title} - {self.score}%"


class MockExamCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name="Kategoriya nomi")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    icon = models.CharField(max_length=50, default='bi-clipboard-check', verbose_name="Icon")
    image = models.ImageField(upload_to='mock_categories/', blank=True, null=True, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Mock imtihon kategoriyasi"
        verbose_name_plural = "Mock imtihon kategoriyalari"
    
    def __str__(self):
        return self.name


class MockExam(models.Model):
    category = models.ForeignKey(MockExamCategory, on_delete=models.CASCADE, related_name='mock_exams', verbose_name="Kategoriya", null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name="Imtihon nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    image = models.ImageField(upload_to='mock_exams/', blank=True, null=True, verbose_name="Rasm")
    time_limit = models.PositiveIntegerField(default=120, verbose_name="Vaqt limiti (daqiqa)")
    passing_score = models.PositiveIntegerField(default=60, verbose_name="O'tish balli (%)")
    unlock_score = models.PositiveIntegerField(default=60, verbose_name="Ochish uchun kerakli ball (%)")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Mock imtihon"
        verbose_name_plural = "Mock imtihonlar"
    
    def __str__(self):
        return self.title
    
    def get_max_points(self):
        """Imtihondagi barcha savollar ballarining yig'indisini qaytarish"""
        return self.mock_questions.aggregate(
            total_points=models.Sum('points')
        )['total_points'] or 0
    
    def is_unlocked_for_user(self, user):
        """Mock imtihonlar uchun barcha imtihonlar ochiq"""
        return True


class MockExamQuestion(models.Model):
    exam = models.ForeignKey(MockExam, on_delete=models.CASCADE, related_name='mock_questions', verbose_name="Imtihon")
    long_text = models.TextField(blank=True, null=True, verbose_name="Uzun matn", help_text="Hikoya, she'r yoki uzun matn (ixtiyoriy)")
    text = models.TextField(verbose_name="Savol matni")
    image = models.ImageField(upload_to='mock_questions/', blank=True, null=True, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    points = models.FloatField(default=1.0, verbose_name="Ball")
    
    class Meta:
        ordering = ['order']
        verbose_name = "Mock savol"
        verbose_name_plural = "Mock savollar"
    
    def __str__(self):
        return self.text[:50]


class MockExamAnswer(models.Model):
    question = models.ForeignKey(MockExamQuestion, on_delete=models.CASCADE, related_name='mock_answers', verbose_name="Savol")
    text = models.CharField(max_length=500, verbose_name="Javob matni")
    image = models.ImageField(upload_to='mock_answers/', blank=True, null=True, verbose_name="Javob rasmi")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javob")
    
    class Meta:
        verbose_name = "Mock javob"
        verbose_name_plural = "Mock javoblar"
    
    def __str__(self):
        return self.text[:50]


class MockExamResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mock_results')
    exam = models.ForeignKey(MockExam, on_delete=models.CASCADE, related_name='mock_results')
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    time_taken = models.PositiveIntegerField(default=0)
    user_answers = models.JSONField(default=dict, blank=True, verbose_name="Foydalanuvchi javoblari")
    earned_points = models.PositiveIntegerField(default=0, verbose_name="Olingan ball")
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-completed_at']
        verbose_name = "Mock natija"
        verbose_name_plural = "Mock natijalar"
    
    def __str__(self):
        return f"{self.user.username} - {self.exam.title} - {self.score}%"


class InstitutionCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name="Kategoriya nomi")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    icon = models.CharField(max_length=50, default='bi-building', verbose_name="Icon")
    image = models.ImageField(upload_to='institution_categories/', blank=True, null=True, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Muassasa kategoriyasi"
        verbose_name_plural = "Muassasa kategoriyalari"
    
    def __str__(self):
        return self.name


class InstitutionType(models.TextChoices):
    TRAINING_CENTER = 'training', "O'quv markazi"
    STATE_SCHOOL = 'state_school', "Davlat maktabi"
    PRIVATE_SCHOOL = 'private_school', "Xususiy maktab"
    STATE_UNIVERSITY = 'state_uni', "Davlat oliy ta'lim"
    FOREIGN_BRANCH = 'foreign_branch', "Xorijiy filial"
    PRIVATE_UNIVERSITY = 'private_uni', "Xususiy oliy ta'lim"
    CONSULTING = 'consulting', "Konsalting"


class Institution(models.Model):
    name = models.CharField(max_length=300, verbose_name="Nomi")
    category = models.ForeignKey(InstitutionCategory, on_delete=models.CASCADE, related_name='institutions', verbose_name="Kategoriya", null=True, blank=True)
    institution_type = models.CharField(max_length=20, choices=InstitutionType.choices, verbose_name="Turi")
    short_description = models.TextField(max_length=200, blank=True, verbose_name="Qisqa tavsif")
    description = models.TextField(blank=True, verbose_name="To'liq tavsif")
    image = models.ImageField(upload_to='institutions/', blank=True, null=True, verbose_name="Asosiy rasm")
    logo = models.ImageField(upload_to='institutions/logos/', blank=True, null=True, verbose_name="Logo")
    address = models.TextField(blank=True, verbose_name="Manzil")
    address_iframe = models.TextField(blank=True, verbose_name="Manzil iframe kodi")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="Email")
    website = models.URLField(blank=True, verbose_name="Veb-sayt")
    contract_price_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Kontrakt summasi (min)")
    contract_price_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Kontrakt summasi (max)")
    admission_start_date = models.DateField(null=True, blank=True, verbose_name="Qabul boshlanish sanasi")
    admission_end_date = models.DateField(null=True, blank=True, verbose_name="Qabul tugash sanasi")
    license_file = models.FileField(upload_to='institutions/licenses/', blank=True, null=True, verbose_name="Litsenziya fayli")
    video_url = models.URLField(max_length=500, blank=True, verbose_name="Video URL (YouTube)")
    telegram = models.URLField(max_length=300, blank=True, verbose_name="Telegram")
    instagram = models.URLField(max_length=300, blank=True, verbose_name="Instagram")
    youtube = models.URLField(max_length=300, blank=True, verbose_name="YouTube")
    facebook = models.URLField(max_length=300, blank=True, verbose_name="Facebook")
    is_featured = models.BooleanField(default=False, verbose_name="Reklama")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Ta'lim muassasasi"
        verbose_name_plural = "Ta'lim muassasalari"
    
    def __str__(self):
        return self.name
    
    def get_contract_price_range(self):
        """Kontrakt summasi oralig'ini qaytarish"""
        if self.contract_price_min and self.contract_price_max:
            return f"{self.contract_price_min:,.0f} - {self.contract_price_max:,.0f} so'm"
        elif self.contract_price_min:
            return f"{self.contract_price_min:,.0f} so'm dan"
        elif self.contract_price_max:
            return f"{self.contract_price_max:,.0f} so'm gacha"
        return "Narx ko'rsatilmagan"
    
    def get_admission_period(self):
        """Qabul muddatini qaytarish"""
        if self.admission_start_date and self.admission_end_date:
            return f"{self.admission_start_date.strftime('%d.%m.%Y')} - {self.admission_end_date.strftime('%d.%m.%Y')}"
        elif self.admission_start_date:
            return f"{self.admission_start_date.strftime('%d.%m.%Y')} dan"
        elif self.admission_end_date:
            return f"{self.admission_end_date.strftime('%d.%m.%Y')} gacha"
        return "Qabul muddati ko'rsatilmagan"
    
    def get_directions_count(self):
        """Yo'nalishlar sonini qaytarish"""
        return self.directions.filter(is_active=True).count()
    
    def get_video_embed_url(self):
        """YouTube URL'ni embed formatiga o'tkazish"""
        if not self.video_url:
            return None
        
        url = self.video_url.strip()
        
        # YouTube watch URL
        if 'youtube.com/watch?v=' in url:
            video_id = url.split('watch?v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1'
        
        # YouTube short URL
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1'
        
        # YouTube embed URL (agar allaqachon embed bo'lsa)
        elif 'youtube.com/embed/' in url:
            return url
        
        # Vimeo URL
        elif 'vimeo.com/' in url:
            video_id = url.split('vimeo.com/')[1].split('?')[0]
            return f'https://player.vimeo.com/video/{video_id}'
        
        # Agar boshqa format bo'lsa, o'zini qaytarish
        return url


class EducationLanguage(models.TextChoices):
    UZBEK = 'uzbek', "O'zbek tili"
    RUSSIAN = 'russian', "Rus tili"
    ENGLISH = 'english', "Ingliz tili"
    MIXED = 'mixed', "Aralash"


class EducationForm(models.TextChoices):
    FULL_TIME = 'full_time', "Kunduzgi"
    PART_TIME = 'part_time', "Sirtqi"
    EVENING = 'evening', "Kechki"
    DISTANCE = 'distance', "Masofaviy"


class InstitutionDirection(models.Model):
    """Muassasa yo'nalishlari"""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='directions', verbose_name="Muassasa")
    name = models.CharField(max_length=300, verbose_name="Yo'nalish nomi")
    description = models.TextField(blank=True, verbose_name="Yo'nalish tavsifi")
    contract_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Kontrakt summasi")
    education_language = models.CharField(max_length=20, choices=EducationLanguage.choices, default=EducationLanguage.UZBEK, verbose_name="Ta'lim tili")
    education_form = models.CharField(max_length=20, choices=EducationForm.choices, default=EducationForm.FULL_TIME, verbose_name="Ta'lim shakli")
    passing_score = models.PositiveIntegerField(null=True, blank=True, verbose_name="O'tish bali")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Muassasa yo'nalishi"
        verbose_name_plural = "Muassasa yo'nalishlari"
    
    def __str__(self):
        return f"{self.institution.name} - {self.name}"
    
    def get_contract_price_display(self):
        """Yo'nalish kontrakt summasini qaytarish"""
        if self.contract_price:
            return f"{self.contract_price:,.0f} so'm"
        return "Narx ko'rsatilmagan"


class Advertisement(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    image = models.ImageField(upload_to='ads/', verbose_name="Rasm")
    link = models.URLField(blank=True, verbose_name="Havola")
    link_url = models.URLField(blank=True, null=True, verbose_name="Havola URL")
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ta'lim muassasasi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Reklama"
        verbose_name_plural = "Reklamalar"
    
    def __str__(self):
        return self.title


class Statistic(models.Model):
    title = models.CharField(max_length=100, verbose_name="Sarlavha")
    value = models.CharField(max_length=50, verbose_name="Qiymat")
    icon = models.CharField(max_length=50, default='bi-graph-up', verbose_name="Icon")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    
    class Meta:
        ordering = ['order']
        verbose_name = "Statistika"
        verbose_name_plural = "Statistikalar"
    
    def __str__(self):
        return self.title


class NewsCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    icon = models.CharField(max_length=50, default='bi-newspaper', verbose_name="Icon")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Yangilik kategoriyasi"
        verbose_name_plural = "Yangilik kategoriyalari"
    
    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=300, verbose_name="Sarlavha")
    slug = models.SlugField(max_length=300, unique=True, verbose_name="Slug")
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='news', verbose_name="Kategoriya")
    summary = models.TextField(max_length=500, verbose_name="Qisqacha mazmuni")
    content = models.TextField(verbose_name="To'liq mazmuni")
    image = models.ImageField(upload_to='news/', verbose_name="Asosiy rasm")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Muallif")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    is_featured = models.BooleanField(default=False, verbose_name="Asosiy yangilik")
    is_published = models.BooleanField(default=True, verbose_name="Nashr qilingan")
    published_at = models.DateTimeField(auto_now_add=True, verbose_name="Nashr sanasi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    class Meta:
        ordering = ['-published_at']
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])


class CourseCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name="Kategoriya nomi")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    icon = models.CharField(max_length=50, default='bi-play-circle', verbose_name="Icon")
    image = models.ImageField(upload_to='course_categories/', blank=True, null=True, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Kurs kategoriyasi"
        verbose_name_plural = "Kurs kategoriyalari"
    
    def __str__(self):
        return self.name


class Course(models.Model):
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='courses', verbose_name="Kategoriya")
    title = models.CharField(max_length=300, verbose_name="Kurs nomi")
    slug = models.SlugField(max_length=300, unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Tavsif")
    image = models.ImageField(upload_to='courses/', verbose_name="Kurs rasmi")
    instructor = models.CharField(max_length=200, verbose_name="O'qituvchi")
    duration = models.CharField(max_length=100, blank=True, verbose_name="Davomiyligi")
    level = models.CharField(max_length=50, choices=[
        ('beginner', 'Boshlang\'ich'),
        ('intermediate', 'O\'rta'),
        ('advanced', 'Yuqori')
    ], default='beginner', verbose_name="Daraja")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Narxi")
    payment_url = models.URLField(blank=True, verbose_name="To'lov URL manzili")
    is_free = models.BooleanField(default=False, verbose_name="Bepul")
    is_featured = models.BooleanField(default=False, verbose_name="Mashhur")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"
    
    def __str__(self):
        return self.title
    
    def get_lessons_count(self):
        return self.lessons.count()


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name="Kurs")
    title = models.CharField(max_length=300, verbose_name="Dars nomi")
    description = models.TextField(verbose_name="Tavsif")
    content = models.TextField(verbose_name="Matnli ma'lumot")
    video_url = models.URLField(max_length=500, blank=True, verbose_name="Video URL (YouTube, Vimeo)")
    video_file = models.FileField(upload_to='lessons/videos/', blank=True, null=True, verbose_name="Video fayl")
    duration = models.CharField(max_length=50, blank=True, verbose_name="Davomiyligi")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_free = models.BooleanField(default=False, verbose_name="Bepul dars")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def get_embed_url(self):
        """YouTube URL'ni embed formatiga o'tkazish"""
        if not self.video_url:
            return None
        
        url = self.video_url
        
        # YouTube watch URL
        if 'youtube.com/watch?v=' in url:
            video_id = url.split('watch?v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        
        # YouTube short URL
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        
        # Vimeo URL
        elif 'vimeo.com/' in url:
            video_id = url.split('vimeo.com/')[1].split('?')[0]
            return f'https://player.vimeo.com/video/{video_id}'
        
        # Agar boshqa format bo'lsa, o'zini qaytarish
        return url


class CourseEnrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    progress = models.PositiveIntegerField(default=0, verbose_name="Progress (%)")
    payment_confirmed = models.BooleanField(default=False, verbose_name="To'lov tasdiqlangan")
    
    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']
        verbose_name = "Kursga yozilish"
        verbose_name_plural = "Kursga yozilishlar"
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class NotificationType(models.TextChoices):
    NEWS = 'news', 'Yangilik'
    TEST = 'test', 'Yangi test'
    CERTIFICATE = 'certificate', 'Yangi sertifikat'
    MOCK_EXAM = 'mock_exam', 'Yangi mock exam'
    COURSE = 'course', 'Yangi kurs'
    SYSTEM = 'system', 'Tizim xabari'


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', verbose_name="Foydalanuvchi", null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices, verbose_name="Turi")
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    message = models.TextField(verbose_name="Xabar")
    link = models.CharField(max_length=500, blank=True, verbose_name="Havola")
    icon = models.CharField(max_length=50, default='bi-bell', verbose_name="Icon")
    is_read = models.BooleanField(default=False, verbose_name="O'qilgan")
    is_global = models.BooleanField(default=False, verbose_name="Barcha foydalanuvchilar uchun")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bildirishnoma"
        verbose_name_plural = "Bildirishnomalar"
    
    def __str__(self):
        return f"{self.title} - {self.get_notification_type_display()}"
    
    def is_read_by_user(self, user):
        """Foydalanuvchi tomonidan o'qilganligini tekshirish"""
        if self.is_global:
            # Global bildirishnoma uchun NotificationRead modelini tekshirish
            return NotificationRead.objects.filter(notification=self, user=user).exists()
        else:
            # Shaxsiy bildirishnoma uchun is_read maydonini tekshirish
            return self.is_read


class NotificationRead(models.Model):
    """Global bildirishnomalarni kim o'qiganligi uchun"""
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='reads')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['notification', 'user']
        verbose_name = "Bildirishnoma o'qilganligi"
        verbose_name_plural = "Bildirishnoma o'qilganliklari"
    
    def __str__(self):
        return f"{self.user.username} - {self.notification.title}"


# ==================== Yo'nalish Imtihon Modellari ====================

class DirectionExam(models.Model):
    """Yo'nalish imtihoni"""
    direction = models.ForeignKey(InstitutionDirection, on_delete=models.CASCADE, related_name='exams', verbose_name="Yo'nalish")
    title = models.CharField(max_length=300, verbose_name="Imtihon nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    subjects = models.CharField(max_length=500, verbose_name="Fanlar (vergul bilan ajratilgan)")
    time_limit = models.PositiveIntegerField(default=120, verbose_name="Vaqt limiti (daqiqa)")
    passing_score = models.FloatField(default=60.0, verbose_name="O'tish balli (ball)")
    application_url = models.URLField(blank=True, verbose_name="Ariza qoldirish URL")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Yo'nalish imtihoni"
        verbose_name_plural = "Yo'nalish imtihonlari"
    
    def __str__(self):
        return f"{self.direction.name} - {self.title}"
    
    def get_subjects_list(self):
        """Fanlar ro'yxatini qaytarish"""
        return [s.strip() for s in self.subjects.split(',') if s.strip()]
    
    def get_max_points(self):
        """Imtihondagi barcha savollar ballarining yig'indisini qaytarish"""
        return self.direction_questions.aggregate(
            total_points=models.Sum('points')
        )['total_points'] or 0
    
    def get_questions_count(self):
        return self.direction_questions.count()


class DirectionExamQuestion(models.Model):
    """Yo'nalish imtihon savoli"""
    exam = models.ForeignKey(DirectionExam, on_delete=models.CASCADE, related_name='direction_questions', verbose_name="Imtihon")
    long_text = models.TextField(blank=True, null=True, verbose_name="Uzun matn", help_text="Hikoya, she'r yoki uzun matn (ixtiyoriy)")
    text = models.TextField(verbose_name="Savol matni")
    image = models.ImageField(upload_to='direction_questions/', blank=True, null=True, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    points = models.FloatField(default=1.1, verbose_name="Ball")
    
    class Meta:
        ordering = ['order']
        verbose_name = "Yo'nalish imtihon savoli"
        verbose_name_plural = "Yo'nalish imtihon savollari"
    
    def __str__(self):
        return self.text[:50]


class DirectionExamAnswer(models.Model):
    """Yo'nalish imtihon javobi"""
    question = models.ForeignKey(DirectionExamQuestion, on_delete=models.CASCADE, related_name='direction_answers', verbose_name="Savol")
    text = models.CharField(max_length=500, verbose_name="Javob matni")
    image = models.ImageField(upload_to='direction_answers/', blank=True, null=True, verbose_name="Javob rasmi")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javob")
    
    class Meta:
        verbose_name = "Yo'nalish imtihon javobi"
        verbose_name_plural = "Yo'nalish imtihon javoblari"
    
    def __str__(self):
        return self.text[:50]


class DirectionExamResult(models.Model):
    """Yo'nalish imtihon natijasi"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='direction_exam_results')
    exam = models.ForeignKey(DirectionExam, on_delete=models.CASCADE, related_name='direction_results')
    score = models.FloatField(default=0, verbose_name="Foiz (%)")
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    time_taken = models.PositiveIntegerField(default=0, verbose_name="Sarflangan vaqt (soniya)")
    user_answers = models.JSONField(default=dict, blank=True, verbose_name="Foydalanuvchi javoblari")
    earned_points = models.FloatField(default=0, verbose_name="Olingan ball")
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-completed_at']
        verbose_name = "Yo'nalish imtihon natijasi"
        verbose_name_plural = "Yo'nalish imtihon natijalari"
    
    @property
    def incorrect_answers(self):
        """Noto'g'ri javoblar soni"""
        return self.total_questions - self.correct_answers
    
    @property
    def formatted_time(self):
        """Sarflangan vaqtni formatlash (MM:SS)"""
        minutes = self.time_taken // 60
        seconds = self.time_taken % 60
        return f"{minutes}:{seconds:02d}"
    
    def __str__(self):
        return f"{self.user.username} - {self.exam.title} - {self.score:.1f}%"


class Partner(models.Model):
    """Hamkorlar modeli"""
    name = models.CharField(max_length=200, verbose_name="Hamkor nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    logo = models.ImageField(upload_to='partners/', verbose_name="Logo")
    website_url = models.URLField(blank=True, verbose_name="Veb-sayt havolasi")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Hamkor"
        verbose_name_plural = "Hamkorlar"
    
    def __str__(self):
        return self.name
