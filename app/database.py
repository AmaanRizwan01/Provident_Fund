import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='provident_fund',
            user='root',
            password=''
        )
        if conn.is_connected():
            print("Connected to MySQL database")
            return conn
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None