DROP DATABASE IF EXISTS family_faves_db;

CREATE DATABASE family_faves_db;

USE family_faves_db;

DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  password VARCHAR(8) NOT NULL
);

INSERT INTO user (username, password) VALUES
    ("maddy", "password"),
    ("rachel", "password");