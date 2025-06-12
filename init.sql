
CREATE TABLE IF NOT EXISTS livre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(255)
);

INSERT INTO livre (titre) VALUES ('Le Petit Prince'), ('1984'), ('Dune');
