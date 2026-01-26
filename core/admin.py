from django.contrib import admin
from .models import (
    SiteSettings, DifficultyLevel, SubjectCategory, Subject, Topic, Question, Answer, TopicResult,
    Certificate, CertificateTopic, CertificateTest, CertificateQuestion, CertificateAnswer, CertificateResult,
    MockExamCategory, MockExam, MockExamQuestion, MockExamAnswer, MockExamResult,
    InstitutionCategory, Institution, InstitutionDirection, Advertisement, Statistic, NewsCategory, News,
    CourseCategory, Course, Lesson, CourseEnrollment, Notification, NotificationRead,
    DirectionExam, DirectionExamQuestion, DirectionExamAnswer, DirectionExamResult, Partner
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'contact_email', 'contact_phone']


@admin.register(DifficultyLevel)
class DifficultyLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    list_editable = ['color', 'icon', 'order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


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
    list_display = ['name', 'subject', 'time_limit', 'passing_score', 'order', 'is_active', 'questions_count_display', 'created_at']
    list_filter = ['subject', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['time_limit', 'passing_score', 'order', 'is_active']
    inlines = [QuestionInline]
    
    def questions_count_display(self, obj):
        return obj.get_questions_count()
    questions_count_display.short_description = 'Savollar soni'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'topic', 'order', 'points', 'has_long_text', 'has_image']
    list_filter = ['topic__subject', 'topic']
    search_fields = ['text', 'long_text']
    list_editable = ['points']
    inlines = [AnswerInline]
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('topic', 'text', 'order', 'points')
        }),
        ('Qo\'shimcha kontent', {
            'fields': ('long_text', 'image'),
            'description': 'Uzun matn (hikoya, she\'r) va rasm qo\'shish uchun'
        }),
    )
    
    def has_long_text(self, obj):
        return bool(obj.long_text and obj.long_text.strip())
    has_long_text.boolean = True
    has_long_text.short_description = 'Uzun matn'
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Rasm'


@admin.register(TopicResult)
class TopicResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'topic', 'score', 'correct_answers', 'total_questions', 'earned_points', 'passed', 'completed_at']
    list_filter = ['passed', 'completed_at', 'topic__subject']
    search_fields = ['user__username', 'topic__name']
    readonly_fields = ['user', 'topic', 'score', 'correct_answers', 'total_questions', 'earned_points', 'passed', 'completed_at']


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
    list_display = ['title', 'topic', 'order', 'time_limit', 'passing_score', 'unlock_score', 'is_active']
    list_filter = ['topic__certificate', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'unlock_score', 'is_active']
    inlines = [CertQuestionInline]


@admin.register(CertificateQuestion)
class CertificateQuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'test', 'order', 'points', 'has_long_text', 'has_image']
    list_filter = ['test__topic__certificate', 'test']
    search_fields = ['text', 'long_text']
    list_editable = ['points']
    inlines = [CertAnswerInline]
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('test', 'text', 'order', 'points')
        }),
        ('Qo\'shimcha kontent', {
            'fields': ('long_text', 'image'),
            'description': 'Uzun matn (hikoya, she\'r) va rasm qo\'shish uchun'
        }),
    )
    
    def has_long_text(self, obj):
        return bool(obj.long_text and obj.long_text.strip())
    has_long_text.boolean = True
    has_long_text.short_description = 'Uzun matn'
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Rasm'


@admin.register(CertificateResult)
class CertificateResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'score', 'correct_answers', 'total_questions', 'earned_points', 'passed', 'completed_at']
    list_filter = ['passed', 'completed_at']
    readonly_fields = ['user', 'test', 'score', 'correct_answers', 'total_questions', 'earned_points', 'passed', 'completed_at']


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
    list_display = ['title', 'category', 'time_limit', 'passing_score', 'unlock_score', 'order', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['unlock_score', 'order', 'is_active']
    inlines = [MockQuestionInline]


@admin.register(MockExamQuestion)
class MockExamQuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'exam', 'order', 'points', 'has_long_text', 'has_image']
    list_filter = ['exam']
    search_fields = ['text', 'long_text']
    list_editable = ['points']
    inlines = [MockAnswerInline]
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('exam', 'text', 'order', 'points')
        }),
        ('Qo\'shimcha kontent', {
            'fields': ('long_text', 'image'),
            'description': 'Uzun matn (hikoya, she\'r) va rasm qo\'shish uchun'
        }),
    )
    
    def has_long_text(self, obj):
        return bool(obj.long_text and obj.long_text.strip())
    has_long_text.boolean = True
    has_long_text.short_description = 'Uzun matn'
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Rasm'


@admin.register(MockExamResult)
class MockExamResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'exam', 'score', 'correct_answers', 'total_questions', 'earned_points', 'passed', 'completed_at']
    list_filter = ['passed', 'completed_at', 'exam']
    readonly_fields = ['user', 'exam', 'score', 'correct_answers', 'total_questions', 'earned_points', 'passed', 'completed_at']


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


