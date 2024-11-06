import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 데이터 로드
df = pd.read_csv('repositories_preprocessed.csv')

# 2. 언어별 레포지토리 수 계산
language_counts = df['language'].value_counts()

# 3. 상위 10개 언어 선택 및 데이터 필터링
top_languages = language_counts.head(10).index.tolist()
df_top_languages = df[df['language'].isin(top_languages)]

print("상위 10개 언어:")
print(top_languages)

# 4. 언어별 평균 스타 수 계산
language_stars_mean = df_top_languages.groupby('language')['stargazers_count'].mean().sort_values(ascending=False)
print("\n언어별 평균 스타 수:")
print(language_stars_mean)

# 5. 언어별 중앙값 스타 수 계산
language_stars_median = df_top_languages.groupby('language')['stargazers_count'].median().sort_values(ascending=False)
print("\n언어별 중앙값 스타 수:")
print(language_stars_median)

# 6. 언어별 평균 스타 수 막대 그래프
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))
sns.barplot(x=language_stars_mean.values, y=language_stars_mean.index, palette='viridis')
plt.title('Compare the average number of stars by language')
plt.xlabel('Average number of stars')
plt.ylabel('programming language')
plt.show()

# 7. 언어별 중앙값 스타 수 막대 그래프
plt.figure(figsize=(12, 8))
sns.barplot(x=language_stars_median.values, y=language_stars_median.index, palette='coolwarm')
plt.title('Compare the average number of stars by language')
plt.xlabel('median number of stars')
plt.ylabel('programming language')
plt.show()

# 8. 언어별 스타 수 분포 박스플롯
data_to_plot = []

for language in top_languages:
    data = df_top_languages[df_top_languages['language'] == language]['stargazers_count']
    data_to_plot.append(data)

plt.figure(figsize=(12, 8))
sns.boxplot(data=data_to_plot)
plt.xticks(range(len(top_languages)), top_languages, rotation=45)
plt.title('Compare the average number of stars by language')
plt.xlabel('programming language')
plt.ylabel('number of stars')
plt.show()

# 9. 언어별 평균 인기 지표 비교
language_metrics_mean = df_top_languages.groupby('language')[['stargazers_count', 'forks_count', 'watchers_count']].mean()

print("\n언어별 평균 인기 지표:")
print(language_metrics_mean)

# 10. 언어별 평균 인기 지표 막대 그래프
language_metrics_mean.plot(kind='bar', figsize=(14, 8))
plt.title('Compare the average number of stars by language')
plt.xlabel('programming language')
plt.ylabel('average value')
plt.xticks(rotation=45)
plt.show()
