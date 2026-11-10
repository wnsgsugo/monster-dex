import json
import os
import pathlib

from flask import Flask, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False

VERSION = "0.1.0"
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    app.run(port=port)
