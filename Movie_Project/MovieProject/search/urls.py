from django.urls import path
from . import views

# URL 패턴 리스트
urlpatterns = [
    # 루트 경로에 search_movie 뷰 연결
    path('', views.search_movie, name='search_movie'),
]
