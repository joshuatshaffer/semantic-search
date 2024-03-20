import psycopg2


def db_connect():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="kjguvkuvrstyt",
        host="localhost",
        port="5432",
    )
