CREATE TABLE users (
   id INT PRIMARY KEY,
   name VARCHAR(255),
   password VARCHAR(255),
   token VARCHAR(255)
);

INSERT INTO users (id,name,password,token) VALUES(1,'Erkebulan','qwerty',NULL),
(2,'Marat','asd',NULL),
(3,'Ers','tamme',NULL)