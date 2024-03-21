from db import db_connect
from foo import shakespeare_lines
from task_log import start_task, end_task
from more_itertools import batched

start_task("Importing sentence_transformers")

from sentence_transformers import SentenceTransformer, util

end_task()


start_task("Loading model")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
end_task()

with db_connect() as conn:
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION if not exists vector;")
        cur.execute("drop table if exists chunks;")
        cur.execute(
            """
                create table chunks (
                    id bigserial primary key,
                    embedding vector (384),
                    file_name text,
                    xpath text,
                    text text
                );
            """
        )

for i, lines in enumerate(batched(shakespeare_lines(), 500)):
    start_task(f"Processing batch {i}")
    sentences = [text for (_, _, text) in lines]

    embeddings = model.encode(sentences)

    with db_connect() as conn:
        for (file_name, xpath, text), embedding in zip(lines, embeddings):
            with conn.cursor() as cur:
                cur.execute(
                    "insert into chunks (embedding, file_name, xpath, text) values (%s, %s, %s, %s);",
                    ([float(e) for e in embedding], file_name, xpath, text),
                )
    end_task()
