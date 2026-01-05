from django.db import models

# Create your models here.
class Contents(models.Model):
    # 1. 구분: 진도체크용인가 일반 콘텐츠용인가
    is_progress = models.BooleanField(default=False, help_text="진도체크 영역으로 보낼지 여부")
    
    # 2. 내용 구성
    text = models.TextField() # 내용 또는 진도 상세 설명
    file = models.FileField(upload_to='contents/files/', null=True, blank=True)
    image = models.ImageField(upload_to='contents/images/', null=True, blank=True)
    
    # 3. 메타 정보
    is_active = models.BooleanField(default=True) # 현재 활성화된 진도인지 확인

    #4 is_progress가 true면 앞에 진도가 붙고 아니면 일반이 붙음
    def __str__(self):
        prefix = "[진도]" if self.is_progress else "[일반]"
        return f"{prefix} {self.text}"

class Feedback(models.Model):
    # 어떤 콘텐츠(특히 진도)에 대한 피드백인지 연결
    session_id = models.ForeignKey(Session, )

    
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='feedbacks')
    session_key = models.CharField(max_length=40, db_index=True)
    reaction = models.CharField(max_length=10, choices=[('GOOD', '좋아요'), ('BAD', '싫어요')])
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('content', 'session_key')