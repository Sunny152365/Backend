from django.contrib.auth.models import AbstractUser
from django.db import models

# 기본 User 모델을 확장하고 싶을 때 사용 (옵션)
class User(AbstractUser):
    # 예: 추가 프로필 필드 가능
    phone_number = models.CharField(max_length=20, blank=True, null=True)
