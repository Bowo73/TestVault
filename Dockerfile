FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

# on attend mariadb sinon ça pète
CMD sh -c " echo 'Attente de MariaDB sur mariadb:3306...' && \
  while ! nc -z mariadb 3306; do sleep 1; done && \
  echo 'MariaDB est prêt, démarrage de l’app' && \
  python app.py"
