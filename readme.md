# Projet Vault + MariaDB + Application Python

Ce projet montre comment :

- Déployer une base de données **MariaDB**
- Stocker les identifiants de connexion dans **HashiCorp Vault**
- Lire les identifiants via Vault dans une **application Python**
- Faire en sorte que l’application continue de fonctionner même si le mot de passe change (sans modifier le code)

---

## Contenu

- `app.py` : application Python qui lit les secrets depuis Vault et interroge la base MariaDB.
- `Dockerfile` : image pour exécuter `app.py`, attend automatiquement que MariaDB soit prêt.
- `init.sql` : initialise la table `livre` avec quelques entrées.
- `init-vault.sh` : initialise le vault.
- `docker-compose.yml` : déploie MariaDB, Vault en mode dev et l’application.

---

## Lancement rapide

### 1. Lancer les services

```bash
docker-compose up --build
