from django.db import models
from .project import Project

class AudioFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="audios")
    file = models.FileField(upload_to="audio/")
    is_sample = models.BooleanField(default=False)  # True = uploaded sample, False = generated TTS/cloned
    created_at = models.DateTimeField(auto_now_add=True)
