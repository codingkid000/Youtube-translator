from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['youtube_url']
        widgets = {
            'youtube_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter YouTube video URL here',
                'style': 'width: 400px;'
            }),
        }
        labels = {
            'youtube_url': 'YouTube Video URL',
        }
