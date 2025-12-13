from django.contrib import admin
from .models import (
    ChatSession, ChatMessage, AIPromptTemplate, AIUsageStatistics,
    SubjectKnowledgeBase, InstitutionRecommendation
)


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at', 'is_active', 'get_messages_count']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['title', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_messages_count(self, obj):
        return obj.get_messages_count()
    get_messages_count.short_description = 'Xabarlar soni'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_type', 'content_preview', 'created_at', 'tokens_used', 'response_time']
    list_filter = ['message_type', 'created_at']
    search_fields = ['content', 'session__title', 'session__user__username']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Xabar matni'


@admin.register(AIPromptTemplate)
class AIPromptTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'order', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']


@admin.register(AIUsageStatistics)
class AIUsageStatisticsAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'messages_sent', 'tokens_used', 'sessions_created']
    list_filter = ['date']
    search_fields = ['user__username', 'user__email']
    date_hierarchy = 'date'


@admin.register(SubjectKnowledgeBase)
class SubjectKnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ['subject', 'topic_name', 'difficulty_level', 'is_active', 'created_at']
    list_filter = ['subject', 'difficulty_level', 'is_active', 'created_at']
    search_fields = ['topic_name', 'content', 'keywords']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(InstitutionRecommendation)
class InstitutionRecommendationAdmin(admin.ModelAdmin):
    list_display = ['name', 'priority', 'is_active']
    list_filter = ['priority', 'is_active']
    search_fields = ['name', 'description']
    filter_horizontal = ['recommended_institutions']
    ordering = ['-priority', 'name']