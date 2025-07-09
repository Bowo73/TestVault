
from flask import Flask, request, render_template_string, redirect, session, url_for, send_file
import os
import time
import hvac
import mysql.connector
import pyotp
import hashlib
import io
import random
import string
import datetime
import secrets as py_secrets
from captcha.image import ImageCaptcha

app = Flask(__name__)
app.secret_key = 'supersecretkey'

login_template = """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
  <h2>Login</h2>
  <form method="post">
    Nom d'utilisateur: <input type="text" name="username"><br>
    Mot de passe: <input type="password" name="password"><br>
    <img src="{{ url_for('captcha') }}" alt="captcha"><br>
    Recopier le code ci-dessus: <input type="text" name="captcha"><br>
    <input type="hidden" name="replay_token" value="{{ token }}">
    <input type="submit" value="Connexion">
  </form>
  {% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
</body>
</html>
"""

totp_template = """
<!DOCTYPE html>
<html>
<head><title>2FA</title></head>
<body>
  <h2>Code de vérification</h2>
  <form method="post">
    Code TOTP: <input type="text" name="code"><br>
    <input type="hidden" name="replay_token" value="{{ token }}">
    <input type="submit" value="Vérifier">
  </form>
  {% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
</body>
</html>
"""

def get_db_credentials():
    client = hvac.Client(url=os.environ['VAULT_ADDR'], token=os.environ['VAULT_TOKEN'])
    db_secrets = client.secrets.kv.v2.read_secret_version(path="database/testvault", raise_on_deleted_version=True)['data']['data']
    return db_secrets

def get_user_from_db(username):
    creds = get_db_credentials()
    conn = mysql.connector.connect(
        host="mariadb",
        user=creds['username'],
        password=creds['password'],
        database="testvault"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def is_valid_replay_token(token):
    used_tokens = set(session.get('used_tokens', []))
    if not token or token in used_tokens:
        return False
    used_tokens.add(token)
    session['used_tokens'] = list(used_tokens)
    return True

@app.route('/captcha')
def captcha():
    image = ImageCaptcha()
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    session['captcha_text'] = captcha_text
    data = image.generate(captcha_text)
    return send_file(data, mimetype='image/png')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    token = py_secrets.token_hex(16)

    if request.method == 'POST':
        if not is_valid_replay_token(request.form.get('replay_token')):
            error = "Tentative de rejeu détectée"
        elif request.form.get('captcha', '').upper() != session.get('captcha_text', ''):
            error = "Captcha invalide"
        else:
            username = request.form['username']
            password = request.form['password']
            user = get_user_from_db(username)
            if user:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if user['password'] == hashed_password:
                    session['pre_2fa'] = True
                    session['username'] = username
                    return redirect(url_for('totp'))
            error = "Identifiants invalides"

    return render_template_string(login_template, error=error, token=token)

@app.route('/2fa', methods=['GET', 'POST'])
def totp():
    if 'pre_2fa' not in session or 'username' not in session:
        return redirect(url_for('login'))

    error = None
    token = py_secrets.token_hex(16)

    if request.method == 'POST':
        if not is_valid_replay_token(request.form.get('replay_token')):
            error = "Tentative de rejeu détectée"
        else:
            code = request.form['code']
            user = get_user_from_db(session['username'])
            if user:
                totp = pyotp.TOTP(user['totp_secret'])
                if totp.verify(code):
                    session['authenticated'] = True

                    creds = get_db_credentials()
                    conn = mysql.connector.connect(
                        host="mariadb",
                        user=creds['username'],
                        password=creds['password'],
                        database="testvault"
                    )
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET last_login = %s WHERE username = %s", 
                                   (datetime.datetime.utcnow(), session['username']))
                    conn.commit()
                    cursor.close()
                    conn.close()

                    return redirect(url_for('index'))
            error = "Code invalide"
    return render_template_string(totp_template, error=error, token=token)

@app.route('/')
def index():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    creds = get_db_credentials()
    conn = mysql.connector.connect(
        host="mariadb",
        user=creds['username'],
        password=creds['password'],
        database="testvault"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livre")
    livres = cursor.fetchall()

    cursor.execute("SELECT last_login FROM users WHERE username = %s", (session['username'],))
    last_login = cursor.fetchone()[0]

    is_obsolete = False
    if last_login is None or (datetime.datetime.utcnow() - last_login).days > 90:
        is_obsolete = True

    cursor.close()
    conn.close()

    book_list = "<br>".join(f"{id}: {titre}" for id, titre in livres)
    login_info = f"<p>Dernière connexion : {last_login or 'Jamais'}</p>"
    login_info += f"<p>Compte obsolète : {'Oui' if is_obsolete else 'Non'}</p>"

    return login_info + "<hr>" + book_list

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
