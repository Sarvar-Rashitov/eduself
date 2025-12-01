from django.db import models
from django.conf import settings

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


class Subject(models.Model):
    name = models.CharField(max_length=200, verbose_name="Fan nomi")
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
    
    def get_tests_count(self):
        return sum(topic.tests.count() for topic in self.topics.all())


class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics', verbose_name="Fan")
    name = models.CharField(max_length=200, verbose_name="Mavzu nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Mavzu"
        verbose_name_plural = "Mavzular"
    
    def __str__(self):
        return f"{self.subject.name} - {self.name}"


class Test(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='tests', verbose_name="Mavzu")
    title = models.CharField(max_length=200, verbose_name="Test nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    time_limit = models.PositiveIntegerField(default=30, verbose_name="Vaqt limiti (daqiqa)")
    passing_score = models.PositiveIntegerField(default=60, verbose_name="O'tish balli (%)")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Test"
        verbose_name_plural = "Testlar"
    
    def __str__(self):
        return self.title
    
    def get_questions_count(self):
        return self.questions.count()


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions', verbose_name="Test")
    text = models.TextField(verbose_name="Savol matni")
    image = models.ImageField(upload_to='questions/', blank=True, null=True, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    
    class Meta:
        ordering = ['order']
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"
    
    def __str__(self):
        return self.text[:50]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name="Savol")
    text = models.CharField(max_length=500, verbose_name="Javob matni")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javob")
    
    class Meta:
        verbose_name = "Javob"
        verbose_name_plural = "Javoblar"
    
    def __str__(self):
        return self.text[:50]


class TestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='test_results')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    time_taken = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-completed_at']
        verbose_name = "Test natijasi"
        verbose_name_plural = "Test natijalari"
    
    def __str__(self):
        return f"{self.user.username} - {self.test.title} - {self.score}%"


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
    name = models.CharField(max_length=200, verbose_name="Mavzu nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Sertifikat mavzusi"
        verbose_name_plural = "Sertifikat mavzulari"
    
    def __str__(self):
        return f"{self.certificate.name} - {self.name}"


class CertificateTest(models.Model):
    topic = models.ForeignKey(CertificateTopic, on_delete=models.CASCADE, related_name='cert_tests', verbose_name="Mavzu")
    title = models.CharField(max_length=200, verbose_name="Test nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    time_limit = models.PositiveIntegerField(default=30, verbose_name="Vaqt limiti (daqiqa)")
    passing_score = models.PositiveIntegerField(default=60, verbose_name="O'tish balli (%)")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sertifikat testi"
        verbose_name_plural = "Sertifikat testlari"
    
    def __str__(self):
        return self.title


class CertificateQuestion(models.Model):
    test = models.ForeignKey(CertificateTest, on_delete=models.CASCADE, related_name='cert_questions', verbose_name="Test")
    text = models.TextField(verbose_name="Savol matni")
    image = models.ImageField(upload_to='cert_questions/', blank=True, null=True, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    
    class Meta:
        ordering = ['order']
        verbose_name = "Sertifikat savoli"
        verbose_name_plural = "Sertifikat savollari"
    
    def __str__(self):
        return self.text[:50]


class CertificateAnswer(models.Model):
    question = models.ForeignKey(CertificateQuestion, on_delete=models.CASCADE, related_name='cert_answers', verbose_name="Savol")
    text = models.CharField(max_length=500, verbose_name="Javob matni")
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
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-completed_at']
        verbose_name = "Sertifikat natijasi"
        verbose_name_plural = "Sertifikat natijalari"


class MockExam(models.Model):
    title = models.CharField(max_length=200, verbose_name="Imtihon nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    image = models.ImageField(upload_to='mock_exams/', blank=True, null=True, verbose_name="Rasm")
    time_limit = models.PositiveIntegerField(default=120, verbose_name="Vaqt limiti (daqiqa)")
    passing_score = models.PositiveIntegerField(default=60, verbose_name="O'tish balli (%)")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Mock imtihon"
        verbose_name_plural = "Mock imtihonlar"
    
    def __str__(self):
        return self.title


class MockExamQuestion(models.Model):
    exam = models.ForeignKey(MockExam, on_delete=models.CASCADE, related_name='mock_questions', verbose_name="Imtihon")
    text = models.TextField(verbose_name="Savol matni")
    image = models.ImageField(upload_to='mock_questions/', blank=True, null=True, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    
    class Meta:
        ordering = ['order']
        verbose_name = "Mock savol"
        verbose_name_plural = "Mock savollar"
    
    def __str__(self):
        return self.text[:50]


class MockExamAnswer(models.Model):
    question = models.ForeignKey(MockExamQuestion, on_delete=models.CASCADE, related_name='mock_answers', verbose_name="Savol")
    text = models.CharField(max_length=500, verbose_name="Javob matni")
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
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-completed_at']
        verbose_name = "Mock natija"
        verbose_name_plural = "Mock natijalar"


class InstitutionType(models.TextChoices):
    TRAINING_CENTER = 'training', "O'quv markazi"
    STATE_SCHOOL = 'state_school', "Davlat maktabi"
    PRIVATE_SCHOOL = 'private_school', "Xususiy maktab"
    STATE_UNIVERSITY = 'state_uni', "Davlat oliy ta'lim"
    FOREIGN_BRANCH = 'foreign_branch', "Xorijiy filial"
    PRIVATE_UNIVERSITY = 'private_uni', "Xususiy oliy ta'lim"


class Institution(models.Model):
    name = models.CharField(max_length=300, verbose_name="Nomi")
    institution_type = models.CharField(max_length=20, choices=InstitutionType.choices, verbose_name="Turi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    logo = models.ImageField(upload_to='institutions/', blank=True, null=True, verbose_name="Logo")
    address = models.TextField(blank=True, verbose_name="Manzil")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="Email")
    website = models.URLField(blank=True, verbose_name="Veb-sayt")
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


class Advertisement(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    image = models.ImageField(upload_to='ads/', verbose_name="Rasm")
    link = models.URLField(blank=True, verbose_name="Havola")
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
