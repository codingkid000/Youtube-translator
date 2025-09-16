# from django.shortcuts import render
# from .forms import VideoForm
# from .models import Video
# import whisperx
# import yt_dlp
# import requests
# import os

# # ---------------------------
# # Helper Functions
# # ---------------------------

# def download_audio(youtube_url):
#     """
#     Download audio from YouTube URL and convert to WAV format.
#     """
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'wav',
#             'preferredquality': '192',
#         }],
#         'outtmpl': 'audio.%(ext)s',  # safer, avoids hardcoding filename
#         'quiet': True,
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(youtube_url, download=True)
#         filename = ydl.prepare_filename(info)
#         # Force .wav extension
#         audio_path = os.path.splitext(filename)[0] + ".wav"
#     return audio_path


# def transcribe_audio(audio_file_path):
#     """
#     Transcribe audio using WhisperX on CPU with FP32.
#     """
#     model = whisperx.load_model("base", device="cpu", compute_type="float32")
#     result = model.transcribe(audio_file_path)

#     # Safely join transcript
#     transcript = " ".join(
#         [segment.get("text", "") for segment in result.get("segments", [])]
#     ).strip()
#     return transcript


# def translate_text(text, target_language='en'):
#     """
#     Translate text using LibreTranslate API.
#     """
#     url = 'https://libretranslate.com/translate'
#     payload = {
#         'q': text,
#         'source': 'en',   # adjust if needed
#         'target': target_language,
#         'format': 'text'
#     }
#     try:
#         response = requests.post(url, data=payload, timeout=30)
#         response.raise_for_status()
#         result = response.json()
#         return result.get('translatedText', text)
#     except Exception as e:
#         print(f"Translation error: {e}")
#         return text


# def generate_mind_map(transcript):
#     """
#     Generate a simple mind map from transcript.
#     """
#     lines = transcript.split('.')
#     return {'Transcript Summary': [line.strip() for line in lines if line.strip()]}


# # ---------------------------
# # Main View
# # ---------------------------

# def index(request):
#     if request.method == 'POST':
#         form = VideoForm(request.POST)
#         if form.is_valid():
#             video = form.save(commit=False)

#             # Step 1: Download audio from YouTube
#             audio_path = download_audio(video.youtube_url)

#             # Step 2: Transcribe audio
#             video.transcript = transcribe_audio(audio_path)

#             # Step 3: Translate transcript
#             video.translated_text = translate_text(video.transcript, 'en')

#             # Save video record
#             video.save()

#             # Step 4: Delete temporary audio file
#             if os.path.exists(audio_path):
#                 os.remove(audio_path)

#             # Step 5: Generate mind map
#             mind_map = generate_mind_map(video.transcript)

#             return render(request, 'result.html', {
#                 'video': video,
#                 'mind_map': mind_map
#             })
#     else:
#         form = VideoForm()

#     return render(request, 'index.html', {'form': form})







from django.shortcuts import render
from .forms import VideoForm
from .models import Video
import whisperx
import yt_dlp
import os
from googletrans import Translator

# ---------------------------
# Helper Functions
# ---------------------------

def download_audio(youtube_url):
    """
    Download audio from YouTube URL and convert to WAV format.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio.%(ext)s',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info)
        audio_path = os.path.splitext(filename)[0] + ".wav"
    return audio_path


def transcribe_audio(audio_file_path):
    """
    Transcribe audio using WhisperX on CPU with FP32.
    """
    model = whisperx.load_model("base", device="cpu", compute_type="float32")
    result = model.transcribe(audio_file_path)

    transcript = " ".join(
        [segment.get("text", "") for segment in result.get("segments", [])]
    ).strip()
    return transcript


def translate_text(text, target_language='en'):
    """
    Translate text using Google Translate.
    """
    translator = Translator()
    try:
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        print(f"Translation error ({target_language}): {e}")
        return text


def generate_mind_map(text):
    """
    Generate a simple mind map from given text.
    """
    lines = text.split('.')
    return [line.strip() for line in lines if line.strip()]


# ---------------------------
# Main View
# ---------------------------

def index(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)

            # Step 1: Download audio
            audio_path = download_audio(video.youtube_url)

            # Step 2: Transcribe
            video.transcript = transcribe_audio(audio_path)

            # Step 3: Translate into multiple languages
            languages = {
                'English': 'en',
                'Tamil': 'ta',
                'Hindi': 'hi',
                'French': 'fr',
                'Spanish': 'es',
                'German': 'de',
            }

            translations = {}
            mind_maps = {}
            for lang_name, lang_code in languages.items():
                translated_text = translate_text(video.transcript, lang_code)
                translations[lang_name] = translated_text
                mind_maps[lang_name] = generate_mind_map(translated_text)

            # Save only English in DB
            video.translated_text = translations['English']
            video.save()

            # Step 4: Cleanup
            if os.path.exists(audio_path):
                os.remove(audio_path)

            return render(request, 'result.html', {
                'video': video,
                'translations': translations,
                'mind_maps': mind_maps
            })
    else:
        form = VideoForm()

    return render(request, 'index.html', {'form': form})
