def __str__(self):
    return str(self.email or self.kakao_user_id or self.naver_user_id or "Anonymous User")

