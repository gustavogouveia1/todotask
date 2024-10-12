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

@bp.route("/tasks/edit/<int:task_id>", methods=["POST"])
def edit(task_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        data = request.get_json()
        new_task = data.get('title').strip()

        if not new_task:
            return jsonify(success=False, error="O título da tarefa não pode estar vazio"), 400

        cursor.execute('UPDATE tasks SET title = %s WHERE id = %s', (new_task, task_id))
        connection.commit()
        return jsonify(success=True)

        cursor.execute('SELECT * FROM tasks WHERE id = %s', (task_id,))
        todo = cursor.fetchone()
        if not todo:
            return jsonify(success=False, error="Tarefa não encontrada"), 404

    except mysql.connector.Error as err:
        return jsonify(success=False, error=str(err)), 500
    finally:
        cursor.close()
        connection.close()

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