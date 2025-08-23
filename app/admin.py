from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.template.response import TemplateResponse

class TTSAdminView(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("tts/", self.admin_site.admin_view(self.tts_view), name="tts_page"),
        ]
        return custom_urls + urls

# koi model register karna zaroori nahi, ye sirf page add karega