class DirectionExamInline(admin.TabularInline):
    model = DirectionExam
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
        ('Ijtimoiy tarmoqlar', {
            'fields': ('telegram', 'instagram', 'youtube', 'facebook')
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
    inlines = [DirectionExamInline]
    
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
        ('Sozlamalar', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'institution', 'link_url', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'order']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'description', 'image', 'institution')
        }),
        ('Havolalar', {
            'fields': ('link', 'link_url')
        }),
        ('Sozlamalar', {
            'fields': ('is_active', 'order')
        }),
    )


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
            'fields': ('duration', 'level', 'price', 'is_free', 'payment_url')
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
    list_display = ['user', 'course', 'progress', 'completed', 'payment_confirmed', 'enrolled_at']
    list_filter = ['completed', 'payment_confirmed', 'enrolled_at', 'course__category']
    search_fields = ['user__username', 'course__title']
    list_editable = ['payment_confirmed']
    readonly_fields = ['enrolled_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'notification_type', 'user', 'is_global', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_global', 'is_read', 'created_at']
    search_fields = ['title', 'message']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('notification_type', 'title', 'message', 'link', 'icon')
        }),
        ('Qabul qiluvchi', {
            'fields': ('user', 'is_global'),
            'description': 'Agar "Barcha foydalanuvchilar uchun" belgilansa, "Foydalanuvchi" maydoni e\'tiborga olinmaydi.'
        }),
        ('Vaqt', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        """Bildirishnoma saqlanayotganda qo'shimcha tekshiruvlar"""
        super().save_model(request, obj, form, change)
        
        # Agar yangi bildirishnoma yaratilgan bo'lsa, Telegram orqali yuborish
        if not change:  # Yangi obyekt
            from django.contrib import messages
            messages.success(request, f"Bildirishnoma yaratildi va Telegram orqali yuborildi: {obj.title}")


@admin.register(NotificationRead)
class NotificationReadAdmin(admin.ModelAdmin):
    list_display = ['notification', 'user', 'read_at']
    list_filter = ['read_at']
    search_fields = ['notification__title', 'user__username']
    readonly_fields = ['read_at']


# ==================== Yo'nalish Imtihon Admin ====================

class DirectionExamAnswerInline(admin.TabularInline):
    model = DirectionExamAnswer
    extra = 4


class DirectionExamQuestionInline(admin.TabularInline):
    model = DirectionExamQuestion
    extra = 1
    show_change_link = True


@admin.register(DirectionExam)
class DirectionExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'direction', 'subjects', 'time_limit', 'passing_score', 'questions_count_display', 'is_active', 'order']
    list_filter = ['direction__institution', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'subjects', 'direction__name']
    list_editable = ['passing_score', 'order', 'is_active']
    inlines = [DirectionExamQuestionInline]
    
    def questions_count_display(self, obj):
        return obj.get_questions_count()
    questions_count_display.short_description = 'Savollar soni'
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('direction', 'title', 'description')
        }),
        ('Imtihon sozlamalari', {
            'fields': ('subjects', 'time_limit', 'passing_score')
        }),
        ('Ariza', {
            'fields': ('application_url',),
            'description': 'O\'tgan foydalanuvchilar uchun ariza qoldirish havolasi'
        }),
        ('Sozlamalar', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(DirectionExamQuestion)
class DirectionExamQuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'exam', 'order', 'points', 'has_long_text', 'has_image']
    list_filter = ['exam__direction__institution', 'exam']
    search_fields = ['text', 'long_text']
    list_editable = ['order', 'points']
    inlines = [DirectionExamAnswerInline]
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('exam', 'text', 'order', 'points')
        }),
        ('Qo\'shimcha kontent', {
            'fields': ('long_text', 'image'),
            'description': 'Uzun matn (hikoya, she\'r) va rasm qo\'shish uchun'
        }),
    )
    
    def has_long_text(self, obj):
        return bool(obj.long_text and obj.long_text.strip())
    has_long_text.boolean = True
    has_long_text.short_description = 'Uzun matn'
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Rasm'


@admin.register(DirectionExamResult)
class DirectionExamResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'exam', 'score', 'earned_points', 'correct_answers', 'total_questions', 'passed', 'completed_at']
    list_filter = ['passed', 'completed_at', 'exam__direction__institution']
    search_fields = ['user__username', 'exam__title']
    readonly_fields = ['user', 'exam', 'score', 'earned_points', 'correct_answers', 'total_questions', 'passed', 'time_taken', 'user_answers', 'completed_at']


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'website_url', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'description', 'logo')
        }),
        ('Havola', {
            'fields': ('website_url',)
        }),
        ('Sozlamalar', {
            'fields': ('order', 'is_active')
        }),
    )
