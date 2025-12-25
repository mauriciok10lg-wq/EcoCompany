from flask import Flask, render_template, redirect, url_for
import os
import json

app = Flask(__name__)

DATA_FILE = "game_state.json"

def load_game_state():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

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
        empresas=game["empresas"],
        ferro=game["mineracao"]["ferro"]
    )

# ⛏️ MINERAR FERRO
@app.route("/minerar-ferro")
def minerar_ferro():
    game = load_game_state()

    # custo da mineração
    custo_energia = 30

    if game["energia"] >= custo_energia:
        game["energia"] -= custo_energia
        game["mineracao"]["ferro"] += 10  # produz 10 unidades de ferro

    save_game_state(game)
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
