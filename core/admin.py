from django.contrib import admin
from .models import (
    SiteSettings, SubjectCategory, Subject, Topic, Test, Question, Answer, TestResult,
    Certificate, CertificateTopic, CertificateTest, CertificateQuestion, CertificateAnswer, CertificateResult,
    MockExamCategory, MockExam, MockExamQuestion, MockExamAnswer, MockExamResult,
    InstitutionCategory, Institution, InstitutionDirection, Advertisement, Statistic, NewsCategory, News,
    CourseCategory, Course, Lesson, CourseEnrollment, Notification
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'contact_email', 'contact_phone']


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1
    show_change_link = True


class TestInline(admin.TabularInline):
    model = Test
    extra = 1
    show_change_link = True


@admin.register(SubjectCategory)
class SubjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order', 'is_active', 'get_topics_count', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    inlines = [TopicInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'order', 'is_active', 'created_at']
    list_filter = ['subject', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    inlines = [TestInline]


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'time_limit', 'passing_score', 'is_active', 'get_questions_count']
    list_filter = ['topic__subject', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'test', 'order']
    list_filter = ['test__topic__subject', 'test']
    search_fields = ['text']
    inlines = [AnswerInline]


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'score', 'correct_answers', 'total_questions', 'passed', 'completed_at']
    list_filter = ['passed', 'completed_at', 'test__topic__subject']
    search_fields = ['user__username', 'test__title']
    readonly_fields = ['user', 'test', 'score', 'correct_answers', 'total_questions', 'passed', 'completed_at']


class CertAnswerInline(admin.TabularInline):
    model = CertificateAnswer
    extra = 4


class CertQuestionInline(admin.TabularInline):
    model = CertificateQuestion
    extra = 1
    show_change_link = True


class CertTopicInline(admin.TabularInline):
    model = CertificateTopic
    extra = 1
    show_change_link = True


class CertTestInline(admin.TabularInline):
    model = CertificateTest
    extra = 1
    show_change_link = True


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    inlines = [CertTopicInline]


@admin.register(CertificateTopic)
class CertificateTopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'certificate', 'order', 'is_active']
    list_filter = ['certificate', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    inlines = [CertTestInline]


@admin.register(CertificateTest)
class CertificateTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'time_limit', 'passing_score', 'is_active']
    list_filter = ['topic__certificate', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    inlines = [CertQuestionInline]


@admin.register(CertificateQuestion)
class CertificateQuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'test', 'order']
    list_filter = ['test__topic__certificate', 'test']
    search_fields = ['text']
    inlines = [CertAnswerInline]


@admin.register(CertificateResult)
class CertificateResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'score', 'correct_answers', 'total_questions', 'passed', 'completed_at']
    list_filter = ['passed', 'completed_at']
    readonly_fields = ['user', 'test', 'score', 'correct_answers', 'total_questions', 'passed', 'completed_at']


class MockAnswerInline(admin.TabularInline):
    model = MockExamAnswer
    extra = 4


class MockQuestionInline(admin.TabularInline):
    model = MockExamQuestion
    extra = 1
    show_change_link = True


@admin.register(MockExamCategory)
class MockExamCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MockExam)
class MockExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'time_limit', 'passing_score', 'order', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    inlines = [MockQuestionInline]


@admin.register(MockExamQuestion)
class MockExamQuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'exam', 'order']
    list_filter = ['exam']
    search_fields = ['text']
    inlines = [MockAnswerInline]


@admin.register(MockExamResult)
class MockExamResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'exam', 'score', 'correct_answers', 'total_questions', 'passed', 'completed_at']
    list_filter = ['passed', 'completed_at', 'exam']
    readonly_fields = ['user', 'exam', 'score', 'correct_answers', 'total_questions', 'passed', 'completed_at']


@admin.register(InstitutionCategory)
class InstitutionCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


