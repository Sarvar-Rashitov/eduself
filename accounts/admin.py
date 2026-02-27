from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PasswordResetToken, LoginHistory, Level, Badge, UserBadge, LivesSettings
from django.utils.html import format_html


@admin.register(LivesSettings)
class LivesSettingsAdmin(admin.ModelAdmin):
    list_display = ['daily_lives', 'max_lives', 'refill_time_minutes', 'lives_cost_on_fail', 'passing_score', 'is_active']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Asosiy sozlamalar', {
            'fields': ('daily_lives', 'max_lives', 'is_active'),
            'description': 'Kunlik va maksimal yurakchalar soni'
        }),
        ('Tiklanish sozlamalari', {
            'fields': ('refill_time_minutes',),
            'description': 'Yurakcha tiklanish vaqti (daqiqalarda)'
        }),
        ('Test sozlamalari', {
            'fields': ('lives_cost_on_fail', 'passing_score'),
            'description': 'Muvaffaqiyatsizlikda yo\'qotish va o\'tish foizi'
        }),
    )
    
    def has_add_permission(self, request):
        # Faqat bitta yozuv bo'lishi mumkin
        return not LivesSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False  # O'chirib bo'lmaydi


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['level_number', 'name', 'required_xp', 'color_preview', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['level_number']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'level_number', 'required_xp', 'description')
        }),
        ('Vizual', {
            'fields': ('icon', 'color')
        }),
        ('Holat', {
            'fields': ('is_active',)
        }),
    )
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 30px; height: 30px; background-color: {}; border-radius: 5px; border: 1px solid #ddd;"></div>',
            obj.color
        )
    color_preview.short_description = 'Rang'


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'badge_type', 'image_preview', 'requirement_info', 'is_active', 'order']
    list_filter = ['badge_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['order', 'id']
    list_editable = ['is_active', 'order']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'description', 'badge_type', 'image', 'order')
        }),
        ('Level Badge uchun', {
            'fields': ('required_level',),
            'classes': ('collapse',),
        }),
        ('Streak Badge uchun', {
            'fields': ('required_streak_days',),
            'classes': ('collapse',),
        }),
        ('Achievement Badge uchun', {
            'fields': ('required_xp', 'required_tests_passed'),
            'classes': ('collapse',),
        }),
        ('Holat', {
            'fields': ('is_active',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: contain;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Rasm'
    
    def requirement_info(self, obj):
        if obj.badge_type == 'level' and obj.required_level:
            return f"Level {obj.required_level.level_number} ({obj.required_level.required_xp} XP)"
        elif obj.badge_type == 'streak' and obj.required_streak_days:
            return f"{obj.required_streak_days} kun streak"
        elif obj.badge_type == 'achievement':
            parts = []
            if obj.required_xp:
                parts.append(f"{obj.required_xp} XP")
            if obj.required_tests_passed:
                parts.append(f"{obj.required_tests_passed} test")
            return " va ".join(parts) if parts else "-"
        return "-"
    requirement_info.short_description = 'Talab'


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'unlocked_at']
    list_filter = ['badge__badge_type', 'unlocked_at']
    search_fields = ['user__username', 'user__email', 'badge__name']
    ordering = ['-unlocked_at']
    readonly_fields = ['unlocked_at']
    
    def has_add_permission(self, request):
        return True  # Admin qo'lda ham badge berishi mumkin


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone', 'total_points', 'current_lives', 'streak_days', 'is_active', 'is_staff', 'created_at']
    list_filter = ['is_active', 'is_staff', 'auth_provider', 'email_verified', 'created_at']
    search_fields = ['username', 'email', 'phone', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Shaxsiy ma\'lumotlar', {'fields': ('phone', 'bio', 'profile_image', 'avatar_number')}),
        ('Gamification', {'fields': ('total_points', 'streak_days', 'last_active_date', 'level')}),
        ('Lives/Hearts', {'fields': ('current_lives', 'last_life_lost_at', 'last_daily_reset')}),
        ('Ijtimoiy tarmoqlar', {'fields': ('auth_provider', 'google_id', 'telegram_id', 'telegram_username', 'telegram_chat_id')}),
        ('Email tasdiqlash', {'fields': ('email_verified',)}),
        ('Til', {'fields': ('language',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Qo\'shimcha', {'fields': ('email', 'phone', 'bio', 'profile_image')}),
    )
    readonly_fields = ['google_id', 'telegram_id', 'created_at', 'updated_at']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'used']
    list_filter = ['used', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['token', 'created_at']


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_type', 'browser', 'os', 'ip_address', 'is_new_device', 'login_time']
    list_filter = ['is_new_device', 'device_type', 'browser', 'os', 'login_time']
    search_fields = ['user__username', 'user__email', 'ip_address']
    readonly_fields = ['user', 'ip_address', 'user_agent', 'device_type', 'browser', 'os', 'location', 'is_new_device', 'login_time']
    ordering = ['-login_time']
    
    def has_add_permission(self, request):
        return False  # Faqat avtomatik yaratiladi
    
    def has_change_permission(self, request, obj=None):
        return False  # O'zgartirib bo'lmaydi
