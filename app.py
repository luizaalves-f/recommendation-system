import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request


BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "recsys.db"

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def fetch_genres():
    with get_db_connection() as conn:
        rows = conn.execute("SELECT name FROM genres ORDER BY name").fetchall()
    return [row["name"] for row in rows]


def fetch_recommendations(genero, limit=10):
    genre_name = genero.strip()

    with get_db_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                m.id,
                m.title,
                m.description,
                m.year,
                m.poster_url,
                g.name AS genre,
                COALESCE(mp.avg_rating, 0) AS avg_rating,
                COALESCE(mp.num_ratings, 0) AS num_ratings
            FROM movies m
            JOIN movie_genres mg ON mg.movie_id = m.id
            JOIN genres g ON g.id = mg.genre_id
            LEFT JOIN movie_popularity mp ON mp.movie_id = m.id
            WHERE g.name = ? COLLATE NOCASE
            ORDER BY
                mp.avg_rating IS NULL,
                mp.avg_rating DESC,
                mp.num_ratings DESC,
                m.year DESC,
                m.title ASC
            LIMIT ?
            """,
            (genre_name, limit),
        ).fetchall()

    return [dict(row) for row in rows]


@app.route("/", methods=["GET"])
def pagina_inicial():
    return jsonify(
        {
            "mensagem": "API de recomendacao de filmes em execucao.",
            "endpoints": {
                "generos": {"metodo": "GET", "url": "/generos"},
                "recomendar": {
                    "metodo": "POST",
                    "url": "/recomendar",
                    "exemplo_body": {"genero": "Action"},
                },
            },
        }
    )


@app.route("/generos", methods=["GET"])
def listar_generos():
    return jsonify({"generos": fetch_genres()})


@app.route("/recomendar", methods=["POST"])
def recomendar_filmes():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"erro": "Envie um corpo JSON valido."}), 400

    genero = data.get("genero")
    if not isinstance(genero, str) or not genero.strip():
        return jsonify({"erro": "Genero nao informado ou invalido."}), 400

    recomendacoes = fetch_recommendations(genero)
    if not recomendacoes:
        return (
            jsonify(
                {
                    "erro": "Nenhuma recomendacao encontrada para o genero informado.",
                    "genero": genero,
                    "generos_disponiveis": fetch_genres(),
                }
            ),
            404,
        )

    return jsonify(
        {
            "genero": genero.strip(),
            "recomendacoes": recomendacoes,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
