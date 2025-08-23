from django import forms
from .models import Project, AudioFile, VideoFile

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "script_text"]

class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ["file", "is_sample"]

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoFile
        fields = ["file", "is_avatar"]
