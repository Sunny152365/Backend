# chat/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

# ws/chat/<room_id>/로 연결되도록 설정
# <room_name>은  실제로는 room.id로 사용할 예정 (설계를 그렇게 함)