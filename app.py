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
        empresas=game["empresas"]
    )

# 🔘 BOTÃO PRODUZIR
@app.route("/produzir")
def produzir():
    game = load_game_state()

    if game["energia"] >= 10:
        game["energia"] -= 10
        game["caixa"] += 500

    save_game_state(game)
    return redirect(url_for("dashboard"))

# ⛏️ BOTÃO MINERAR
@app.route("/minerar")
def minerar():
    game = load_game_state()

    if game["energia"] >= 20:
        game["energia"] -= 20
        game["caixa"] += 800

    save_game_state(game)
    return redirect(url_for("dashboard"))

# ⚡ BOTÃO COMPRAR ENERGIA
@app.route("/comprar-energia")
def comprar_energia():
    game = load_game_state()

    if game["caixa"] >= 1000:
        game["caixa"] -= 1000
        game["energia"] += 100

    save_game_state(game)
    return redirect(url_for("dashb_
