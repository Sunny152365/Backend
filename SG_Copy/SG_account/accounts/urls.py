from django.urls import path
from .views import (
    EmailLoginView,
    KakaoLoginView,
    NaverLoginView,
    NaverCallbackView,
    NaverCallbackSuccessView,
    NaverCallbackErrorView,
    register,
)

urlpatterns = [
    path('login/email/', EmailLoginView.as_view(), name='email-login'),
    path('login/kakao/', KakaoLoginView.as_view(), name='kakao-login'),
    path('login/naver/', NaverLoginView.as_view(), name='naver-login'),
    path('naver/callback/', NaverCallbackView.as_view(), name='naver-callback'),
    # 성공 처리 URL 추가
    path('api/naver/callback/success/', NaverCallbackSuccessView.as_view()),
    path('api/naver/callback/error/', NaverCallbackErrorView.as_view()),
    path('register/', register, name='register'),
]

