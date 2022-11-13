-- DROP DATABASE IF EXISTS family_faves_db;

-- CREATE DATABASE family_faves_db;

-- USE family_faves_db;

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS recipes;

CREATE TABLE user (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  password VARCHAR(8) NOT NULL
);

CREATE TABLE recipes (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  recipe_title VARCHAR(50) NOT NULL,
  url VARCHAR(255) NOT NULL,
  description VARCHAR(500) NOT NULL,
  name VARCHAR(50) NOT NULL
);

-- INSERT INTO user (username, password) VALUES
--     ("maddy", "password"),
--     ("rachel", "password");

-- INSERT INTO recipes (recipe_title, url, description, name) VALUES
--   ("Banana Bread", "http://www.google.com", "Better than mom's, don't tell!", "the kids"),
--   ("Pizza", "http://www.google.com", "Mushroom, sausage and cheese", "Dad"),
--   ("Enchiladas", "http://www.google.com", "Vegan, sweet potato and black bean", "Stacy");
  
