# monster-dex · 몬스터 도감 서버

CI/CD 수업(13-4 · 13-5)에서 사용하는 실습 저장소입니다.
이 저장소를 직접 clone하지 않고, **Use this template** 으로 내 계정에 저장소를 만든 뒤 사용합니다.

## 시작 방법

1. 이 저장소 화면 오른쪽 위 **Use this template** → **Create a new repository**
2. Repository name `monster-dex`, **Public** 선택 → **Create repository**
3. 내 저장소 화면 → **Code** → **Open with GitHub Desktop** → **Clone**

## 폴더 구성

| 경로 | 내용 | 수정 여부 |
|---|---|---|
| `app.py` | 서버 시작 버전 (바로 실행 · 배포 가능) | 기능을 추가할 때 수정 |
| `data/monsters.json` | 몬스터 8마리 | 데이터 변경 실습에서 수정 |
| `requirements.txt` | 필요한 패키지 목록 | 패키지를 추가할 때 수정 |
| `ops/setup_prod.py` | 운영 서버 준비 (폴더와 빈 가상환경 생성) | 수정 X |
| `ops/run_prod.py` | 운영 서버 실행기 | 수정 X |
| `handouts/monsters.yaml` | 기획팀 데이터(YAML) | 데이터 형식을 YAML로 바꾸는 배포에서 `data/monsters.yaml` 로 복사 |

배포 스크립트(`deploy.py`) · 테스트 파일(`tests/`) · `Jenkinsfile` 은 수업에서 직접 새로 만듭니다.

## 개발 환경 (VS Code 터미널 · 저장소 폴더 위치)

| 작업 | Windows (PowerShell) | macOS |
|---|---|---|
| 가상환경 만들기 | `python -m venv .venv` | `python3 -m venv .venv` |
| 가상환경 켜기 | `.\.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` |
| 패키지 설치 | `python -m pip install -r requirements.txt` | 같음 |
| 개발 서버 실행 | `python app.py` → http://localhost:5001 | 같음 |
| 운영 서버 준비 (1번) | `python ops\setup_prod.py` → `C:\monster\live` | `python ops/setup_prod.py` → `/Users/Shared/monster/live` |
| 운영 실행기 (새 터미널 창, 저장소 폴더로 이동한 뒤) | `python ops\run_prod.py live` | `python3 ops/run_prod.py live` |

## 운영 배포 (운영 터미널)

VS Code 터미널 패널의 **+** 로 새 터미널을 열고, 운영 폴더로 이동한 뒤 대상을 지정해 입력합니다.

| 작업 | Windows (PowerShell) | macOS |
|---|---|---|
| 운영 폴더로 이동 | `cd C:\monster\live` | `cd /Users/Shared/monster/live` |
| 1회차: 저장소 받기 | `git clone 내저장소주소 app` | 같음 |
| 2회차부터: 코드 받기 | `git -C app pull` | 같음 |
| 커밋 확인 | `git -C app log -1 --oneline` | 같음 |
| 운영 서버 파이썬으로 패키지 설치 | `.venv\Scripts\python.exe -m pip install -r app\requirements.txt` | `.venv/bin/python -m pip install -r app/requirements.txt` |
| 재시작 요청 | `Get-Date \| Out-File restart.flag` | `date > restart.flag` |
| 배포 확인 | http://localhost:8001/health | 같음 |
