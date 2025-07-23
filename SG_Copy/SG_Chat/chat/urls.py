from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'chatrooms', ChatRoomViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('chatrooms/<int:chatroom_id>/messages/', ChatRoomMessagesView.as_view(), name='chatroom-messages'),
]

# WebSocket은 asgi.py에서 따로 관리하고, REST API는 urls.py에서 관리하니까 구분해서 생각하자.