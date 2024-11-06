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

# 2. 'python_libraries' 컬럼을 리스트로 변환
def parse_libraries(x):
    if pd.isnull(x):
        return []
    try:
        return ast.literal_eval(x) if isinstance(x, str) else x
    except (ValueError, SyntaxError):
        return []

df['python_libraries'] = df['python_libraries'].apply(parse_libraries)

# 변환 후 확인
print("변환된 'python_libraries' 컬럼의 일부 데이터:")
print(df['python_libraries'].head(10))
print("Data type after parsing:", df['python_libraries'].apply(type).unique())

# 3. 'python_libraries' 컬럼을 개별 행으로 펼치기
all_libraries = df.explode('python_libraries')

# 4. 라이브러리 시리즈 생성 및 결측치 제거
libraries_series = all_libraries['python_libraries'].dropna()

# 5. 라이브러리 빈도수 계산
library_counts = libraries_series.value_counts()

# 6. 상위 20개 라이브러리 선택
top_libraries = library_counts.head(20)
print("상위 20개 라이브러리:")
print(top_libraries)

# 7. 막대 그래프 그리기
sns.set(style="whitegrid")
plt.figure(figsize=(12, 10))
sns.barplot(x=top_libraries.values, y=top_libraries.index, palette='viridis')
plt.title('Number of top 20 Python libraries used')
plt.xlabel('frequency')
plt.ylabel('libraries')
plt.tight_layout()
plt.show()

# 8. 파이 차트 그리기 (선택 사항)
plt.figure(figsize=(10, 10))
plt.pie(top_libraries.values, labels=top_libraries.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('viridis', len(top_libraries)))
plt.title('Number of top 20 Python libraries used')
plt.axis('equal')  # 원형으로 표시
plt.show()