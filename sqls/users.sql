

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    pw_hash TEXT NOT NULL DEFAULT '<unset>',
    username TEXT NOT NULL UNIQUE,
    name TEXT
);