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