"""Migration: Add APIKey model"""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the API Key', max_length=255)),
                ('key', models.CharField(help_text='The API Key value', max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True, help_text='Whether this API key is active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_used', models.DateTimeField(blank=True, help_text='Last time this API key was used', null=True)),
                ('description', models.TextField(blank=True, help_text='Description of this API key')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='api_keys', to='core.user')),
            ],
            options={
                'db_table': 'api_keys',
                'ordering': ['-created_at'],
            },
        ),
    ]
