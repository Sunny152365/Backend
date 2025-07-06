# analyzer/admin.py

from django.contrib import admin
from .models import SearchHistory, TopKeyword

# SearchHistory 모델을 관리자 페이지에 등록하고 관리 옵션 설정
@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    # 관리자 리스트 페이지에서 표시할 필드 목록
    list_display = ('id', 'user', 'keyword', 'category', 'search_time', 'crawl_duration')
    # 필터링 옵션 (카테고리, 검색 시간) 추가
    list_filter = ('category', 'search_time')
    # 검색창에서 검색 가능한 필드 지정 (user 모델의 username 포함)
    search_fields = ('keyword', 'user__username')

# TopKeyword 모델을 관리자 페이지에 등록하고 관리 옵션 설정
@admin.register(TopKeyword)
class TopKeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'search_history', 'word', 'frequency')
    search_fields = ('word', 'search__keyword')  # 검색 기록 키워드로 검색 가능
