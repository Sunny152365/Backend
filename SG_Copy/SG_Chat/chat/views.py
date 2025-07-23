from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny


User = get_user_model()

class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # 채팅방 생성 시 자동으로 본인을 참여자로 추가
        room = serializer.save()
        room.participants.add(self.request.user)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        # 특정 채팅방 참가
        room = self.get_object()
        room.participants.add(request.user)
        return Response({'status': 'joined'})

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        # 특정 채팅방의 메시지 목록 조회 (GET /chatrooms/<id>/messages/)
        room = self.get_object()
        messages = Message.objects.filter(room=room).order_by('created_at')

        # 읽지 않은 메시지에 대해 read_by에 사용자 추가
        for message in messages:
            if request.user.is_authenticated and request.user not in message.read_by.all():
                message.read_by.add(request.user)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]  # 추후 IsAuthenticated로 변경 가능

    def perform_create(self, serializer):
        # 메시지 전송 시 자동으로 sender를 요청 사용자로 설정
        serializer.save(sender=self.request.user)

    def list(self, request, *args, **kwargs):
        # 쿼리 파라미터로 room ID를 받아 해당 방 메시지 리스트 조회
        room_id = request.query_params.get('room')
        if not room_id:
            return Response({"error": "room ID is required."}, status=400)

        messages = Message.objects.filter(room_id=room_id).order_by('created_at')

        # 읽지 않은 메시지에 대해 read_by에 사용자 추가
        for message in messages:
            if request.user.is_authenticated and request.user not in message.read_by.all():
                message.read_by.add(request.user)

        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)


from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the chat server!")


# ChatRoomViewSet
# 채팅방 조회 / 생성 / 참가 기능 (POST /chatrooms/<id>/join/)
# MessageViewSet
# 메시지 전송 / 조회 (자동으로 sender 설정)