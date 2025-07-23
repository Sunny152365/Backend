from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # 커스텀 사용자 모델을 쓸 수도 있으므로 이렇게 가져옴

# [1] 고수가 제공하는 서비스 카테고리 (예: 청소, 인테리어, 이사 등)
class Category(models.Model):
    name = models.CharField(max_length=100)  # 카테고리 이름

    def __str__(self):
        return self.name


# [2] 전문가(고수) 모델
class Expert(models.Model):
    name = models.CharField(max_length=100)         # 전문가 이름
    description = models.TextField(blank=True)      # 소개글

    category = models.ForeignKey(                   # 제공 서비스 카테고리
        Category,
        on_delete=models.CASCADE,
        related_name='experts'
    )

    latitude = models.FloatField()                  # 위도
    longitude = models.FloatField()                 # 경도

    rating = models.FloatField(default=0.0)         # 평균 별점
    review_count = models.IntegerField(default=0)   # 리뷰 수
    hire_count = models.IntegerField(default=0)     # 고용 횟수

    experience_years = models.IntegerField(default=0)  # 경력 (년 단위)

    def __str__(self):
        return self.name


# [3] 리뷰 모델
class Review(models.Model):
    expert = models.ForeignKey(
        Expert,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(  # 작성자 (로그인 사용자)
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer_name = models.CharField(max_length=100)  # 작성자 표시 이름
    rating = models.FloatField()                      # 별점 (0.0 ~ 5.0)
    comment = models.TextField(blank=True)            # 후기 내용
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer_name} - {self.expert.name} ({self.rating})"

    class Meta:
        ordering = ['-created_at']
