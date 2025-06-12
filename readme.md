commande pour mariaDB:

docker run -d \
  --name mariadb \
  -e MARIADB_ROOT_PASSWORD=yourpassword \
  -e MARIADB_DATABASE=demo \
  -p 3306:3306 \
  mariadb:latest

  docker run -d --name mariadb -e MARIADB_ROOT_PASSWORD=yourpassword -e MARIADB_DATABASE=demo -p 3306:3306 mariadb:latest

Commande pour hashicorp vault:

docker run --cap-add=IPC_LOCK -d \
  --name=vault-dev \
  -p 8200:8200 \
  -e VAULT_DEV_ROOT_TOKEN_ID=root \
  -e VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200 \
  hashicorp/vault:latest

docker run --cap-add=IPC_LOCK -d --name=vault-dev -p 8200:8200 -e VAULT_DEV_ROOT_TOKEN_ID=root -e VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200 hashicorp/vault:latest