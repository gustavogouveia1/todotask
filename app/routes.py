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

@bp.route("/tasks/update_status/<int:task_id>", methods=["POST"])
def update_status(task_id):
    data = request.get_json()
    new_status = data.get('status')

    if new_status not in ['pendente', 'em andamento', 'completa']:
        return jsonify(success=False, error="Status inválido"), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('UPDATE tasks SET status = %s WHERE id = %s', (new_status, task_id))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify(success=True)