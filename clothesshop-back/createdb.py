import psycopg2


def execute_sql(file_path, db_name, user, password, host='localhost', port=5432):
    # Подключение к базе данных
    conn = psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = conn.cursor()

    # Чтение SQL-скрипта
    with open(file_path, 'r', encoding='utf-8') as f:
        sql = f.read()

    # Выполнение SQL-запросов
    try:
        cursor.execute(sql)
        conn.commit()
        print(f"Executed script: {file_path}")
    except Exception as e:
        print(f"Error executing {file_path}: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


# Выполнение скриптов
execute_sql('scripts/output_database_structure.sql', 'pharmacy_db', 'your_user', 'your_password')
execute_sql('scripts/output_data.sql', 'pharmacy_db', 'your_user', 'your_password')
