from django.contrib import admin
from .models import Content, ProgressBox, ProgressCheck

# Register your models here.
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['session', 'content_type', 'title', 'created_at']
    list_filter = ['session', 'content_type']

@admin.register(ProgressBox)
class ProgressBoxAdmin(admin.ModelAdmin):
    list_display = ['session', 'content', 'order', 'created_at']

@admin.register(ProgressCheck)
class ProgressCheckAdmin(admin.ModelAdmin):
    list_display = ['progress_box', 'user_id', 'emotion', 'created_at']