import json
import os
import pathlib

from flask import Flask, jsonify, request

app = Flask(__name__)
app.json.ensure_ascii = False

VERSION = "0.2.0"
BASE_DIR = pathlib.Path(__file__).parent


def load_monsters():
    path = BASE_DIR / "data" / "monsters.json"
    return json.loads(path.read_text(encoding="utf-8"))


@app.route("/")
def index():
    return "몬스터 도감 서버 " + VERSION


@app.route("/health")
def health():
    return jsonify({"status": "ok", "version": VERSION})


@app.route("/monsters")
def monster_list():
    return jsonify(load_monsters())

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

@app.route("/monsters/<monster_id>")
def monster_detail(monster_id):
    for monster in load_monsters():
        if monster["id"] == monster_id:
            return jsonify(monster)
    # 반복문 밖: 끝까지 찾지 못한 경우
    return jsonify({"error": "없는 몬스터입니다: " + monster_id}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    app.run(port=port)
