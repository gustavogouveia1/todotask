import mysql.connector

db_config = {
    'user': 'usuario',
    'password': 'senha',
    'host': 'host',
    'database': 'banco de dados'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)