# GitHub AI 프로젝트 데이터 수집기

이 프로젝트는 GitHub API를 활용하여 AI 관련 오픈소스 프로젝트의 데이터를 수집하는 파이썬 스크립트입니다. 레포지토리를 검색하고, 각 레포지토리의 메타데이터, 언어 사용량, 의존성 파일 등을 수집하여 분석에 활용할 수 있도록 합니다.

## 📝 소개

AI 분야의 오픈소스 프로젝트를 분석하여 언어 사용 빈도, 라이브러리 의존성, 코드 복잡도 등을 파악하고자 할 때, 대량의 데이터를 효율적으로 수집하는 것은 매우 중요합니다. 이 스크립트는 GitHub API를 통해 자동으로 데이터를 수집하여 이러한 분석을 용이하게 해줍니다.

## 🎯 주요 기능

- **레포지토리 검색**: `machine learning`, `deep learning`, `artificial intelligence` 키워드를 사용하여 인기 있는 레포지토리를 검색합니다.
- **메타데이터 수집**: 레포지토리의 이름, 설명, 생성일, 별(star) 개수 등 주요 정보를 수집합니다.
- **언어 정보 수집**: 각 레포지토리에서 사용된 프로그래밍 언어와 사용량을 수집합니다.
- **의존성 파일 수집**: 주요 언어에 따라 해당 레포지토리의 의존성 파일(예: `requirements.txt`, `package.json` 등)을 수집합니다.
- **API 요청 관리**: GitHub API의 Rate Limit을 고려하여 요청 횟수를 관리하고, 요청 간 딜레이를 추가하여 안정적인 수집을 보장합니다.

## 📋 요구 사항

- Python 3.6 이상
- `requests` 라이브러리
- GitHub Personal Access Token (개인 액세스 토큰)

## 🛠 설치 방법

1. **리포지토리 클론**

   ```bash
   git clone https://github.com/yourusername/github-ai-data-collector.git
   cd github-ai-data-collector
   ```

2. **필요한 라이브러리 설치**

   ```bash
   pip install requests
   ```

3. **GitHub Personal Access Token 생성**

   - GitHub 계정에서 **Settings > Developer settings > Personal access tokens**로 이동합니다.
   - **Generate new token**을 클릭하고 토큰을 생성합니다.
   - 토큰 생성 시 **repo** 권한이 필요하지 않으므로 기본 설정으로 생성하면 됩니다.

4. **환경 변수 설정**

   - 생성한 토큰을 환경 변수 `GITHUB_TOKEN`에 설정합니다.

     **Windows (CMD):**

     ```cmd
     set GITHUB_TOKEN=your_personal_access_token_here
     ```

     **macOS/Linux (bash):**

     ```bash
     export GITHUB_TOKEN='your_personal_access_token_here'
     ```

## 🚀 사용 방법

1. **스크립트 실행**

   ```bash
   python data_collection.py
   ```

2. **결과 확인**

   - 스크립트 실행이 완료되면 현재 디렉토리에 `repositories.json` 파일이 생성됩니다.
   - 이 파일에는 수집된 레포지토리의 모든 데이터가 JSON 형식으로 저장됩니다.

## 📂 코드 구조 설명

### `data_collection.py`

이 스크립트는 데이터 수집을 위한 메인 파일입니다.

#### 주요 구성 요소

- **라이브러리 임포트**

  ```python
  import requests
  import os
  import time
  import json
  import base64
  from urllib.parse import quote
  ```

- **환경 변수에서 GitHub 토큰 가져오기**

  ```python
  GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
  ```

- **헤더 설정**

  ```python
  headers = {
      'Authorization': f'token {GITHUB_TOKEN}',
      'Accept': 'application/vnd.github.v3+json',
  }
  ```

- **검색 키워드 및 설정**

  ```python
  keywords = ['machine learning', 'deep learning', 'artificial intelligence']
  NUM_REPOS = 1000  # 수집할 레포지토리 수
  ```

- **의존성 파일 매핑**

  ```python
  dependency_files = {
      'Python': ['requirements.txt', 'Pipfile', 'setup.py'],
      'JavaScript': ['package.json', 'yarn.lock'],
      # 기타 언어 매핑...
  }
  ```

- **레포지토리 검색 및 데이터 수집 루프**

  ```python
  for keyword in keywords:
      # 검색 및 페이지네이션 처리
      # 각 레포지토리에 대해:
          # 메타데이터 수집
          # 언어 정보 수집
          # 주요 언어 확인 및 의존성 파일 수집
          # 요청 간 딜레이 추가
  ```

- **API 요청 횟수 관리 및 Rate Limit 처리**

  ```python
  total_requests += 1  # 요청 횟수 증가
  time.sleep(0.5)      # 요청 간 딜레이
  ```

- **데이터 저장**

  ```python
  with open('repositories.json', 'w', encoding='utf-8') as f:
      json.dump(repositories, f, ensure_ascii=False, indent=4)
  ```

## ⚠️ 주의 사항

- **GitHub API Rate Limit**: 인증된 요청의 경우 시간당 5,000회의 제한이 있습니다. 요청 횟수를 모니터링하고 딜레이를 추가하여 제한에 걸리지 않도록 주의하세요.
- **Secondary Rate Limit**: 갑작스러운 대량의 요청은 추가적인 제한에 걸릴 수 있으므로, 요청 간 딜레이(`time.sleep(0.5)`)를 유지하세요.
- **라이선스 준수**: 수집한 데이터와 코드의 사용은 GitHub의 이용 약관과 각 레포지토리의 라이선스를 준수해야 합니다.
- **개인정보 보호**: 레포지토리의 공개 데이터만 수집하며, 개인정보나 민감한 정보를 처리하지 않도록 주의하세요.
- **토큰 보안**: Personal Access Token은 절대로 공개 저장소나 코드에 직접 포함시키지 마세요. 환경 변수를 사용하여 안전하게 관리하세요.

## 📊 데이터 분석 예시

수집된 `repositories.json` 파일을 활용하여 다양한 분석을 수행할 수 있습니다.

- **언어 사용 빈도 분석**

  ```python
  import json
  import pandas as pd
  import matplotlib.pyplot as plt

  with open('repositories.json', 'r', encoding='utf-8') as f:
      data = json.load(f)

  df = pd.DataFrame(data)
  language_counts = df['language'].value_counts()

  language_counts.plot(kind='bar')
  plt.title('언어별 레포지토리 수')
  plt.xlabel('언어')
  plt.ylabel('레포지토리 수')
  plt.show()
  ```

- **라이브러리 의존성 분석**

  ```python
  # 각 레포지토리의 의존성 파일에서 라이브러리 목록 추출 및 빈도 분석
  ```

- **코드 복잡도 분석**

  - 레포지토리의 소스 코드를 클론하여 `radon` 등의 도구를 사용하여 코드 복잡도를 측정할 수 있습니다.

## 🤝 기여 방법

1. 이 리포지토리를 포크하세요.
2. 기능을 추가하거나 버그를 수정한 후 커밋하세요.
3. 변경 사항을 푸시하고 Pull Request를 생성하세요.

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.

## 📧 문의

프로젝트와 관련된 질문이나 제안 사항이 있으시면 아래의 이메일로 연락해주세요.

- 이메일: your.email@example.com

---

이 README는 프로젝트의 전반적인 개요와 사용 방법을 제공하며, 코드를 실행하고 데이터를 수집하는 데 필요한 모든 정보를 담고 있습니다. 프로젝트를 진행하시면서 추가적인 도움이 필요하시다면 언제든지 문의해주세요.