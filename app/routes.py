from flask import Blueprint, render_template, request, jsonify
from .redis_config import get_redis_client
from .db import get_db_connection, mysql
from datetime import datetime
import json

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

def datetime_converter(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

# Obtem a conexão com o Redis
redis_client = get_redis_client()

@bp.route('/tasks', methods=['GET'])
def tasks():
    cache_key = "tasks_cache"

    cached_tasks = redis_client.get(cache_key)

    if cached_tasks:
        return jsonify(tasks=json.loads(cached_tasks))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()

    # Converte datetime para string antes de serializar
    for task in tasks:
        # Aqui você pode verificar especificamente por 'created_at'
        if 'created_at' in task and isinstance(task['created_at'], datetime):
            task['created_at'] = task['created_at'].isoformat()  # Converte 'created_at' para string

    # Armazena as tarefas no cache por 1800 segundos (30 minutos)
    redis_client.setex(cache_key, 60, json.dumps(tasks))

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

    redis_client.delete("tasks_cache")

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
        
        cursor.execute('SELECT * FROM tasks WHERE id = %s', (task_id,))
        todo = cursor.fetchone()
        if not todo:
            return jsonify(success=False, error="Tarefa não encontrada"), 404

        cursor.execute('UPDATE tasks SET title = %s WHERE id = %s', (new_task, task_id))
        connection.commit()

        redis_client.delete("tasks_cache")
    
        return jsonify(success=True, task={'id': task_id, 'title': new_task})

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

    redis_client.delete("tasks_cache")

    return jsonify(success=True)

@bp.route("/tasks/delete/<int:task_id>", methods=["DELETE"])
def delete(task_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    connection.commit()
    cursor.close()
    connection.close()

    redis_client.delete("tasks_cache")
    
    return jsonify(success=True)