# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        WebSocket 연결 시 호출됨.
        URL에서 room_name 추출 후, 같은 방 사용자들과 메시지 공유를 위한 그룹에 자신을 추가.
        그리고 연결을 승인한다.
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # 그룹에 채널 추가 (메시지 브로드캐스팅 대상이 됨)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # 클라이언트 연결 승인
        await self.accept()

    async def disconnect(self, close_code):
        """
        WebSocket 연결 해제 시 호출.
        그룹에서 채널 제거.
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        클라이언트로부터 메시지를 수신할 때마다 호출됨.
        메시지(JSON 문자열)를 파싱하여 DB에 저장 후, 같은 방의 모든 클라이언트에 메시지 브로드캐스트.
        """
        # 디버깅용 로그 — 누가 어떤 메시지를 보냈는지 출력
        print(f"📩 Receive called. User: {self.scope['user']}, Data: {text_data}")

        data = json.loads(text_data)
        message = data.get('message', '')

        # 현재 연결된 사용자 정보
        user = self.scope["user"]

        # 익명 사용자는 메시지 처리 없이 연결 종료
        if user.is_anonymous:
            print("🚫 익명 사용자는 메시지를 보낼 수 없습니다. 연결 종료.")
            await self.close()
            return

        username = user.username if user.is_authenticated else "anonymous"

        # 메시지 DB 저장 전 로그 출력
        print(f"💾 Saving message from user_id={user.id} in room={self.room_name}: {message}")

        # DB에 메시지 저장 (비동기 호출, 내부에서 동기 DB 접근)
        await self.save_message(user.id, self.room_name, message)

        # 그룹에 메시지 브로드캐스트 (해당 그룹 내 모든 클라이언트에게 메시지 전달)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',   # 그룹 이벤트 핸들러 호출 명칭
                'message': message,
                'user': username,
            }
        )

    async def chat_message(self, event):
        """
        그룹에서 보낸 메시지를 수신하여 클라이언트(WebSocket)로 전송.
        """
        message = event['message']
        user = event['user']

        # JSON 포맷으로 메시지 전송
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))

    @database_sync_to_async
    def save_message(self, user_id, room_name, message):
        """
        데이터베이스에 메시지를 저장하는 동기 함수를 비동기 방식으로 감싸서 사용.
        models는 함수 내에서 임포트하여 앱 초기화 문제 방지.
        room_name은 실제로는 ChatRoom의 id(정수)임을 유념.
        """
        from .models import ChatRoom, Message
        from django.contrib.auth import get_user_model
        User = get_user_model()

        try:
            # room_name을 정수로 변환 가능해야 함
            room_id = int(room_name)
            room = ChatRoom.objects.get(id=room_id)
            user = User.objects.get(id=user_id)
        except (ValueError, ChatRoom.DoesNotExist, User.DoesNotExist) as e:
            print(f"⚠️ save_message 에러: {e}")
            # 예외 발생 시 None 반환하여 무시 가능
            return None

        # 메시지 DB에 저장
        return Message.objects.create(sender=user, room=room, content=message)
