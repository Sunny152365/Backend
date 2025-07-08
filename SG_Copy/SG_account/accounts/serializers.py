from rest_framework import serializers
from django.contrib.auth import authenticate

class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise serializers.ValidationError("이메일 또는 비밀번호가 올바르지 않습니다.")
            data['user'] = user
            return data
        else:
            raise serializers.ValidationError("이메일과 비밀번호가 모두 필요합니다.")
