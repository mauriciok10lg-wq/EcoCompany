from flask import Flask, render_template
import os
import json

app = Flask(__name__)

DATA_FILE = "game_state.json"

# 🔹 Carregar dados do jogo
def load_game_state():
    if not os.path.exists(DATA_FILE):
        return {
            "caixa": 0,
            "energia": 0,
            "indice_verde": 0,
            "empresas": 0
        }
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# 🔹 Salvar dados do jogo
def save_game_state(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route("/")
def dashboard():
    game = load_game_state()
    return render_template(
        "dashboard.html",
        caixa=game["caixa"],
        energia=game["energia"],
        indice_verde=game["indice_verde"],
        empresas=game["empresas"]
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
