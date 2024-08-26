# db_connector.py

import psycopg2
from psycopg2 import pool
from get_env import DBNAME, USER, DB_PASSWORD, HOST, PORT

# You can use connection pooling for better performance
connection_pool = None

def init_db_pool(minconn=1, maxconn=20):
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(minconn, maxconn,
                                                             user=USER,
                                                             password=DB_PASSWORD,
                                                             host=HOST,
                                                             port=PORT,
                                                             database=DBNAME)
        if connection_pool:
            print("Connection pool created successfully")
    except Exception as error:
        print("Error while connecting to PostgreSQL", error)

def get_db_pool():
    global connection_pool
    if connection_pool is None:
        raise Exception("Connection pool is not initialized. Call init_db_pool() first.")
    return connection_pool

def get_db_connection():
    global connection_pool
    if connection_pool:
        return connection_pool.getconn()
    else:
        print("Connection pool is not initialized.")
        return None

def close_db_connection(conn):
    global connection_pool
    if connection_pool:
        connection_pool.putconn(conn)
    else:
        print("Connection pool is not initialized.")

def close_all_connections():
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        print("Connection pool closed.")
