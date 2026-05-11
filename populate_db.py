import ast
import random
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "recsys.db"
SCHEMA_SQL = BASE_DIR / "schema.sql"
MOVIES_CSV = BASE_DIR / "tmdb_5000_movies.csv"
CREDITS_CSV = BASE_DIR / "tmdb_5000_credits.csv"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"


def parse_jsonish(value):
    if pd.isna(value):
        return []
    if isinstance(value, list):
        return value
    if not isinstance(value, str) or not value.strip():
        return []

    try:
        parsed = ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return []

    return parsed if isinstance(parsed, list) else []


def load_datasets():
    movies = pd.read_csv(MOVIES_CSV)
    credits = pd.read_csv(CREDITS_CSV).rename(columns={"movie_id": "id"})

    required_movies_columns = {
        "id",
        "title",
        "overview",
        "release_date",
        "original_language",
        "genres",
    }
    required_credits_columns = {"id", "crew"}

    missing_movies = required_movies_columns - set(movies.columns)
    missing_credits = required_credits_columns - set(credits.columns)
    if missing_movies or missing_credits:
        raise ValueError(
            "Colunas ausentes nos CSVs. "
            f"movies: {sorted(missing_movies)}; credits: {sorted(missing_credits)}"
        )

    return pd.merge(movies, credits[["id", "crew"]], on="id", how="inner")


def recreate_schema(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF")

    cursor.executescript(
        """
        DROP VIEW IF EXISTS movie_popularity;
        DROP TABLE IF EXISTS ratings;
        DROP TABLE IF EXISTS movie_directors;
        DROP TABLE IF EXISTS movie_genres;
        DROP TABLE IF EXISTS directors;
        DROP TABLE IF EXISTS genres;
        DROP TABLE IF EXISTS movies;
        DROP TABLE IF EXISTS languages;
        DROP TABLE IF EXISTS users;
        """
    )

    with open(SCHEMA_SQL, "r", encoding="utf-8") as schema_file:
        cursor.executescript(schema_file.read())

    cursor.execute("PRAGMA foreign_keys = ON")
    conn.commit()


def build_language_map(conn, df):
    languages = sorted(code for code in df["original_language"].dropna().unique() if code)
    conn.executemany(
        "INSERT OR IGNORE INTO languages (code, name) VALUES (?, ?)",
        [(code, code.upper()) for code in languages],
    )

    rows = conn.execute("SELECT id, code FROM languages").fetchall()
    return {code: language_id for language_id, code in rows}


def build_poster_url(poster_path):
    if pd.isna(poster_path) or not str(poster_path).strip():
        return None
    path = str(poster_path).strip()
    return path if path.startswith("http") else f"{POSTER_BASE_URL}{path}"


def build_year(release_date):
    parsed = pd.to_datetime(release_date, errors="coerce")
    return None if pd.isna(parsed) else int(parsed.year)


def populate_movies(conn, df, language_ids):
    rows = []
    for _, movie in df.iterrows():
        rows.append(
            (
                int(movie["id"]),
                movie["title"],
                None if pd.isna(movie["overview"]) else movie["overview"],
                language_ids.get(movie["original_language"]),
                build_year(movie["release_date"]),
                build_poster_url(movie.get("poster_path")),
            )
        )

    conn.executemany(
        """
        INSERT OR REPLACE INTO movies
            (id, title, description, language_id, year, poster_url)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows,
    )


def get_or_create_id(conn, table, name):
    conn.execute(f"INSERT OR IGNORE INTO {table} (name) VALUES (?)", (name,))
    row = conn.execute(f"SELECT id FROM {table} WHERE name = ?", (name,)).fetchone()
    return row[0]


def populate_genres(conn, df):
    movie_genres = set()

    for _, movie in df.iterrows():
        movie_id = int(movie["id"])
        for genre in parse_jsonish(movie["genres"]):
            genre_name = genre.get("name") if isinstance(genre, dict) else None
            if not genre_name:
                continue
            genre_id = get_or_create_id(conn, "genres", genre_name)
            movie_genres.add((movie_id, genre_id))

    conn.executemany(
        "INSERT OR IGNORE INTO movie_genres (movie_id, genre_id) VALUES (?, ?)",
        sorted(movie_genres),
    )


def populate_directors(conn, df):
    movie_directors = set()

    for _, movie in df.iterrows():
        movie_id = int(movie["id"])
        for crew_member in parse_jsonish(movie["crew"]):
            if not isinstance(crew_member, dict) or crew_member.get("job") != "Director":
                continue
            director_name = crew_member.get("name")
            if not director_name:
                continue
            director_id = get_or_create_id(conn, "directors", director_name)
            movie_directors.add((movie_id, director_id))

    conn.executemany(
        """
        INSERT OR IGNORE INTO movie_directors (movie_id, director_id)
        VALUES (?, ?)
        """,
        sorted(movie_directors),
    )


def populate_demo_users_and_ratings(conn):
    users_data = [
        ("Ana", "Silva", "ana@teste.com", "hash123", "1990-05-10"),
        ("Bruno", "Souza", "bruno@teste.com", "hash456", "1985-08-22"),
        ("Carla", "Oliveira", "carla@teste.com", "hash789", "1995-12-03"),
    ]
    conn.executemany(
        """
        INSERT OR IGNORE INTO users
            (name, last_name, email, password_hash, birthday)
        VALUES (?, ?, ?, ?, ?)
        """,
        users_data,
    )

    movie_ids = [row[0] for row in conn.execute("SELECT id FROM movies")]
    user_ids = [row[0] for row in conn.execute("SELECT id FROM users")]

    ratings = []
    for user_id in user_ids:
        for movie_id in random.sample(movie_ids, min(10, len(movie_ids))):
            ratings.append(
                (
                    user_id,
                    movie_id,
                    round(random.uniform(2.5, 5.0), 1),
                    datetime.now().isoformat(timespec="seconds"),
                )
            )

    conn.executemany(
        """
        INSERT OR IGNORE INTO ratings (user_id, movie_id, rating, rated_at)
        VALUES (?, ?, ?, ?)
        """,
        ratings,
    )


def print_counts(conn):
    for table in (
        "languages",
        "movies",
        "genres",
        "movie_genres",
        "directors",
        "movie_directors",
        "users",
        "ratings",
    ):
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"   {table}: {count}")


def main():
    print("1. Carregando e mesclando datasets...")
    df = load_datasets()

    print("2. Recriando banco conforme schema.sql...")
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        recreate_schema(conn)

        print("3. Populando idiomas...")
        language_ids = build_language_map(conn, df)

        print("4. Populando filmes...")
        populate_movies(conn, df, language_ids)

        print("5. Populando generos e relacionamentos...")
        populate_genres(conn, df)

        print("6. Populando diretores e relacionamentos...")
        populate_directors(conn, df)

        print("7. Criando usuarios e avaliacoes ficticios...")
        populate_demo_users_and_ratings(conn)

        conn.commit()
        print("8. Totais inseridos:")
        print_counts(conn)

    print("Populacao concluida com sucesso!")


if __name__ == "__main__":
    main()