class InstitutionDirectionInline(admin.TabularInline):
    model = InstitutionDirection
    extra = 1
    show_change_link = True


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'institution_type', 'is_featured', 'is_active', 'order']
    list_filter = ['category', 'institution_type', 'is_featured', 'is_active']
    search_fields = ['name', 'description', 'address']
    list_editable = ['is_featured', 'is_active', 'order']
    inlines = [InstitutionDirectionInline]
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'category', 'institution_type', 'image', 'logo')
        }),
        ('Tavsif', {
            'fields': ('short_description', 'description')
        }),
        ('Kontrakt ma\'lumotlari', {
            'fields': ('contract_price_min', 'contract_price_max')
        }),
        ('Qabul ma\'lumotlari', {
            'fields': ('admission_start_date', 'admission_end_date')
        }),
        ('Hujjatlar va media', {
            'fields': ('license_file', 'video_url')
        }),
        ('Aloqa ma\'lumotlari', {
            'fields': ('phone', 'email', 'website', 'address', 'address_iframe')
        }),
        ('Sozlamalar', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )


@admin.register(InstitutionDirection)
class InstitutionDirectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'institution', 'get_contract_price_display', 'order', 'is_active']
    list_filter = ['institution', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'institution__name']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('institution', 'name', 'description')
        }),
        ('Ta\'lim ma\'lumotlari', {
            'fields': ('education_language', 'education_form', 'passing_score')
        }),
        ('Kontrakt ma\'lumotlari', {
            'fields': ('contract_price',)
        }),
        ('Imtihon', {
            'fields': ('exam_url',)
        }),
        ('Sozlamalar', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'institution', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'order']


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', 'icon', 'order']
    list_editable = ['value', 'icon', 'order']


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'views_count', 'is_featured', 'is_published', 'published_at']
    list_filter = ['category', 'is_featured', 'is_published', 'published_at']
    search_fields = ['title', 'summary', 'content']
    list_editable = ['is_featured', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'published_at', 'updated_at']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'category', 'author')
        }),
        ('Kontent', {
            'fields': ('summary', 'content', 'image')
        }),
        ('Sozlamalar', {
            'fields': ('is_featured', 'is_published')
        }),
        ('Statistika', {
            'fields': ('views_count', 'published_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.site_header = "EduSelf Admin"
admin.site.site_title = "EduSelf"
admin.site.index_title = "Boshqaruv paneli"


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    show_change_link = True


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'instructor', 'level', 'price', 'is_free', 'is_featured', 'is_active', 'get_lessons_count']
    list_filter = ['category', 'level', 'is_free', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'instructor']
    list_editable = ['is_featured', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('category', 'title', 'slug', 'instructor')
        }),
        ('Kontent', {
            'fields': ('description', 'image')
        }),
        ('Kurs ma\'lumotlari', {
            'fields': ('duration', 'level', 'price', 'is_free')
        }),
        ('Sozlamalar', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'duration', 'order', 'is_free', 'is_active', 'created_at']
    list_filter = ['course__category', 'course', 'is_free', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'content']
    list_editable = ['order', 'is_free', 'is_active']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('course', 'title', 'description')
        }),
        ('Kontent', {
            'fields': ('content', 'video_url', 'video_file', 'duration')
        }),
        ('Sozlamalar', {
            'fields': ('order', 'is_free', 'is_active')
        }),
    )


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'progress', 'completed', 'enrolled_at']
    list_filter = ['completed', 'enrolled_at', 'course__category']
    search_fields = ['user__username', 'course__title']
    readonly_fields = ['enrolled_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'notification_type', 'user', 'is_global', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_global', 'is_read', 'created_at']
    search_fields = ['title', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('notification_type', 'title', 'message', 'link', 'icon')
        }),
        ('Qabul qiluvchi', {
            'fields': ('user', 'is_global'),
            'description': 'Agar "Barcha foydalanuvchilar uchun" belgilansa, "Foydalanuvchi" maydoni e\'tiborga olinmaydi.'
        }),
        ('Holat', {
            'fields': ('is_read', 'created_at')
        }),
    )
