# analyzer/urls.py

from django.urls import path
from . import views, auth_views  # auth_views는 새로 만들 auth 관련 뷰 파일


app_name = 'analyzer'  # 네임스페이스 설정 추천

urlpatterns = [
    path('', views.index, name='index'),                                      # 메인 페이지 (검색폼)
    path('crawl/', views.unified_crawl, name='result'),                       # 검색 결과 페이지
    path('download/', views.download_image, name='download_image'),           # 서버 저장 이미지 다운로드
    path('download_direct/', views.download_direct, name='download_direct'),  # 메모리 직접 다운로드
    path('history/', views.history, name='history'),                          # 검색 기록 조회

    # 인증 관련 경로 추가
    path('signup/', auth_views.signup, name='signup'),                        # 회원가입
    path('login/', auth_views.login_view, name='login'),                      # 로그인
    path('logout/', auth_views.logout_view, name='logout'),                   # 로그아웃
]