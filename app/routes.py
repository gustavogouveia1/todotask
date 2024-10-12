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