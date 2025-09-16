from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('youtube_url', 'created_at')
    readonly_fields = ('transcript', 'translated_text', 'created_at')
