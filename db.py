import psycopg
from pgvector.psycopg import register_vector


def db_connect():
    conn = psycopg.connect(
        dbname="postgres",
        user="postgres",
        password="kjguvkuvrstyt",
        host="localhost",
        port="5432",
    )
    register_vector(conn)
    return conn
