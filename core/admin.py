from django.contrib import admin
from .models import User, Meeting

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'url_code', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'url_code')