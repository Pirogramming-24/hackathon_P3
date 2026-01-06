from django.db import models

# Create your models here.
class Device(models.Model):
    # 장고 세션에서 생성되는 고유 키값 (익명 사용자 이름표)
    device_key = models.CharField(max_length=40, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Device: {self.device_key[:8]}"