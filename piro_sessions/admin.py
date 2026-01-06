from django.contrib import admin
from .models import Session

# Register your models here.
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'created_at']
    list_filter = ['date']
    search_fields = ['title']