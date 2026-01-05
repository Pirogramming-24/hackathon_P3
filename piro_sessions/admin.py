from django.contrib import admin
from .models import Session, ProgressCheck, Question, Content, Notice

# Register your models here.
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'created_at']
    list_filter = ['date']
    search_fields = ['title']

@admin.register(ProgressCheck)
class ProgressCheckAdmin(admin.ModelAdmin):
    list_display = ['session', 'emotion', 'created_at']
    list_filter = ['session', 'emotion', 'created_at']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['session', 'content_preview', 'answered', 'created_at']
    list_filter = ['session', 'answered', 'created_at']
    search_fields = ['content', 'reply']
    
    def content_preview(self, obj):
        return obj.content[:50]
    content_preview.short_description = '질문 내용'

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['session', 'content_type', 'title', 'created_at']
    list_filter = ['session', 'content_type', 'created_at']
    search_fields = ['title', 'content']

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['session', 'title', 'created_at']
    list_filter = ['session', 'created_at']
    search_fields = ['title', 'content']