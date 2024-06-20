import os
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from googletrans import Translator

from django.contrib import admin
from . models import VideoDecode, VideoUpload

# Register your models here.
@admin.register(VideoUpload)
class VideoUploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

@admin.register(VideoDecode)
class VideoDecodeAdmin(admin.ModelAdmin):
    list_display = ('video_file', 'short_code', 'original_text', 'converted_text')
    fields = ('video_file', 'short_code')

    def save_model(self, request, obj, form, change):
        video_upload_instance = obj.video_file
        video_path = video_upload_instance.files.path
        
        original_text = transcribe_video(video_path)
        if original_text:
            obj.original_text = original_text
            obj.converted_text = translate_text(original_text, obj.short_code)

        super().save_model(request, obj, form, change)



def transcribe_video(video_path):
    recognizer = sr.Recognizer()
    audio_path = 'temp_audio.wav'

    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')
    except Exception as e:
        print("Error extracting audio:", e)
        return None
    
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

def translate_text(text, target_language):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text