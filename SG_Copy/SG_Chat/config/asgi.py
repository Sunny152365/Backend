# config/asgi.py
"""
ASGI config for config project.

This exposes the ASGI callable as a module-level variable named `application`.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing  # 채팅 앱의 라우팅을 임포트

# Django 환경변수 설정 (settings.py 모듈 위치)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Django ASGI 애플리케이션 생성 (HTTP 요청 처리를 위한 기본 앱)
django_asgi_app = get_asgi_application()

# ProtocolTypeRouter를 사용해 HTTP 요청과 WebSocket 요청을 구분해서 처리
application = ProtocolTypeRouter({
    # HTTP 요청은 기존 Django 애플리케이션이 처리
    "http": django_asgi_app,

    # WebSocket 요청은 Channels의 인증 미들웨어와 URL 라우터가 처리
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns  # chat 앱 내 WebSocket 경로 매핑
        )
    ),
})
