import requests
import os
import time
import json
import base64
from urllib.parse import quote

# 환경 변수에서 GitHub Personal Access Token 가져오기
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise Exception("GITHUB_TOKEN 환경 변수가 설정되어 있지 않습니다. Personal Access Token을 환경 변수로 설정해주세요.")

# 헤더에 토큰 추가
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
}

# 검색할 키워드 목록
keywords = ['machine learning', 'deep learning', 'artificial intelligence']

# 수집할 레포지토리 수
NUM_REPOS = 1000  # 원하는 레포지토리 수 설정

# 결과를 저장할 리스트
repositories = []

# 요청 횟수를 카운트하기 위한 변수
total_requests = 0

# 언어별 의존성 파일 매핑
dependency_files = {
    'Python': ['requirements.txt', 'Pipfile', 'setup.py'],
    'Jupyter Notebook': ['requirements.txt', 'Pipfile', 'setup.py'],
    'JavaScript': ['package.json', 'yarn.lock'],
    'TypeScript': ['package.json', 'yarn.lock'],
    'Java': ['pom.xml', 'build.gradle', 'build.gradle.kts'],
    'C#': ['packages.config', '*.csproj'],
    'C++': ['CMakeLists.txt'],
    'Ruby': ['Gemfile', 'Gemfile.lock'],
    'Go': ['go.mod', 'go.sum'],
    'PHP': ['composer.json', 'composer.lock'],
    'Rust': ['Cargo.toml', 'Cargo.lock'],
    'Swift': ['Package.swift'],
    'Kotlin': ['build.gradle', 'build.gradle.kts'],
    'R': ['DESCRIPTION'],
    'Shell': ['requirements.txt', 'package.json'],  # 스크립트 언어의 경우
}

# GitHub API 검색 URL
search_url = 'https://api.github.com/search/repositories'

# 각 키워드에 대해 검색 수행
for keyword in keywords:
    print(f"\n키워드 '{keyword}'로 레포지토리 검색 중...")

    # 페이지 번호 초기화
    page = 1
    while len(repositories) < NUM_REPOS:
        params = {
            'q': f'{keyword} in:name,description,readme',
            'sort': 'stars',
            'order': 'desc',
            'per_page': 30,
            'page': page
        }

        response = requests.get(search_url, headers=headers, params=params)
        total_requests += 1  # 요청 횟수 증가

        # Rate Limit 초과 시 대기
        if response.status_code == 403:
            if 'X-RateLimit-Remaining' in response.headers and response.headers['X-RateLimit-Remaining'] == '0':
                reset_time = int(response.headers.get('X-RateLimit-Reset'))
                sleep_time = reset_time - int(time.time()) + 5  # 5초 여유를 두고 대기
                print(f"Rate Limit에 도달하여 {sleep_time}초 동안 대기합니다.")
                time.sleep(max(sleep_time, 0))
                continue
            else:
                print("403 오류 발생: 접근이 금지되었습니다.")
                break

        elif response.status_code != 200:
            print(f"에러 발생: {response.status_code}")
            print(response.text)
            break

        data = response.json()
        items = data.get('items', [])

        if not items:
            print("더 이상 결과가 없습니다.")
            break

        for item in items:
            # 레포지토리 메타데이터 수집
            repo_data = {
                'id': item['id'],
                'name': item['name'],
                'full_name': item['full_name'],
                'html_url': item['html_url'],
                'description': item['description'],
                'created_at': item['created_at'],
                'updated_at': item['updated_at'],
                'pushed_at': item['pushed_at'],
                'stargazers_count': item['stargazers_count'],
                'watchers_count': item['watchers_count'],
                'forks_count': item['forks_count'],
                'language': item['language'],
                'topics': item.get('topics', []),
                'license': item['license']['name'] if item['license'] else None,
                'owner': {
                    'login': item['owner']['login'],
                    'html_url': item['owner']['html_url'],
                    'type': item['owner']['type'],
                },
                'languages': {},
                'dependencies': {},
            }

            owner = item['owner']['login']
            repo_name = item['name']

            # 레포지토리별 추가 요청: 언어 정보 수집
            languages_url = f"https://api.github.com/repos/{owner}/{repo_name}/languages"
            languages_response = requests.get(languages_url, headers=headers)
            total_requests += 1  # 요청 횟수 증가

            if languages_response.status_code == 200:
                languages_data = languages_response.json()
                repo_data['languages'] = languages_data
            else:
                repo_data['languages'] = {}
                print(f"언어 정보 수집 실패: {languages_response.status_code}")

            # 주요 언어 확인
            main_language = item['language']
            if not main_language:
                main_language = 'Unknown'

            # 의존성 파일 목록 결정
            dependency_file_list = dependency_files.get(main_language, [])

            # 의존성 파일 수집
            repo_data['dependencies'] = {}
            for dep_file in dependency_file_list:
                # 파일 경로 인코딩
                dep_file_encoded = quote(dep_file)
                contents_url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{dep_file_encoded}"
                contents_response = requests.get(contents_url, headers=headers)
                total_requests += 1  # 요청 횟수 증가

                if contents_response.status_code == 200:
                    contents_data = contents_response.json()

                    # 여러 파일이 반환되는 경우(예: 와일드카드 사용)
                    if isinstance(contents_data, list):
                        for file_info in contents_data:
                            if file_info['type'] == 'file':
                                file_name = file_info['name']
                                file_download_url = file_info['download_url']
                                file_response = requests.get(file_download_url, headers=headers)
                                total_requests += 1  # 요청 횟수 증가

                                if file_response.status_code == 200:
                                    content = file_response.text
                                    repo_data['dependencies'][file_name] = content
                                else:
                                    print(f"{file_name} 다운로드 실패: {file_response.status_code}")
                    else:
                        if contents_data['type'] == 'file':
                            # 파일 내용은 base64로 인코딩되어 있음
                            content = base64.b64decode(contents_data['content']).decode('utf-8')
                            file_name = contents_data['name']
                            repo_data['dependencies'][file_name] = content
                        else:
                            print(f"{dep_file}은 파일이 아닙니다.")
                elif contents_response.status_code == 404:
                    continue  # 파일이 없는 경우 다음 파일로 넘어감
                else:
                    print(f"{dep_file} 수집 실패: {contents_response.status_code}")

                # 요청 간 딜레이 추가
                time.sleep(0.5)

            repositories.append(repo_data)

            if len(repositories) >= NUM_REPOS:
                break

            # 요청 간 딜레이 추가 (Secondary Rate Limit 방지)
            time.sleep(2)

        print(f"페이지 {page} 처리 완료, 총 수집된 레포지토리 수: {len(repositories)}")
        page += 1

    if len(repositories) >= NUM_REPOS:
        break

# 결과를 JSON 파일로 저장
with open('repositories.json', 'w', encoding='utf-8') as f:
    json.dump(repositories, f, ensure_ascii=False, indent=4)

print(f"\n데이터 수집 완료. 'repositories.json' 파일로 저장되었습니다.")
print(f"총 API 요청 횟수: {total_requests}")