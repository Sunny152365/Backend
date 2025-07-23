from django.contrib import admin
from .models import Category, Expert, Review  # Review 모델도 임포트

# [1] 카테고리 관리자 설정
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']  # 목록에 id와 이름 표시
    search_fields = ['name']       # 이름으로 검색 가능

# [2] 전문가 관리자 설정
@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'category', 'rating', 'review_count', 'hire_count'
    ]                             # 주요 필드 목록에 표시
    list_filter = ['category']    # 오른쪽 필터 메뉴: 카테고리별 필터링
    search_fields = ['name', 'description']  # 이름과 설명으로 검색 가능
    ordering = ['-rating', '-review_count']  # 별점과 리뷰 수 내림차순 정렬
    list_per_page = 20            # 페이지당 20개씩 표시

# [3] 후기 관리자 설정
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'expert', 'reviewer_name', 'rating', 'created_at'
    ]                             # 후기 리스트에 표시될 필드
    list_filter = ['rating', 'created_at']  # 별점과 작성일 필터
    search_fields = ['reviewer_name', 'comment']  # 리뷰어 이름과 내용 검색 가능
    ordering = ['-created_at']    # 최신 후기부터 정렬
    list_per_page = 30            # 페이지당 30개 표시
