from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 로그인 및 토큰 발급
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # 토큰 갱신
]
