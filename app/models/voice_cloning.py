from django.db import models


class ClonedVoice(models.Model):
    PROVIDERS = (
    ("elevenlabs", "ElevenLabs"),
    ("coqui", "Coqui XTTS"),
    )


    name = models.CharField(max_length=100)
    provider = models.CharField(max_length=20, choices=PROVIDERS)
    sample_audio = models.FileField(upload_to="voice_samples/", blank=True, null=True)
    external_voice_id = models.CharField(max_length=100, blank=True, null=True) # e.g., ElevenLabs voice_id
    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return f"{self.name} ({self.get_provider_display()})"