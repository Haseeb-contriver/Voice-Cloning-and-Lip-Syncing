from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=255)
    script_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
