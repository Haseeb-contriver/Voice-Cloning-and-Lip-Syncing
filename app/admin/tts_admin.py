from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django import forms
from app.models import TextToSpeech
from pydub import AudioSegment
import os, requests

# def generate_tts(text):
#     API_URL = "https://api-inference.huggingface.co/models/facebook/fastspeech2-en-ljspeech"
#     headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
#     response = requests.post(API_URL, headers=headers, json={"inputs": text})
#     filename = f"tts_audio/output_{hash(text)}.mp3"
#     full_path = os.path.join("media", filename)

#     os.makedirs(os.path.dirname(full_path), exist_ok=True)
#     with open(full_path, "wb") as f:
#         f.write(response.content)
#     return filename

from pydub import AudioSegment
import os, requests

def generate_tts(text):
    API_URL = "https://api-inference.huggingface.co/models/facebook/fastspeech2-en-ljspeech"
    headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": text})

    # Save temporary wav file
    wav_filename = f"tts_audio/temp_{hash(text)}.wav"
    wav_full_path = os.path.join("media", wav_filename)
    os.makedirs(os.path.dirname(wav_full_path), exist_ok=True)
    with open(wav_full_path, "wb") as f:
        f.write(response.content)

    # Convert to MP3
    mp3_filename = f"tts_audio/output_{hash(text)}.mp3"
    mp3_full_path = os.path.join("media", mp3_filename)
    sound = AudioSegment.from_wav(wav_full_path)
    sound.export(mp3_full_path, format="mp3")

    # Remove temp wav
    os.remove(wav_full_path)

    return mp3_filename


class TTSForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 60}))

@admin.register(TextToSpeech)
class TextToSpeechAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("generate/", self.admin_site.admin_view(self.generate_view), name="tts_generate"),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):   # ✅ list ki jagah apna form show karega
        return self.generate_view(request)

    def generate_view(self, request):
        form = TTSForm(request.POST or None)
        context = dict(
            self.admin_site.each_context(request),
            form=form,
            title="Text to Speech"
        )
        if request.method == "POST" and form.is_valid():
            text = form.cleaned_data["text"]
            file_path = generate_tts(text)
            obj = TextToSpeech.objects.create(text=text, audio_file=file_path)
            context["success"] = f"Audio generated and saved as {file_path}"
        return TemplateResponse(request, "admin/tts_page.html", context)
