from django.db import connection

def check_db_connection():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print('Database connected', result)
    except Exception as e:
        print("Error connecting to database", e)

check_db_connection()
