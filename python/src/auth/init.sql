DROP USER IF EXISTS 'auth_user'@'localhost';

CREATE USER IF NOT EXISTS 'auth_user'@'localhost' IDENTIFIED BY 'Auth123';

DROP DATABASE auth;

CREATE DATABASE IF NOT EXISTS auth;

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

USE auth;

CREATE TABLE IF NOT EXISTS user(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user(email, password) VALUES("spec@specmail.com", "specpass");

