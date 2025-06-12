
import os
import time
import hvac
import mysql.connector

# On attend vault sinon ça casse tt
time.sleep(5)

# Connexion au vault et récup des secrets
client = hvac.Client(url=os.environ['VAULT_ADDR'], token=os.environ['VAULT_TOKEN'])
secrets = client.secrets.kv.v2.read_secret_version(path="database/testvault")['data']['data']

# Connexion à la bdd
conn = mysql.connector.connect(
    host="mariadb",
    user=secrets['username'],
    password=secrets['password'],
    database="testvault"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM livre")
for (id, titre) in cursor.fetchall():
    print(f"{id}: {titre}")
cursor.close()
conn.close()
