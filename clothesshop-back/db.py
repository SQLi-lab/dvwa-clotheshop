import sqlite3
import psycopg2
import os
from psycopg2.extras import RealDictCursor

#DATABASE_TYPE = 'postgres'  # Измените на 'postgres', если используете PostgreSQL
DATABASE_TYPE = 'sqlite'
db_name = str(os.getenv('POSTGRES_DB')).replace("-", "_")

# DATABASE_CONFIG = {
#     'sqlite': {
#         'database': 'pharmacy.db'
#     },
#     'postgres': {
#         'dbname': db_name,
#         'user': os.getenv('POSTGRES_USER'),
#         'password': os.getenv('POSTGRES_PASS'),
#         'host': os.getenv('POSTGRES_HOST'),
#         'port': os.getenv('POSTGRES_PORT')
#     }
# }
DATABASE_CONFIG = {
    'sqlite': {
        'database': 'clothesshop.db'
    },
    'postgres': {
        'dbname': 'pharmacy', # dbname едина, там ток табла другая
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': 5432
    }
}


def get_connection():
    if DATABASE_TYPE == 'sqlite':
        return sqlite3.connect(DATABASE_CONFIG['sqlite']['database'])
    elif DATABASE_TYPE == 'postgres':
        config = DATABASE_CONFIG['postgres']
        return psycopg2.connect(
            dbname=config['dbname'],
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port']
        )

def query_db(query, args=(), one=False):
    conn = get_connection()
    if DATABASE_TYPE == 'sqlite':
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
    else:
        cursor = conn.cursor(cursor_factory=RealDictCursor)  # Используем RealDictCursor для Postgres
    cursor.execute(query, args)
    rv = cursor.fetchall()
    conn.close()

    if DATABASE_TYPE == 'sqlite':
        data = [dict(row) for row in rv]
    else:
        data = rv

    return (data[0] if data else None) if one else data


def execute_db(query, args=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, args)
    conn.commit()
    conn.close()
