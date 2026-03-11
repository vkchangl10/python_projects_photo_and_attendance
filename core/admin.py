from django.contrib import admin
from .models import User, Meeting, APIKey


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'url_code', 'created_by', 'created_at')
    list_filter = ('created_by',)
    search_fields = ('title', 'url_code', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        """Set the created_by field to the current user if creating new meeting"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_by', 'created_at', 'last_used')
    list_filter = ('is_active', 'created_by')
    search_fields = ('name', 'key', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('key', 'created_at', 'updated_at', 'last_used')
    
    def save_model(self, request, obj, form, change):
        """Set the created_by field to the current user if creating new API key"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
