import psycopg2


def db_connect():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="kjguvkuvrstyt",
        host="localhost",
        port="5432",
    )


with db_connect() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT NOW()")
        print(cur.fetchall())
