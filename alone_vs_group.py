import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import matplotlib as mpl
import os

# 1. 한글 폰트 설정
font_path = 'C:/Windows/Fonts/NanumGothic.ttf'  # Windows
# font_path = '/Library/Fonts/NanumGothic.ttf'  # macOS
# font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'  # Linux

# 폰트 프로퍼티 생성
font_prop = fm.FontProperties(fname=font_path)

# matplotlib의 기본 폰트 설정
plt.rcParams['font.family'] = font_prop.get_name()

# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

# 2. matplotlib 폰트 캐시 삭제
cache_dir = mpl.get_cachedir()
print("matplotlib 캐시 디렉토리:", cache_dir)

font_cache_files = [f for f in os.listdir(cache_dir) if f.startswith('fontList')]
for f in font_cache_files:
    os.remove(os.path.join(cache_dir, f))

print("matplotlib 폰트 캐시를 삭제했습니다.")

# Python 세션을 재시작한 후 실행하세요.

# 3. 데이터 로드
df = pd.read_csv('repositories_preprocessed.csv')

# 4. 데이터프레임의 컬럼 목록 확인
print("데이터프레임의 컬럼 목록:")
print(df.columns)

# 5. 'owner_type' 컬럼이 존재하는지 확인하고, 데이터 확인
if 'owner_type' not in df.columns:
    print("\nError: 'owner_type' 컬럼이 데이터프레임에 존재하지 않습니다. 컬럼 이름을 다시 확인해주세요.")
else:
    print("\n'owner_type' 컬럼 데이터 타입:", df['owner_type'].dtype)
    print("\n'owner_type' 컬럼 샘플 데이터:")
    print(df['owner_type'].head(10))
    
    # 6. 결측치 확인 및 처리
    missing_owner_type = df['owner_type'].isna().sum()
    print("\n'owner_type' 컬럼의 결측치 개수:", missing_owner_type)
    
    # 결측치를 'Unknown'으로 대체
    df['owner_type'] = df['owner_type'].fillna('Unknown')
    
    # 'User'와 'Organization' 외의 다른 값이 있는지 확인
    unique_owner_types = df['owner_type'].unique()
    print("\n'unique_owner_types':", unique_owner_types)
    
    # 'User'와 'Organization' 외의 값을 'Other'로 대체
    df['owner_type'] = df['owner_type'].apply(lambda x: x if x in ['User', 'Organization'] else 'Other')
    
    # 'User'와 'Organization'의 비율 계산
    owner_counts = df['owner_type'].value_counts()
    owner_percentage = df['owner_type'].value_counts(normalize=True) * 100
    
    print("\n'owner_type' 비율:")
    print(owner_percentage)
    
    # 7. 막대 그래프 그리기
    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 6))
    sns.barplot(x=owner_counts.values, y=owner_counts.index, palette='viridis')
    plt.title('개인 vs 조직 소유자 비율', fontproperties=font_prop, fontsize=16)
    plt.xlabel('레포지토리 수', fontproperties=font_prop, fontsize=14)
    plt.ylabel('소유자 유형', fontproperties=font_prop, fontsize=14)
    plt.tight_layout()
    plt.show()
    
    # 8. 파이 차트 그리기
    plt.figure(figsize=(8, 8))
    plt.pie(owner_counts.values, labels=owner_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('viridis', len(owner_counts)))
    plt.title('개인 vs 조직 소유자 비율', fontproperties=font_prop, fontsize=16)
    plt.axis('equal')  # 원형으로 표시
    plt.show()
