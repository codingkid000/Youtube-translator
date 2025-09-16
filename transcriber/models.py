from django.db import models

class Video(models.Model):
    youtube_url = models.URLField(verbose_name="YouTube Video URL")
    transcript = models.TextField(blank=True, null=True, verbose_name="Transcription")
    translated_text = models.TextField(blank=True, null=True, verbose_name="Translated Text")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return self.youtube_url
