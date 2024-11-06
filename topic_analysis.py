import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import matplotlib.font_manager as fm

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Arial'  # Windows의 경우

# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

# 1. 데이터 로드
df = pd.read_csv('repositories_preprocessed.csv')

# 2. 'topics' 컬럼을 리스트로 변환
def parse_topics(x):
    if pd.isnull(x):
        return []
    try:
        return ast.literal_eval(x)
    except (ValueError, SyntaxError):
        return []

df['topics'] = df['topics'].apply(parse_topics)

# 3. 토픽 데이터를 개별 행으로 펼치기
all_topics = df.explode('topics')

# 4. 토픽 시리즈 생성 및 결측치 제거
topics_series = all_topics['topics'].dropna()

# 5. 토픽 빈도수 계산
topic_counts = topics_series.value_counts()

# 6. 상위 20개 토픽 선택
top_topics = topic_counts.head(20)
print("상위 20개 토픽:")
print(top_topics)

# 7. 막대 그래프 그리기
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))
sns.barplot(x=top_topics.values, y=top_topics.index, palette='viridis')
plt.title('Top 20 topic frequency')
plt.xlabel('repository count')
plt.ylabel('topic')
plt.tight_layout()
plt.show()

# 워드클라우드를 생성하기 위한 라이브러리
from wordcloud import WordCloud

# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

font_path = 'C:/Windows/Fonts/Arial.ttf'  # Windows의 경우

# 워드클라우드 생성
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    font_path=font_path,
    max_words=200,
    colormap='viridis'
)

# 토픽 빈도수 딕셔너리 생성
topic_dict = topic_counts.to_dict()

# 워드클라우드 생성
if topic_dict:
    wordcloud.generate_from_frequencies(topic_dict)
    
    # 워드클라우드 시각화
    plt.figure(figsize=(15, 7.5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('토픽 워드클라우드')
    plt.show()
else:
    print("워드클라우드를 생성할 토픽 데이터가 없습니다.")