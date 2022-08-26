from django.db import models

# Create your models here.
class ContentFilter(models.Model):
    videoId = models.CharField(max_length=15, default="")


class VideoCache:
    def __init__(self,search_query,videos):
        self.search_query = search_query
        self.videos = videos

class CustomVideo(models.Model):
    video = models.FileField(upload_to='custom_videos/')

