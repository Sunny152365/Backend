from django.urls import path
from .views import NearbyExpertListView, ExpertByCategoryView, ReviewListView

urlpatterns = [
    # 위치 기반 전문가 리스트 조회 (lat, lng, radius 쿼리 파라미터)
    path('nearby/', NearbyExpertListView.as_view(), name='nearby_experts'),

    # 카테고리별 전문가 리스트 조회 (category_id 또는 category, 페이징 지원)
    path('by-category/', ExpertByCategoryView.as_view(), name='experts_by_category'),

    # 특정 전문가의 리뷰 리스트 조회 (expert_id URL 파라미터)
    path('reviews/<int:expert_id>/', ReviewListView.as_view(), name='expert_reviews'),
]
