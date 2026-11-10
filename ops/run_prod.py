import os
import pathlib
import subprocess
import sys
import time

PORTS = {"live": "8001", "staging": "8002"}


def get_base():
    base = os.environ.get("DEPLOY_BASE", "")
    if base != "":
        return pathlib.Path(base)
    if os.name == "nt":
        return pathlib.Path("C:/monster")
    return pathlib.Path("/Users/Shared/monster")


TARGET = sys.argv[1] if len(sys.argv) > 1 else "live"
if TARGET not in PORTS:
    print("사용법: python ops/run_prod.py [live | staging]")
    sys.exit(2)

ROOT = get_base() / TARGET
if os.name == "nt":
    PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"
else:
    PYTHON = ROOT / ".venv" / "bin" / "python"
APP = ROOT / "app" / "app.py"
FLAG = ROOT / "restart.flag"
PORT = PORTS[TARGET]
if not PYTHON.exists():
    print("[운영] " + str(PYTHON) + " 가 없습니다. 먼저 python ops/setup_prod.py " + TARGET + " 를 실행합니다.")
    sys.exit(1)
print("[운영] 대상: " + str(ROOT) + " (포트 " + PORT + ")")


def read_flag():
    if FLAG.exists():
        return FLAG.read_text(encoding="utf-8")
    return ""


def start_app():
    if not APP.exists():
        print("[운영] app/app.py 가 없습니다. 배포 후 restart.flag 를 바꾸면 시작합니다.")
        return None
    env = dict(os.environ)
    env["PORT"] = PORT
    print("[운영] 앱 시작: " + str(APP) + " (포트 " + PORT + ")")
    return subprocess.Popen([str(PYTHON), str(APP)], cwd=str(APP.parent), env=env)


def stop_app(process):
    if process is not None and process.poll() is None:
        print("[운영] 앱 종료")
        process.terminate()
        process.wait()


process = start_app()
last_flag = read_flag()
reported_exit = False
try:
    while True:
        time.sleep(1)
        current_flag = read_flag()
        if current_flag != last_flag:
            print("[운영] restart.flag 변경 확인 → 다시 시작합니다.")
            stop_app(process)
            process = start_app()
            last_flag = current_flag
            reported_exit = False
        elif process is not None and process.poll() is not None and not reported_exit:
            print("[운영] 앱이 종료되었습니다. 종료 코드 " + str(process.returncode))
            print("[운영] 원인을 고친 뒤 다시 배포하면 restart.flag 변경으로 다시 시작합니다.")
            reported_exit = True
except KeyboardInterrupt:
    stop_app(process)
