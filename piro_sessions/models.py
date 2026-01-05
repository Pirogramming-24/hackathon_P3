from django.db import models
from django.utils import timezone

# Create your models here.

class Session(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date']
    
    def __str__(self):
        return f"{self.title} ({self.date})"

class ProgressCheck(models.Model):
    EMOTION_CHOICES = [
        ('happy', '😊'),
        ('sad', '😢'),
    ]
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='progress_checks')
    emotion = models.CharField(max_length=10, choices=EMOTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.session.title} - {self.get_emotion_display()}"

class Question(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='questions')
    content = models.TextField()
    answered = models.BooleanField(default=False)
    reply = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='questions/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Q: {self.content[:50]}"

class Content(models.Model):
    CONTENT_TYPES = [
        ('link', '링크'),
        ('file', '파일'),
        ('image', '이미지'),
        ('text', '텍스트'),
    ]
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='contents')
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    file = models.FileField(upload_to='contents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_content_type_display()}: {self.title or self.content[:30]}"

class Notice(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='notices')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title