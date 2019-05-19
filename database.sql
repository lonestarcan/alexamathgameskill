DROP TABLE users;
CREATE TABLE IF NOT EXISTS users (
	id varchar(1000),
	question text,
	answer int,
	PRIMARY KEY(id)
);
