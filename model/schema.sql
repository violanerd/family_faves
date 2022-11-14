-- DROP DATABASE IF EXISTS family_faves_db;

-- CREATE DATABASE family_faves_db;

-- USE family_faves_db;

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS recipes;

CREATE TABLE user (
  id INTEGER PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  password VARCHAR(8) NOT NULL
);

CREATE TABLE recipes (
  id INTEGER PRIMARY KEY,
  recipe_title VARCHAR(50) NOT NULL,
  url VARCHAR(255) NOT NULL,
  description VARCHAR(500) NOT NULL,
  name VARCHAR(50) NOT NULL
);


  
