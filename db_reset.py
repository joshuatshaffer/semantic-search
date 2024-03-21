from db import db_connect


def db_reset():
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cur.execute("DROP TABLE IF EXISTS chunks;")
            cur.execute(
                """
                    CREATE TABLE chunks (
                        id bigserial PRIMARY KEY,
                        embedding vector(384),
                        file_name text NOT NULL,
                        xpath text NOT NULL,
                        text text,
                        UNIQUE (file_name, xpath)
                    );
                """
            )


if __name__ == "__main__":
    db_reset()
