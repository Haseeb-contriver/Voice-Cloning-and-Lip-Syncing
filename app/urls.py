from django.urls import path
from app.views import create_project, project_detail, home, speech_cloning

urlpatterns = [
    path("", home, name="home"),
    path("project/new/", create_project, name="create_project"),
    path("project/<int:pk>/", project_detail, name="project_detail"),
    path("speech-cloning/", speech_cloning, name="speech_cloning"),
]
