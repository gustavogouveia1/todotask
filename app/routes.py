from flask import Blueprint, render_template, request, jsonify
from .db import get_db_connection

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/tasks', methods=['GET'])
def tasks():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(tasks=tasks)

@bp.route("/tasks/add", methods=["POST"])
def add():
    data = request.get_json()
    todo = data.get('todo', '').strip() 
    if not todo:
        return jsonify(success=False, error="O título da tarefa não pode estar vazio"), 400
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO tasks (title) VALUES (%s)', (todo,))
    connection.commit()
    task_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return jsonify(success=True, task={'id': task_id, 'title': todo, 'status': 'pendente'})
