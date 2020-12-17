--load
PRAGMA foreign_keys = ON;

create table movies (
    id integer not null primary key,
    title TEXT,
    url TEXT,
    imdb_code TEXT,
    title_long TEXT,
    slug TEXT,
    year INTEGER,
    rating FLOAT,
    runtime INTEGER,
    summary TEXT,
    yt_trailer_code TEXT,
    language TEXT,
    mpa_rating TEXT,
    background_image TEXT,
    background_image_original TEXT,
    small_cover_image TEXT,
    medium_cover_image TEXT,
    large_cover_image TEXT,
    date_uploaded TEXT,
    date_uploaded_unix INTEGER
);

create table movie_genre(
    record_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL,
    genre TEXT NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(id)
)