import yaml
import os
import pathlib

from flask import Flask, jsonify, request

app = Flask(__name__)
app.json.ensure_ascii = False

VERSION = "0.4.0"
BASE_DIR = pathlib.Path(__file__).parent


def load_monsters():
    path = BASE_DIR / "data" / "monsters.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


@app.route("/")
def index():
    return "몬스터 도감 서버 " + VERSION


@app.route("/health")
def health():
    return jsonify({"status": "ok", "version": VERSION})

@app.route("/monsters")
def monster_list():
    monsters = load_monsters()
    element = request.args.get("element")
    if element is None:
        return jsonify(monsters)
    result = []
    for monster in monsters:
        if monster["element"] == element:
            result.append(monster)
    return jsonify(result)


@app.route("/monsters")
def monster_list():
    return jsonify(load_monsters())



@app.route("/monsters/<monster_id>")
def monster_detail(monster_id):
    for monster in load_monsters():
        if monster["id"] == monster_id:
            return jsonify(monster)
    # 반복문 밖: 끝까지 찾지 못한 경우
    return jsonify({"error": "없는 몬스터입니다: " + monster_id}), 404

@app.route("/dex")
def dex():
    rows = ""
    for m in load_monsters():
        cells = "<td>" + m["name"] + "</td><td>" + m["element"] + "</td><td>" + str(m["level"]) + "</td><td>" + m["weakness"] + "</td>"
        if m["level"] >= 30:
            cells = cells.replace("<td>", "<td><b>").replace("</td>", "</b></td>")
        rows += "<tr>" + cells + "</tr>"
    return (
        "<html><head><meta charset='utf-8'><title>몬스터 도감</title></head><body>"
        + "<h1>몬스터 도감 v" + VERSION + "</h1>"
        + "<table border='1'><tr><th>이름</th><th>속성</th><th>레벨</th><th>약점</th></tr>"
        + rows + "</table></body></html>"
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    app.run(port=port)
