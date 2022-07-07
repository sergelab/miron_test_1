

CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT
);

INSERT INTO products (title, description) VALUES ('Товар 1', 'Описание 1');
INSERT INTO products (title, description) VALUES ('Товар 2', 'Описание 2');
INSERT INTO products (title, description) VALUES ('Товар 3', 'Описание 3');
INSERT INTO products (title, description) VALUES ('Товар 4', 'Описание 4');
INSERT INTO products (title, description) VALUES ('Товар 5', 'Описание 5');
