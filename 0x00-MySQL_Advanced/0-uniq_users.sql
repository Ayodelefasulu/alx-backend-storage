-- Task: Create a table named 'users' with the specified attributes
-- This table should store user information and enforce unique emails

CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    PRIMARY KEY (id)
);

-- The table 'users' has been created with 'id', 'email', and 'name' columns
-- 'id' is the primary key and auto-increments
-- 'email' is unique and cannot be null
-- 'name' is a string with a maximum length of 255 characters
