from django.db import models
from piro_sessions.models import Session

# Create your models here.
class Content(models.Model):
    """콘텐츠"""
    CONTENT_TYPES = [
        ('link', '링크'),
        ('file', '파일'),
        ('image', '이미지'),
        ('text', '텍스트'),
    ]
    
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='contents',
        verbose_name="세션"
    )
    content_type = models.CharField(
        max_length=10, 
        choices=CONTENT_TYPES,
        verbose_name="타입"
    )
    title = models.CharField(max_length=200, blank=True, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    file = models.FileField(
        upload_to='contents/', 
        blank=True, 
        null=True,
        verbose_name="파일"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "콘텐츠"
        verbose_name_plural = "콘텐츠 목록"
    
    def __str__(self):
        return f"{self.get_content_type_display()}: {self.title or self.content[:30]}"


class ProgressBox(models.Model):
    """진도 체크 박스"""
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='progress_boxes',
        verbose_name="세션"
    )
    content = models.CharField(max_length=200, verbose_name="진도 내용")
    order = models.IntegerField(default=0, verbose_name="순서")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "진도 박스"
        verbose_name_plural = "진도 박스 목록"
    
    def __str__(self):
        return f"{self.session.title} - {self.content}"
    
    def get_stats(self):
        """통계 계산"""
        happy = self.checks.filter(emotion='happy').count()
        sad = self.checks.filter(emotion='sad').count()
        return {'happy': happy, 'sad': sad}


class ProgressCheck(models.Model):
    """진도 체크"""
    EMOTION_CHOICES = [
        ('happy', '😊'),
        ('sad', '😢'),
    ]
    
    progress_box = models.ForeignKey(
        ProgressBox,
        on_delete=models.CASCADE,
        related_name='checks',
        verbose_name="진도 박스"
    )
    user_id = models.CharField(max_length=100, verbose_name="사용자 ID")
    emotion = models.CharField(max_length=10, choices=EMOTION_CHOICES, verbose_name="감정")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")
    
    class Meta:
        unique_together = ['progress_box', 'user_id']
        verbose_name = "진도 체크"
        verbose_name_plural = "진도 체크 목록"
    
    def __str__(self):
        return f"{self.progress_box.content} - {self.user_id}"