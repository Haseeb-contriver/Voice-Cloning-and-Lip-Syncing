# app/views.py
from django.shortcuts import render
from django.http import HttpResponse

def speech_cloning(request):
    if request.method == "POST":
        text = request.POST.get("text")
        # Yahan pe aap apna TTS / cloning ka code call karoge
        return HttpResponse(f"Audio generated for: {text}")
    return render(request, "speech_cloning.html")
