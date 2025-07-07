"""
URL configuration for miniproject_wordcloud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 관리자 페이지 (기본: /admin/)
    path('admin/', admin.site.urls),

    # analyzer 앱 내 URL 연결, 기본 루트 경로로 연결
    path('', include('analyzer.urls')),

    # Django 내장 인증 시스템 URL (로그인, 로그아웃 등)
   path('accounts/login/', auth_views.LoginView.as_view(template_name='analyzer/login.html'), name='login'),
]

# 개발 환경에서 정적 파일과 미디어 파일 직접 서빙
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
