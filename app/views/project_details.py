from django.shortcuts import render, redirect, get_object_or_404
from app.models import Project
from app.forms import ProjectForm, AudioUploadForm, VideoUploadForm

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    audio_form = AudioUploadForm()
    video_form = VideoUploadForm()
    return render(request, "core/project_detail.html", {
        "project": project,
        "audio_form": audio_form,
        "video_form": video_form
    })