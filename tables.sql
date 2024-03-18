CREATE SCHEMA IF NOT EXISTS aipdf;

CREATE TABLE IF NOT EXISTS aipdf.user (
  id serial primary key,
  email varchar(100) not null unique,
  username varchar(20) not null unique,
  is_active bool default false,
  created_at timestamp default current_timestamp,
  updated_at timestamp
);

CREATE TABLE IF NOT EXISTS aipdf.pdf_vector (
  id SERIAL NOT NULL PRIMARY KEY,
  vectorstore_path varchar NOT NULL UNIQUE,
  user_id INT NOT NULL,
  label VARHCAR(30) NOT NULL,
  uuid VARCHAR(36) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS aipdf.chat (
  id SERIAL NOT NULL PRIMARY KEY,
  user_id INT NOT NULL,
  pdf_id INT NOT NULL,
  uuid VARCHAR(36) NOT NULL,
  name VARCHAR(30) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS aipdf.tokens (
  id SERIAL NOT NULL PRIMARY KEY,
  user_id INT NOT NULL,
  token_sequence VARCHAR(40) NOT NULL UNIQUE,
  is_enable BOOL DEFAULT FALSE,
  FOREIGN KEY (user_id) REFERENCES user(id)
);
