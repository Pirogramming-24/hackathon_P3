from django.db import models
from piro_sessions.models import Session

# Create your models here.
class Question(models.Model):
    """질문"""
    session = models.ForeignKey(
        Session, 
        on_delete=models.CASCADE, 
        related_name='questions',
        verbose_name="세션"
    )
    content = models.TextField(verbose_name="질문 내용")
    answered = models.BooleanField(default=False, verbose_name="답변 완료")
    reply = models.TextField(blank=True, null=True, verbose_name="답변")
    image = models.ImageField(
        upload_to='questions/', 
        blank=True, 
        null=True,
        verbose_name="첨부 이미지"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "질문"
        verbose_name_plural = "질문 목록"
    
    def __str__(self):
        return f"Q: {self.content[:50]}"