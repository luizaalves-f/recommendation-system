PRAGMA foreign_keys = ON;

-- Usuarios
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,                           -- Nome do usuario
    last_name TEXT,                               -- Sobrenome do usuario
    email TEXT UNIQUE NOT NULL COLLATE NOCASE,    -- Email unico sem diferenciar maiusculas/minusculas
    password_hash TEXT NOT NULL,                  -- Hash da senha (nunca salvar senha em texto puro)
    birthday DATE,                                -- Data de nascimento do usuario
    is_active INTEGER NOT NULL DEFAULT 1,         -- 1 = ativo, 0 = inativo
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login_at DATETIME
);
CREATE INDEX idx_users_email ON users(email);

-- Idiomas
CREATE TABLE languages (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,   -- 'en', 'pt'
    name TEXT NOT NULL            -- 'English', 'Português'
);

-- Filmes
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    language_id INTEGER REFERENCES languages(id) ON DELETE SET NULL,
    year INTEGER,
    poster_url TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_movies_title ON movies(title);
CREATE INDEX idx_movies_year ON movies(year);
CREATE INDEX idx_movies_language ON movies(language_id);

-- Generos
CREATE TABLE IF NOT EXISTS genres (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL       -- Nome do genero
);

-- Diretores
CREATE TABLE IF NOT EXISTS directors (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL       -- Nome do diretor
);

-- Relacao filme-genero (muitos-para-muitos)
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INTEGER NOT NULL,      -- ID do filme, referencia movies(id)
    genre_id INTEGER NOT NULL,      -- ID do genero, referencia genres(id)
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_movie_genres_genre ON movie_genres(genre_id);

-- Relacao filme-diretor (muitos-para-muitos)
-- Se quiser apenas 1 diretor por filme, troque por movies.director_id com FK.
CREATE TABLE IF NOT EXISTS movie_directors (
    movie_id INTEGER NOT NULL,      -- ID do filme, referencia movies(id)
    director_id INTEGER NOT NULL,   -- ID do diretor, referencia directors(id)
    PRIMARY KEY (movie_id, director_id),
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
    FOREIGN KEY (director_id) REFERENCES directors(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_movie_directors_director ON movie_directors(director_id);

-- Avaliacoes dos usuarios
CREATE TABLE IF NOT EXISTS ratings (
    user_id INTEGER NOT NULL,                                 -- ID do usuario, referencia users(id)
    movie_id INTEGER NOT NULL,                                -- ID do filme, referencia movies(id)
    rating REAL NOT NULL CHECK (rating >= 0 AND rating <= 5), -- Nota de 0 a 5
    rated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, movie_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_ratings_user ON ratings(user_id);
CREATE INDEX IF NOT EXISTS idx_ratings_movie ON ratings(movie_id);

CREATE VIEW IF NOT EXISTS movie_popularity AS
SELECT
    movie_id,
    AVG(rating) AS avg_rating,
    COUNT(*) AS num_ratings
FROM ratings
GROUP BY movie_id;