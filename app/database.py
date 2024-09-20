import psycopg
import time
from typing import Tuple
from .config import settings

def get_db() -> Tuple:
    while True:
        try:
            # Establish connection
            conn = psycopg.connect(
                host=settings.database_hostname, 
                port=settings.database_port,
                dbname=settings.database_name, 
                user=settings.database_username, 
                password=settings.database_password
            )
            cur = conn.cursor()
            print('Database connection successful.')
            return conn, cur  # Return the connection and cursor
        except psycopg.Error as error:
            print('Connecting to database failed.')
            print('Error:', error)
            time.sleep(2)

def close_db(conn, cur):
    if cur:
        cur.close()
    if conn:
        conn.close()
    print('Database connection closed.')