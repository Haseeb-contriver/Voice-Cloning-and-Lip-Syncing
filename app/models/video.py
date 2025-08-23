from django.db import models
from .project import Project

class VideoFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="videos")
    file = models.FileField(upload_to="video/")
    is_avatar = models.BooleanField(default=False)  # True = uploaded avatar, False = lip-synced output
    created_at = models.DateTimeField(auto_now_add=True)
