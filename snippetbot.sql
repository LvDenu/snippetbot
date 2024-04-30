CREATE DATABASE snippetbot;
USE snippetbot;
CREATE TABLE snippets (
    name VARCHAR(255) PRIMARY KEY,
    code_lang VARCHAR(255),
    code LONGTEXT
);
