from flask import Flask, render_template
import os

app = Flask(__name__)

# 🔹 DADOS DO JOGO (por enquanto em memória)
game_state = {
    "caixa": 125000,
    "energia": 18500,
    "indice_verde": 82,
    "empresas": 4
}

@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        caixa=game_state["caixa"],
        energia=game_state["energia"],
        indice_verde=game_state["indice_verde"],
        empresas=game_state["empresas"]
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
