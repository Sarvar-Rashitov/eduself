from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PasswordResetToken

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone', 'total_points', 'is_active', 'is_staff', 'created_at']
    list_filter = ['is_active', 'is_staff', 'auth_provider', 'email_verified', 'created_at']
    search_fields = ['username', 'email', 'phone', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Shaxsiy ma\'lumotlar', {'fields': ('phone', 'bio', 'profile_image')}),
        ('Statistika', {'fields': ('total_points',)}),
        ('Ijtimoiy tarmoqlar', {'fields': ('auth_provider', 'google_id', 'telegram_id')}),
        ('Email tasdiqlash', {'fields': ('email_verified',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Qo\'shimcha', {'fields': ('email', 'phone', 'bio', 'profile_image')}),
    )
    readonly_fields = ['total_points', 'google_id', 'telegram_id', 'created_at', 'updated_at']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'used']
    list_filter = ['used', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['token', 'created_at']
