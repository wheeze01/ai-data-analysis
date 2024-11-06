import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 워드클라우드를 생성하기 위한 라이브러리 (워드클라우드 생략 시 필요 없음)
# from wordcloud import WordCloud  # 워드클라우드 사용 시 필요

# 폰트 설정
plt.rcParams['font.family'] = 'Arial'

# 1. 데이터 로드
df = pd.read_csv('repositories_preprocessed.csv')

# 2. 'license' 컬럼에서 라이선스 이름 추출
def extract_license_name(x):
    if pd.isnull(x):
        return 'No License'
    elif isinstance(x, str):
        return x
    else:
        return 'Other'

df['license_name'] = df['license'].apply(extract_license_name)

# 변환 후 확인
print("License 이름 추출 후 데이터 확인:")
print(df[['license', 'license_name']].head(10))

# 3. 라이선스별 레포지토리 수 계산
license_counts = df['license_name'].value_counts()

# 4. 상위 10개 라이선스 선택
top_licenses = license_counts.head(10)
print("상위 10개 라이선스:")
print(top_licenses)

# 5. 막대 그래프 그리기
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))
sns.barplot(x=top_licenses.values, y=top_licenses.index, palette='viridis')
plt.title('Number of repositories per Top 10 licenses')
plt.xlabel('count of repository')
plt.ylabel('license')
plt.tight_layout()
plt.show()

# 6. 파이 차트 그리기 (선택 사항)
plt.figure(figsize=(8, 8))
plt.pie(top_licenses.values, labels=top_licenses.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('viridis', len(top_licenses)))
plt.title('Repository Percentage by Top 10 Licenses')
plt.axis('equal')  # 원형으로 표시
plt.show()

# 7. 워드클라우드 생략 또는 포함
from wordcloud import WordCloud

# # 워드클라우드 생성
font_path = 'C:/Windows/Fonts/Arial.ttf'  # Windows의 경우
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    font_path=font_path,
    max_words=200,
    colormap='viridis'
)
topic_dict = license_counts.to_dict()

if topic_dict:
    wordcloud.generate_from_frequencies(topic_dict)
    
    plt.figure(figsize=(15, 7.5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('license WordCloud')
    plt.show()
else:
    print("워드클라우드를 생성할 라이선스 데이터가 없습니다.")
