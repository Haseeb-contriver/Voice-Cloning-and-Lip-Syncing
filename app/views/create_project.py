from django.shortcuts import render, redirect, get_object_or_404
from app.models import Project
from app.forms import ProjectForm, AudioUploadForm, VideoUploadForm

def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect("project_detail", pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, "core/create_project.html", {"form": form})