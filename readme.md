
# Projet Flask + Vault + MariaDB

Ce projet montre comment :

- Déployer une base de données **MariaDB** avec initialisation automatique
- Stocker les identifiants de connexion dans **HashiCorp Vault**
- Lire les secrets depuis Vault dans une **application Flask**
- Ajouter un système de **login avec authentification à deux facteurs (TOTP)**
- Générer dynamiquement les mots de passe TOTP (compatibles Google Authenticator)
- Ajouter un **CAPTCHA** pour contrer les bots
- Suivre la **dernière connexion** et détecter les **comptes obsolètes**
- Protéger les formulaires contre les **attaques par rejeu (anti-replay)**

---

## Contenu

- `app.py` : application Flask avec authentification (login + TOTP), CAPTCHA, anti-rejeu, détection d'inactivité et affichage des livres.
- `Dockerfile` : image Python qui attend automatiquement MariaDB avant de démarrer l'app Flask.
- `init.sql` : initialise la base `testvault` avec les tables `livre` et `users`, et ajoute des données de test.
- `init-vault.sh` : initialise le Vault avec un secret de connexion pour MariaDB.
- `docker-compose.yml` : déploie Vault, MariaDB, et l'application Flask.

---

## Lancement rapide

### 1. Lancer tous les services

```bash
docker-compose down -v
docker-compose up --build
```

### 2. Accéder à l’application

- URL : [http://localhost:5000](http://localhost:5000)
- Identifiants :
  - Utilisateur : `admin`
  - Mot de passe : `adminpass`
  - Clé TOTP : `JBSWY3DPEHPK3PXP` (scan via Google Authenticator ou FreeOTP)

### 3. Générer un code TOTP (si besoin)

```python
import pyotp
print(pyotp.TOTP("JBSWY3DPEHPK3PXP").now())
```

---

## Fonctionnalité de sécurité

- Le mot de passe est stocké hashé (SHA-256) dans la base
- Le code TOTP expire toutes les 30 secondes
- Les identifiants de connexion à MariaDB sont sécurisés dans Vault

---

## À faire

- Ajouter un front HTML stylisé (CSS)
- Permettre la création d'utilisateurs avec génération automatique de QR Code
