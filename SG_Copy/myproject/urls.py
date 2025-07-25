"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
    # 여기에서 accounts 앱의 URL들을 포함시킴
    path('api/', include('SG_account.accounts.urls')), # <-- 이게 있어야 /api/login/ 으로 연결됨

    path('', include('SG_account.accounts.urls')),
    path('mypage/', include('SG_mypage.urls')),
    path('account/', include('SG_account.accounts.urls')),   # 기존 account 앱도 include
]

# 미디어 파일 설정 (이미지 업로드용)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
