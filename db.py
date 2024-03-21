import psycopg2
from pgvector.psycopg2 import register_vector


def db_connect():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="kjguvkuvrstyt",
        host="localhost",
        port="5432",
    )
    register_vector(conn)
    return conn
