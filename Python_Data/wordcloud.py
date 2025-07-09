from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 분석할 텍스트 데이터
text = "시간은 흐르고, 마음은 멀어진다. 그러나 기억은 늘 그 자리에 있다."

# 워드클라우드 생성
wordcloud = WordCloud(
    font_path='NanumGothic.ttf',  # 한글 폰트 경로
    background_color='white',
    width=800,
    height=400
).generate(text)

# 출력
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
