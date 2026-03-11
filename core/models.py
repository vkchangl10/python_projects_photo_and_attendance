from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets

class User(AbstractUser):
    """Custom user model"""
    bio = models.TextField(blank=True)
    avatar = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'

class Meeting(models.Model):
    """Meeting model"""
    url_code = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'meetings'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class APIKey(models.Model):
    """API Key model for FastAPI authentication"""
    name = models.CharField(max_length=255, help_text="Name of the API Key")
    key = models.CharField(max_length=255, unique=True, help_text="The API Key value")
    is_active = models.BooleanField(default=True, help_text="Whether this API key is active")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='api_keys')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_used = models.DateTimeField(null=True, blank=True, help_text="Last time this API key was used")
    description = models.TextField(blank=True, help_text="Description of this API key")
    
    class Meta:
        db_table = 'api_keys'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.key[:10]}...)"
    
    def save(self, *args, **kwargs):
        """Generate a random key if not provided"""
        if not self.key:
            self.key = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)