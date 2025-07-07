from django.db import models
from django.contrib.auth.models import User  # 로그인 기능 시 필요

class SearchHistory(models.Model):
    """
    사용자의 검색 기록을 저장하는 모델
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # 로그인 연결용, 선택적
    keyword = models.CharField(max_length=100)
    category = models.CharField(max_length=10)  # 'news' 또는 'blog'
    search_time = models.DateTimeField(auto_now_add=True)
    crawl_duration = models.FloatField(help_text="크롤링 소요 시간 (초)")

    def __str__(self):
        return f"{self.keyword} ({self.category}) at {self.search_time}"

class TopKeyword(models.Model):
    """
    각 검색 기록에 연결된 상위 키워드 정보 저장 모델
    """
    search_history = models.ForeignKey('SearchHistory', on_delete=models.CASCADE, related_name='top_keywords')
    # 'SearchHistory' (문자열로 참조), SearchHistory (직접 클래스 참조) 보통 모델이 정의되기 전에 참조할 때 쓰고, 같은 파일 안에서 이미 선언된 클래스면 직접 참조, 문자열이 조금 더 유연
    word = models.CharField(max_length=50)
    frequency = models.IntegerField()

    def __str__(self):
        return f"{self.word} ({self.frequency})"
