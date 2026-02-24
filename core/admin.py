from django.contrib import admin
from .models import (
    SiteSettings, DifficultyLevel, SubjectCategory, Subject, Topic, Question, Answer, TopicResult,
    Certificate, CertificateTopic, CertificateTest, CertificateQuestion, CertificateAnswer, CertificateResult,
    MockExamCategory, MockExam, MockExamQuestion, MockExamAnswer, MockExamResult,
    InstitutionCategory, Institution, InstitutionDirection, Advertisement, Statistic, NewsCategory, News,
    CourseCategory, Course, Lesson, CourseEnrollment, LessonProgress, Notification, NotificationRead,
    DirectionExam, DirectionExamQuestion, DirectionExamAnswer, DirectionExamResult, Partner, TranslationCache
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
    list_display = ['title', 'category', 'time_limit', 'passing_score', 'order', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    inlines = [MockQuestionInline]
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('category', 'title', 'description', 'image')
        }),
        ('Imtihon sozlamalari', {
            'fields': ('time_limit', 'passing_score')
        }),
        ('Sozlamalar', {
            'fields': ('order', 'is_active')
        }),
    )


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
            'fields': ('phone', 'email', 'website', 'application_url', 'address', 'address_iframe')
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
        ('Tashqi havola', {
            'fields': ('external_link', 'external_link_text'),
            'description': 'Yangilik detailida ko\'rsatiladigan tashqi havola (ixtiyoriy)'
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
        ('Amaliy mashq', {
            'fields': ('practice_topic',),
            'description': 'Darsga amaliy mashq sifatida mavzu ulang'
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
        
        # Agar yangi bildirishnoma yaratilgan bo'lsa
        if not change:  # Yangi obyekt
            from django.contrib import messages
            
            if obj.is_global:
                from accounts.models import User
                
                # Email yuborilishi kerak bo'lganlar (BARCHA email tasdiqlangan)
                email_count = User.objects.filter(
                    is_active=True,
                    email__isnull=False,
                    email_verified=True
                ).exclude(email='').count()
                
                # Telegram yuborilishi kerak bo'lganlar (Telegram ID bor)
                telegram_count = User.objects.filter(
                    is_active=True,
                    telegram_chat_id__isnull=False,
                    telegram_id__isnull=False
                ).exclude(telegram_chat_id='').count()
                
                messages.success(
                    request, 
                    f"✅ Global bildirishnoma yaratildi! (ID: {obj.id})\n"
                    f"📧 Email: {email_count} ta foydalanuvchiga\n"
                    f"📱 Telegram: {telegram_count} ta foydalanuvchiga\n"
                    f"⏳ Yuborish background'da davom etmoqda..."
                )
            else:
                user_info = f"{obj.user.first_name} ({obj.user.email})" if obj.user else "Noma'lum"
                
                # Qaysi usul bilan yuboriladi
                send_methods = []
                if obj.user:
                    if obj.user.email_verified:
                        send_methods.append("📧 Email")
                    if obj.user.telegram_id and obj.user.telegram_chat_id:
                        send_methods.append("📱 Telegram")
                
                send_str = " va ".join(send_methods) if send_methods else "❌ Yuborilmaydi"
                
                messages.success(
                    request, 
                    f"✅ Shaxsiy bildirishnoma yaratildi! (ID: {obj.id})\n"
                    f"👤 Foydalanuvchi: {user_info}\n"
                    f"📤 Yuborish: {send_str}"
                )


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


@admin.register(TranslationCache)
class TranslationCacheAdmin(admin.ModelAdmin):
    list_display = ['original_text_short', 'source_lang', 'target_lang', 'translated_text_short', 'hit_count', 'created_at']
    list_filter = ['source_lang', 'target_lang', 'created_at']
    search_fields = ['original_text', 'translated_text', 'text_hash']
    readonly_fields = ['text_hash', 'created_at', 'updated_at', 'hit_count']
    ordering = ['-hit_count', '-created_at']
    
    def original_text_short(self, obj):
        return obj.original_text[:50] + '...' if len(obj.original_text) > 50 else obj.original_text
    original_text_short.short_description = 'Original matn'
    
    def translated_text_short(self, obj):
        return obj.translated_text[:50] + '...' if len(obj.translated_text) > 50 else obj.translated_text
    translated_text_short.short_description = 'Tarjima'
    
    fieldsets = (
        ('Tarjima ma\'lumotlari', {
            'fields': ('source_lang', 'target_lang', 'original_text', 'translated_text')
        }),
        ('Texnik ma\'lumotlar', {
            'fields': ('text_hash', 'hit_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['clear_low_hit_cache']
    
    def clear_low_hit_cache(self, request, queryset):
        """Hit count 5 dan kam bo'lgan cache'larni o'chirish"""
        count = queryset.filter(hit_count__lt=5).delete()[0]
        self.message_user(request, f"{count} ta kam ishlatilgan cache o'chirildi.")
    clear_low_hit_cache.short_description = "Kam ishlatilgan cache'larni o'chirish (hit < 5)"
