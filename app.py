from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.security import check_password_hash
import os
import json
import time

app = Flask(__name__)
app.secret_key = "ecoCompany_super_secret_key"

USERS_FILE = "users.json"
GAME_STATE_FILE = "game_state.json"

# ================= UTIL =================
def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_game():
    with open(GAME_STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_game(data):
    with open(GAME_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ================= PRODUÇÃO AUTOMÁTICA 24H =================
def processar_producao(game):
    agora = int(time.time())

    # ---------- FÁBRICA ----------
    fab = game["fabrica"]
    if fab["ativa"]:
        horas = (agora - fab["ultimo_calculo"]) / 3600
        if horas > 0:
            consumo_minerio = fab["consumo_minerio_hora"] * horas
            consumo_energia = fab["consumo_energia_hora"] * horas
            producao_aco = fab["producao_aco_hora"] * horas

            if (
                game["estoque"]["minerio"] >= consumo_minerio
                and game["energia"] >= consumo_energia
            ):
                game["estoque"]["minerio"] -= consumo_minerio
                game["energia"] -= consumo_energia
                game["estoque"]["aco"] += producao_aco

        fab["ultimo_calculo"] = agora

    # ---------- MINERAÇÃO ----------
    min = game["mineracao"]
    if min["ativa"]:
        horas = (agora - min["ultimo_calculo"]) / 3600
        if horas > 0:
            consumo_energia = min["consumo_energia_hora"] * horas
            producao_minerio = min["producao_minerio_hora"] * horas

            if game["energia"] >= consumo_energia:
                game["energia"] -= consumo_energia
                game["estoque"]["minerio"] += producao_minerio

        min["ultimo_calculo"] = agora

    # ---------- FAZENDA ----------
    faz = game["fazenda"]
    if faz["ativa"]:
        horas = (agora - faz["ultimo_calculo"]) / 3600
        if horas > 0:
            consumo_energia = faz["consumo_energia_hora"] * horas
            producao_graos = faz["producao_graos_hora"] * horas

            if game["energia"] >= consumo_energia:
                game["energia"] -= consumo_energia
                game["estoque"]["graos"] += producao_graos

        faz["ultimo_calculo"] = agora

    return game

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = load_users()["users"]
        u = request.form["username"]
        p = request.form["password"]

        if u in users and check_password_hash(users[u]["password"], p):
            session["user"] = u
            return redirect(url_for("dashboard"))

        return render_template("login.html", erro="Usuário ou senha inválidos")

    return render_template("login.html")

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    game = load_game()
    game = processar_producao(game)
    save_game(game)

    game.setdefault("indice_verde", 100)
game.setdefault("empresas", 1)
game.setdefault("alerta", "")

    return render_template("dashboard.html", game=game)

# ================= FÁBRICA =================
@app.route("/fabrica", methods=["GET", "POST"])
def fabrica():
    if "user" not in session:
        return redirect(url_for("login"))

    game = load_game()
    fab = game["fabrica"]

    if request.method == "POST":
        fab["ativa"] = "ativa" in request.form
        fab["consumo_minerio_hora"] = int(request.form["consumo_minerio"])
        fab["consumo_energia_hora"] = int(request.form["consumo_energia"])
        fab["producao_aco_hora"] = int(request.form["producao_aco"])
        save_game(game)
        return redirect(url_for("fabrica"))

    return render_template("fabrica.html", fabrica=fab)

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/mercado", methods=["GET", "POST"])
def mercado():
    if "user" not in session:
        return redirect(url_for("login"))

    game = load_game()

    precos = {
        "minerio": {"buy": 50, "sell": 40},
        "aco": {"buy": 120, "sell": 100},
        "graos": {"buy": 30, "sell": 25}
    }

    if request.method == "POST":
        item = request.form["item"]
        acao = request.form["acao"]
        qtd = int(request.form["quantidade"])

        if acao == "comprar":
            custo = precos[item]["buy"] * qtd
            if game["dinheiro"] >= custo:
                game["dinheiro"] -= custo
                game["estoque"][item] += qtd

        elif acao == "vender":
            if game["estoque"][item] >= qtd:
                ganho = precos[item]["sell"] * qtd
                game["estoque"][item] -= qtd
                game["dinheiro"] += ganho

        save_game(game)
        return redirect(url_for("mercado"))

    return render_template("mercado.html", game=game, precos=precos)

# ================= START =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
