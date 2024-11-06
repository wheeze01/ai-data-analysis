import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 데이터 로드
df = pd.read_csv('repositories_preprocessed.csv')

# 'Unknown'이 아닌 언어만 선택
df_known_languages = df[df['language'] != 'Unknown']

# 2. 프로그래밍 언어 분포 계산
language_counts = df_known_languages['language'].value_counts()

# 3. 상위 20개 언어 선택 및 출력
top_languages = language_counts.head(20)
print("Top 20 Programming Languages:")
print(top_languages)

# 4. 막대 그래프 그리기
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))
sns.barplot(x=top_languages.values, y=top_languages.index, palette='viridis')
plt.title('Top 20 Programming Languages in AI Projects')
plt.xlabel('Number of Repositories')
plt.ylabel('Programming Language')
plt.show()

# 5. 파이 차트 그리기
top_languages_pie = language_counts.head(10)
plt.figure(figsize=(8, 8))
plt.pie(top_languages_pie.values, labels=top_languages_pie.index, autopct='%1.1f%%', startangle=140)
plt.title('Top 10 Programming Languages Distribution')
plt.axis('equal')
plt.show()

# 6. 언어별 평균 스타 수 계산 및 그래프 그리기
language_stars = df.groupby('language')['stargazers_count'].mean().sort_values(ascending=False)
top_language_stars = language_stars.head(10)
print("\nTop 10 Languages by Average Stars:")
print(top_language_stars)

plt.figure(figsize=(12, 8))
sns.barplot(x=top_language_stars.values, y=top_language_stars.index, palette='coolwarm')
plt.title('Top 10 Languages by Average Stars')
plt.xlabel('Average Number of Stars')
plt.ylabel('Programming Language')
plt.show()
