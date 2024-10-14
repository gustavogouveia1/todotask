from flask import Flask, Blueprint, render_template, request, jsonify, redirect, url_for, make_response
from app.models import get_redis_client, get_db_connection, mysql
from datetime import datetime, timedelta
import json
import hashlib
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta_aqui'  
app.config['JWT_TOKEN_LOCATION'] = ['cookies']  
app.config['JWT_COOKIE_SECURE'] = False  
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  

jwt = JWTManager(app)

redis_client = get_redis_client()

auth_bp = Blueprint('auth', __name__)
print("Blueprint auth_bp foi criado com sucesso!")

def index():
    return render_template('index.html')

@auth_bp.route('/auth/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return jsonify({"error": "Usuário e senha são obrigatórios!"}), 400

        if verify_user(username, password):
            access_token = create_access_token(identity=username)

            redis_client.set(f'token:{username}', access_token, ex=3600)  

            response = make_response(redirect(url_for('tasks.index'))) 
            response.set_cookie('access_token', access_token, httponly=True)  
            response.set_cookie('username', username, httponly=True)  

            return response

        else:
            return jsonify({"error": "Usuário ou senha inválidos!"}), 401

def verify_user(username, password):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT password FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    connection.close()

    if user is None:
        return False

    stored_password_hash = user['password']  
    input_password_hash = hashlib.sha256(password.encode()).hexdigest()  

    return stored_password_hash == input_password_hash

@auth_bp.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if not username or not password or not email:
            return jsonify({"error": "Todos os campos são obrigatórios!"}), 400

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('INSERT INTO users (username, password, email) VALUES (%s, %s, %s)', (username, hashed_password, email))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({
            "message": "Usuário registrado com sucesso!",
            "username": username,
            "email": email
        }), 201