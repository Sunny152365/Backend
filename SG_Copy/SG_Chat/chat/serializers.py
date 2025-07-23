from rest_framework import serializers
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'content', 'created_at']

class ChatRoomSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    lastMessage = serializers.SerializerMethodField()
    lastMessageTime = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'participants', 'messages', 'created_at', 'lastMessage', 'lastMessageTime']

    def get_lastMessage(self, obj):
        last_msg = obj.messages.last()
        return last_msg.content if last_msg else None

    def get_lastMessageTime(self, obj):
        last_msg = obj.messages.last()
        return last_msg.created_at.isoformat() if last_msg else None


# UserSerializer
# 유저 ID, 이름만 노출
# MessageSerializer
# 메시지 내용 + 보낸 유저 정보
# ChatRoomSerializer
# 채팅방 정보 + 참여자 목록 + 메시지들