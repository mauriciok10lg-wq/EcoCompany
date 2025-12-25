from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

app = Flask(__name__)
app.secret_key = "ecoCompany_super_secret_key"

USERS_FILE = "users.json"
GAME_STATE_FILE = "game_state.json"

# ---------- util ----------
def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_game():
    with open(GAME_STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_game(data):
    with open(GAME_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ---------- rotas ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()["users"]

        if username in users and check_password_hash(
            users[username]["password"], password
        ):
            session["user"] = username
            return redirect(url_for("dashboard"))

        return render_template("login.html", erro="Usuário ou senha inválidos")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    game = load_game()

    return render_template(
        "dashboard.html",
        user=session["user"],
        game=game
    )


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/avancar_mes", methods=["POST"])
def avancar_mes():
    if "user" not in session:
        return redirect(url_for("login"))

    game = load_game()
    fabrica = game["fabrica"]

    # limpa alerta anterior
    game["alerta"] = ""

    @app.route("/fabrica", methods=["GET", "POST"])
def fabrica():
    if "user" not in session:
        return redirect(url_for("login"))

    game = load_game()
    fabrica = game["fabrica"]

    if request.method == "POST":
        fabrica["ativa"] = "ativa" in request.form

        # Se vierem os campos do formulário avançado
        if "consumo_minerio" in request.form:
            fabrica["consumo_minerio"] = int(request.form["consumo_minerio"])
            fabrica["consumo_energia"] = int(request.form["consumo_energia"])
            fabrica["producao_aco"] = int(request.form["producao_aco"])

        save_game(game)
        return redirect(url_for("fabrica"))

    return render_template("fabrica.html", fabrica=fabrica)

    game["mes_atual"] += 1
    save_game(game)

    return redirect(url_for("dashboard"))

@app.route("/fabrica", methods=["GET", "POST"])
def fabrica():
    if "user" not in session:
        return redirect(url_for("login"))

    game = load_game()
    fabrica = game["fabrica"]

    if request.method == "POST":
        fabrica["consumo_minerio"] = int(request.form["consumo_minerio"])
        fabrica["consumo_energia"] = int(request.form["consumo_energia"])
        fabrica["producao_aco"] = int(request.form["producao_aco"])
        fabrica["ativa"] = "ativa" in request.form

        save_game(game)
        return redirect(url_for("fabrica"))

    return render_template("fabrica.html", fabrica=fabrica)


# ---------- start ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
