from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django import forms
from django.utils.text import slugify
from app.models import TextToSpeech
import os

# 🔊 Simple TTS (gTTS)
from gtts import gTTS


def generate_tts_simple(text: str, lang: str = "en") -> str:
    """
    Generate MP3 using gTTS and return the relative path under MEDIA_ROOT.
    """
    # ensure media/tts_audio exists
    rel_dir = "tts_audio"
    media_dir = os.path.join("media", rel_dir)
    os.makedirs(media_dir, exist_ok=True)

    # safe file name
    safe_snippet = slugify(text)[:40] or "tts"
    filename = f"output_{safe_snippet}_{abs(hash((text, lang))) % 10**8}.mp3"
    full_path = os.path.join(media_dir, filename)

    # synth + save
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(full_path)

    # return relative path for FileField (relative to MEDIA_ROOT)
    return os.path.join(rel_dir, filename)


class TTSForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5, "cols": 60}),
        label="Text"
    )
    lang = forms.ChoiceField(
        choices=[
            ("en", "English"),
            ("ur", "Urdu"),
            ("hi", "Hindi"),
            ("ar", "Arabic"),
        ],
        initial="en",
        label="Language"
    )


@admin.register(TextToSpeech)
class TextToSpeechAdmin(admin.ModelAdmin):
    """
    Custom admin page that shows a simple TTS form and saves the generated MP3
    into TextToSpeech.audio_file.
    """

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("generate/", self.admin_site.admin_view(self.generate_view), name="tts_generate"),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        # show our custom page instead of the default changelist
        return self.generate_view(request)

    def generate_view(self, request):
        form = TTSForm(request.POST or None)
        context = dict(
            self.admin_site.each_context(request),
            form=form,
            title="Text to Speech (Simple - gTTS)",
        )

        if request.method == "POST" and form.is_valid():
            text = form.cleaned_data["text"].strip()
            lang = form.cleaned_data["lang"]

            if not text:
                context["error"] = "Please enter some text."
                return TemplateResponse(request, "admin/tts_page.html", context)

            try:
                file_path = generate_tts_simple(text, lang)
                TextToSpeech.objects.create(text=text, audio_file=file_path)
                self.message_user(request, f"✅ Audio generated: {file_path}")
                # Post/Redirect/Get to avoid resubmits and URL reverse issues
                return redirect("admin:tts_generate")
            except Exception as e:
                context["error"] = f"❌ TTS failed: {e}"

        return TemplateResponse(request, "admin/tts_page.html", context)
