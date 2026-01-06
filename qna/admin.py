from django.contrib import admin
from .models import Question

# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['session', 'content_preview', 'answered', 'created_at']
    list_filter = ['session', 'answered', 'created_at']
    search_fields = ['content', 'reply']
    
    def content_preview(self, obj):
        return obj.content[:50]
    content_preview.short_description = '질문 내용'