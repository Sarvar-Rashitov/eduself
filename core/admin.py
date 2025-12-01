from django.contrib import admin
from .models import (
    SiteSettings, Subject, Topic, Test, Question, Answer, TestResult,
    Certificate, CertificateTopic, CertificateTest, CertificateQuestion, CertificateAnswer, CertificateResult,
    MockExam, MockExamQuestion, MockExamAnswer, MockExamResult,
    Institution, Advertisement, Statistic
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


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'get_topics_count', 'created_at']
    list_filter = ['is_active', 'created_at']
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


@admin.register(MockExam)
class MockExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'time_limit', 'passing_score', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
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


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'institution_type', 'is_featured', 'is_active', 'order']
    list_filter = ['institution_type', 'is_featured', 'is_active']
    search_fields = ['name', 'description', 'address']
    list_editable = ['is_featured', 'is_active', 'order']


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


admin.site.site_header = "EduSelf Admin"
admin.site.site_title = "EduSelf"
admin.site.index_title = "Boshqaruv paneli"
