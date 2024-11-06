import pandas as pd
import numpy as np
import json
import re

# 1. JSON 파일 로드
with open('repositories.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. 데이터프레임 생성
df = pd.DataFrame(data)

# 3. 필요한 컬럼 선택
needed_columns = [
    'id', 'name', 'full_name', 'html_url', 'description',
    'created_at', 'updated_at', 'pushed_at',
    'stargazers_count', 'watchers_count', 'forks_count',
    'language', 'topics', 'license', 'owner', 'languages', 'dependencies'
]
df = df[needed_columns]

# 4. 날짜 컬럼 타입 변환
date_columns = ['created_at', 'updated_at', 'pushed_at']
for col in date_columns:
    df[col] = pd.to_datetime(df[col])

# 5. 결측치 처리
df['description'] = df['description'].fillna('')
df['language'] = df['language'].fillna('Unknown')
df['license'] = df['license'].fillna('No License')

# 수정된 부분: x가 리스트인지 확인하여 처리
df['topics'] = df['topics'].apply(lambda x: x if isinstance(x, list) else [])
df['dependencies'] = df['dependencies'].apply(lambda x: x if isinstance(x, dict) else {})

# owner 컬럼의 결측치 처리
df = df.dropna(subset=['owner'])

# 6. 중복 데이터 제거
df = df.drop_duplicates(subset='id')

# 7. Owner 정보 펼치기
owner_df = pd.json_normalize(df['owner'])
owner_df.rename(columns={
    'login': 'owner_login',
    'html_url': 'owner_html_url',
    'type': 'owner_type'
}, inplace=True)
df = pd.concat([df.drop(columns=['owner']), owner_df], axis=1)

# 8. Topics 컬럼 처리
df['topics_str'] = df['topics'].apply(lambda x: ','.join(x) if isinstance(x, list) else '')

# 9. Dependencies 컬럼 처리
def extract_python_libraries(dependencies):
    libs = set()
    for file_name, content in dependencies.items():
        if file_name == 'requirements.txt':
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    lib_name = re.split('==|>=|<=|>|<', line)[0]
                    libs.add(lib_name)
    return list(libs)

df['python_libraries'] = df['dependencies'].apply(extract_python_libraries)

# 10. 수치 데이터 로그 변환
df['stargazers_count_log'] = np.log1p(df['stargazers_count'])
df['forks_count_log'] = np.log1p(df['forks_count'])

# 11. 전처리된 데이터 저장
df.to_csv('repositories_preprocessed.csv', index=False)
df.to_pickle('repositories_preprocessed.pkl')

# 12. 데이터 확인
print(df.head())
print(df.info())
