import os
import pathlib
import subprocess
import sys
import time
import urllib.request


def get_prod_root():
    if os.environ.get("PROD_ROOT"):
        return pathlib.Path(os.environ["PROD_ROOT"])
    if os.name == "nt":
        return pathlib.Path("C:/monster/live")
    return pathlib.Path("/Users/Shared/monster/live")


def get_prod_python(root):
    if os.name == "nt":
        return root / ".venv" / "Scripts" / "python.exe"
    return root / ".venv" / "bin" / "python"


def update_code(root):
    print("[1/4] 코드 받기 (git)")
    app_dir = root / "app"
    commit = os.environ.get("GIT_COMMIT", "origin/main")
    subprocess.run(["git", "-C", str(app_dir), "fetch", "-q", "origin"], check=True)
    subprocess.run(["git", "-C", str(app_dir), "checkout", "-q", "--force", commit], check=True)
    subprocess.run(["git", "--no-pager", "-C", str(app_dir), "log", "-1", "--oneline"], check=True)


def install_packages(root):
    print("[2/4] 패키지 설치")
    python = get_prod_python(root)
    requirements = root / "app" / "requirements.txt"
    subprocess.run([str(python), "-m", "pip", "install", "-q", "-r", str(requirements)], check=True)


def request_restart(root):
    print("[3/4] 재시작 요청")
    (root / "restart.flag").write_text(str(time.time()), encoding="utf-8")


def check_health():
    print("[4/4] 헬스 체크")
    for i in range(15):
        try:
            with urllib.request.urlopen("http://localhost:8001/health", timeout=2) as res:
                print("응답:", res.read().decode("utf-8"))
                return
        except Exception:
            print("  응답 대기 중 (" + str(i + 1) + "초)")
            time.sleep(1)
    print("헬스 체크 실패: 15초 동안 운영 서버가 응답하지 않았습니다.")
    sys.exit(1)


if __name__ == "__main__":
    root = get_prod_root()
    update_code(root)
    install_packages(root)
    request_restart(root)
    check_health()
    print("배포 완료")