CREATE TABLE IF NOT EXISTS livre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    totp_secret VARCHAR(32) NOT NULL,
    last_login DATETIME DEFAULT NULL
);

INSERT INTO livre (titre) VALUES ('Le Petit Prince'), ('1984'), ('Dune');

INSERT INTO users (username, password, totp_secret, last_login)
VALUES (
  'admin',
  SHA2('adminpass', 256),
  'JBSWY3DPEHPK3PXP',
  NULL
);
