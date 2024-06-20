from django.db import models

# Create your models here.
LANGUAGE_SHORT_CODE = [
    ('en', 'English'),
    ('bn', 'Bangla'),
    ('hi', 'Hindi'),
    ('fr', 'French'),
    ('es', 'Spanish'),
    ('zh-CN', 'Chinese'),
    ('ar', 'Arabic'),
    ('de', 'German'),
    ('it', 'Italian'),
    ('ja', 'Japanese'),
    ('pk', 'Pakistani'),
]

class VideoUpload(models.Model):
    title = models.CharField(max_length=100, null=True, unique=True)
    files = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class VideoDecode(models.Model):
    short_code = models.CharField(max_length=20, choices=LANGUAGE_SHORT_CODE)
    original_text = models.TextField(null=True, blank=True)
    converted_text = models.TextField(null=True, blank=True)
    video_file = models.ForeignKey(VideoUpload, on_delete=models.CASCADE, related_name='decodes')

    def __str__(self):
        return f"{self.video_file.title} converted to {self.short_code}"
