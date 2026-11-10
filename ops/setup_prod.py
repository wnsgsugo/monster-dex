import os
import pathlib
import sys
import venv

PORTS = {"live": "8001", "staging": "8002"}


def get_base():
    base = os.environ.get("DEPLOY_BASE", "")
    if base != "":
        return pathlib.Path(base)
    if os.name == "nt":
        return pathlib.Path("C:/monster")
    return pathlib.Path("/Users/Shared/monster")


target = sys.argv[1] if len(sys.argv) > 1 else "live"
if target not in PORTS:
    print("사용법: python ops/setup_prod.py [live | staging]")
    sys.exit(2)

root = get_base() / target
(root / "app").mkdir(parents=True, exist_ok=True)
flag = root / "restart.flag"
if not flag.exists():
    flag.write_text("", encoding="utf-8")

venv_dir = root / ".venv"
if venv_dir.exists():
    print("[준비] 가상환경이 이미 있습니다: " + str(venv_dir))
else:
    print("[준비] 가상환경을 만드는 중입니다. (10~30초)")
    venv.create(venv_dir, with_pip=True)

if os.name == "nt":
    python = venv_dir / "Scripts" / "python.exe"
else:
    python = venv_dir / "bin" / "python"

print("[준비] 완료")
print("  폴더: " + str(root))
print("  파이썬: " + str(python))
print("  포트: " + PORTS[target])
print("  다음 단계: 새 터미널 창에서 저장소 폴더로 이동한 뒤 run_prod.py " + target + " 실행")
