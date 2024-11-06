import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import matplotlib.dates as mdates

# 1. 데이터 로드
df = pd.read_csv('repositories_preprocessed.csv')

# 데이터 확인
print("데이터 프레임의 첫 5개 행:")
print(df.head())

# 2. 'create_at' 컬럼의 데이터 타입 및 예시 확인
print("\n'created_at' 컬럼 데이터 타입:", df['created_at'].dtype)
print("\n'created_at' 컬럼 샘플 데이터:")
print(df['created_at'].head(10))

# 3. 'create_at' 컬럼을 datetime 형식으로 변환
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

# 변환 후 데이터 확인
print("\n변환된 'created_at' 컬럼의 일부 데이터:")
print(df['created_at'].head(10))
print("\n변환된 'created_at' 컬럼의 데이터 타입:", df['created_at'].dtype)

# 4. 연도별 레포지토리 수 집계
df['year'] = df['created_at'].dt.year
yearly_counts = df['year'].value_counts().sort_index()

print("\n연도별 신규 레포지토리 수:")
print(yearly_counts)

# 5. 월별 레포지토리 수 집계
df['month'] = df['created_at'].dt.to_period('M')  # Year-Month 형식
monthly_counts = df['month'].value_counts().sort_index()

print("\n월별 신규 레포지토리 수 (최근 12개월):")
print(monthly_counts.tail(12))  # 최근 12개월 예시

# 6. 연도별 시계열 그래프 그리기
plt.figure(figsize=(12, 6))
sns.lineplot(x=yearly_counts.index, y=yearly_counts.values, marker='o', color='blue')
plt.title('Trends in the number of new AI projects by year')
plt.xlabel('year')
plt.ylabel('number of repositories')
plt.xticks(yearly_counts.index)  # 모든 연도에 대해 x축 눈금 설정
plt.grid(True)
plt.tight_layout()
plt.show()