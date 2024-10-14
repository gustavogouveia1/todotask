from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.models import get_redis_client, get_db_connection, mysql
from datetime import datetime
import json
import hashlib

auth_bp = Blueprint('auth', __name__)
print("Blueprint tasks_bp foi criado com sucesso!")

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
        return redirect(url_for('tasks.index'))
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
