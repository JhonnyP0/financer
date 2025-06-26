CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR (50) NOT NULL UNIQUE, 
    password_hash VARCHAR (255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS accounts (
    acc_id INT AUTO_INCREMENT PRIMARY KEY,
    id INT,
    spendings INT,
    savings INT,
    groceries INT,
    FOREIGN KEY (id) references users(id)
);