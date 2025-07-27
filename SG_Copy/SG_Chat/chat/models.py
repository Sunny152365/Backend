# chat/models.py
from django.db import models
from django.conf import settings  # ✅ AUTH_USER_MODEL 사용을 위해 필요

class ChatRoom(models.Model):
    # ✅ 사용자(User)는 settings.AUTH_USER_MODEL로 참조
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.id}"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ 읽음 처리용 ManyToMany 필드도 동일하게 변경
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='read_messages', blank=True)

    def __str__(self):
        return f"{self.sender} → Room {self.room.id}: {self.content[:20]}"
    
# ChatRoom
# 1:1 또는 단체 채팅방. 참여자는 ManyToMany로 연결됨.
# Message
# 메시지는 채팅방에 속하고, 보낸 사람과 내용을 가짐.
# 관리자, 고수, 의뢰인 3 종류의 사용자 모두 메시지를 보낼 수 있음.