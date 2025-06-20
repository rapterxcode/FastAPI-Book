-- Create database if not exists
CREATE DATABASE IF NOT EXISTS bookstore;

-- Use the database
USE bookstore;

-- Create books table
CREATE TABLE IF NOT EXISTS books (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  author VARCHAR(255) NOT NULL,
  published_year INT,
  genre VARCHAR(100),
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create indexes for better search performance
CREATE INDEX idx_title ON books(title);
CREATE INDEX idx_author ON books(author);
CREATE INDEX idx_published_year ON books(published_year);
CREATE INDEX idx_genre ON books(genre); 

INSERT INTO books (title, author, published_year, genre) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 1925, 'Fiction'),
('To Kill a Mockingbird', 'Harper Lee', 1960, 'Fiction'),
('1984', 'George Orwell', 1949, 'Dystopian'),
('Pride and Prejudice', 'Jane Austen', 1813, 'Romance'),
('The Hobbit', 'J.R.R. Tolkien', 1937, 'Fantasy'),
('The Catcher in the Rye', 'J.D. Salinger', 1951, 'Fiction'),
('Lord of the Flies', 'William Golding', 1954, 'Fiction'),
('Animal Farm', 'George Orwell', 1945, 'Allegory'),
('The Alchemist', 'Paulo Coelho', 1988, 'Fiction'),
('Brave New World', 'Aldous Huxley', 1932, 'Dystopian');

SELECT * FROM books; 