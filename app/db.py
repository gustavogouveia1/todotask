import mysql.connector

db_config = {
    'user': 'gouveiadev01',
    'password': 'Loks123',
    'host': 'mysql.gouveiadev.com.br',
    'database': 'gouveiadev01'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)