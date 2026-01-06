from django.db import models
from piro_sessions.models import Session

# Create your models here.
class Notice(models.Model):
    """공지사항"""
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='notices',
        verbose_name="세션"
    )
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    file = models.FileField(
        upload_to='notices/',
        blank=True,
        null=True,
        verbose_name="파일"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "공지사항"
        verbose_name_plural = "공지사항 목록"
    
    def __str__(self):
        return self.title