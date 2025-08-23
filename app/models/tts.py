from django.db import models

class TextToSpeech(models.Model):
    text = models.TextField("Text Input")
    audio_file = models.FileField(upload_to="tts_audio/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TTS #{self.id} - {self.text[:30]}"
