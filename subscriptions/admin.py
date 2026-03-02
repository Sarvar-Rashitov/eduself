from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import (
    SubscriptionPlan, UserSubscription, PromoCode, 
    ReferralProgram, UserReferral, ReferralProgress,
    Payment, Donation
)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration_days', 'is_popular', 'is_active', 'order']
    list_filter = ['is_active', 'is_popular']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'price']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'slug', 'description', 'price', 'duration_days')
        }),
        ('Cheklovlar', {
            'fields': (
                'unlimited_lives',
                'ai_analysis_limit',
                'ai_companion_limit',
                'university_exam_limit',
                'mock_exam_limit',
                'certificate_test_limit'
            )
        }),
        ('Ko\'rinish', {
            'fields': ('icon', 'color', 'badge_text', 'is_popular')
        }),
        ('Holat', {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'start_date', 'end_date', 'acquired_via', 'is_active_display']
    list_filter = ['status', 'acquired_via', 'is_trial', 'plan']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Foydalanuvchi va Ta\'rif', {
            'fields': ('user', 'plan')
        }),
        ('Muddat', {
            'fields': ('start_date', 'end_date', 'status', 'is_trial')
        }),
        ('Qanday olingan', {
            'fields': ('acquired_via',)
        }),
        ('Foydalanish statistikasi', {
            'fields': (
                'ai_analysis_used',
                'ai_companion_used',
                'university_exam_used',
                'mock_exam_used',
                'certificate_test_used'
            )
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def is_active_display(self, obj):
        if obj.is_active():
            return format_html('<span style="color: green;">✓ Faol</span>')
        return format_html('<span style="color: red;">✗ Faol emas</span>')
    is_active_display.short_description = 'Holat'
    
    actions = ['activate_subscriptions', 'expire_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        count = queryset.update(status='active')
        self.message_user(request, f'{count} ta obuna faollashtirildi.')
    activate_subscriptions.short_description = 'Tanlangan obunalarni faollashtirish'
    
    def expire_subscriptions(self, request, queryset):
        count = queryset.update(status='expired')
        self.message_user(request, f'{count} ta obuna muddati tugadi deb belgilandi.')
    expire_subscriptions.short_description = 'Tanlangan obunalar muddatini tugash'


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'plan', 'discount_display', 'valid_from', 'valid_until', 'usage_display', 'is_active']
    list_filter = ['is_active', 'plan']
    search_fields = ['code']
    date_hierarchy = 'created_at'
    readonly_fields = ['current_uses', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Promokod', {
            'fields': ('code', 'plan')
        }),
        ('Chegirma', {
            'fields': ('discount_percent', 'discount_amount')
        }),
        ('Muddat', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('Cheklovlar', {
            'fields': ('max_uses', 'current_uses')
        }),
        ('Holat', {
            'fields': ('is_active',)
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def discount_display(self, obj):
        if obj.discount_percent > 0:
            return f"{obj.discount_percent}%"
        if obj.discount_amount > 0:
            return f"{obj.discount_amount} so'm"
        return "Chegirma yo'q"
    discount_display.short_description = 'Chegirma'
    
    def usage_display(self, obj):
        if obj.max_uses == 0:
            return f"{obj.current_uses} / Cheksiz"
        return f"{obj.current_uses} / {obj.max_uses}"
    usage_display.short_description = 'Foydalanish'


@admin.register(ReferralProgram)
class ReferralProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan', 'required_referrals', 'referral_deadline_days', 'reward_duration_days', 'is_active']
    list_filter = ['is_active', 'plan']
    search_fields = ['name']
    
    fieldsets = (
        ('Dastur', {
            'fields': ('name', 'plan')
        }),
        ('Shartlar', {
            'fields': ('required_referrals', 'referral_deadline_days')
        }),
        ('Mukofot', {
            'fields': ('reward_duration_days',)
        }),
        ('Holat', {
            'fields': ('is_active',)
        }),
    )


@admin.register(UserReferral)
class UserReferralAdmin(admin.ModelAdmin):
    list_display = ['referrer', 'referred', 'program', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'program']
    search_fields = ['referrer__username', 'referred__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']


@admin.register(ReferralProgress)
class ReferralProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'program', 'referral_count', 'progress_display', 'deadline', 'is_completed', 'reward_given']
    list_filter = ['is_completed', 'reward_given', 'program']
    search_fields = ['user__username', 'user__email']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    def progress_display(self, obj):
        percentage = (obj.referral_count / obj.program.required_referrals) * 100
        color = 'green' if obj.is_completed else 'orange'
        return format_html(
            '<span style="color: {};">{} / {} ({}%)</span>',
            color,
            obj.referral_count,
            obj.program.required_referrals,
            int(percentage)
        )
    progress_display.short_description = 'Jarayon'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'payment_method', 'final_amount', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'plan']
    search_fields = ['user__username', 'user__email', 'transaction_id']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    
    fieldsets = (
        ('Foydalanuvchi va Ta\'rif', {
            'fields': ('user', 'subscription', 'plan')
        }),
        ('To\'lov ma\'lumotlari', {
            'fields': ('payment_method', 'amount', 'discount_amount', 'final_amount')
        }),
        ('Promokod', {
            'fields': ('promo_code',)
        }),
        ('Holat', {
            'fields': ('status', 'transaction_id')
        }),
        ('Qo\'shimcha', {
            'fields': ('payment_data',)
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method']
    search_fields = ['user__username', 'user__email', 'transaction_id']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'completed_at']
    
    fieldsets = (
        ('Foydalanuvchi', {
            'fields': ('user', 'amount', 'message')
        }),
        ('To\'lov', {
            'fields': ('payment_method', 'status', 'transaction_id')
        }),
        ('Qo\'shimcha', {
            'fields': ('payment_data',)
        }),
        ('Vaqt', {
            'fields': ('created_at', 'completed_at')
        }),
    )
