CREATE DATABASE IF NOT EXISTS multicont_db;

USE multicont_db;

CREATE TABLE IF NOT EXISTS users (
	id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name varchar(50) NOT NULL,
	email varchar(50) NOT NULL,
	address varchar(50) NOT NULL,
	phone varchar(10) NOT NULL
);


