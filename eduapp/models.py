from django.db import models

# Create your models here.
class ContentFilter(models.Model):
    videoId = models.CharField(max_length=15, default="")
