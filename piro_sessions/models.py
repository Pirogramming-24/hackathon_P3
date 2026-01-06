from django.db import models

# Create your models here.
class Session(models.Model):
    """세션 기본 정보"""
    title = models.CharField(max_length=100, verbose_name="세션 제목")
    date = models.DateField(verbose_name="세션 날짜")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    
    class Meta:
        ordering = ['date']
        verbose_name = "세션"
        verbose_name_plural = "세션 목록"
    
    def __str__(self):
        return f"{self.title} ({self.date})"