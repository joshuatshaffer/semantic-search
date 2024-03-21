import os
from db import db_connect
from embedding import load_embedding_model
from task_log import task
from lxml import etree
from multiprocessing import Pool


def load_play(file_name):
    with task("Loading lines"):
        tree = etree.parse("shaks200/" + file_name)
        lines = [
            (
                str(tree.getpath(line)),
                str(line.text),
            )
            for line in tree.findall("//SPEECH/LINE")
        ]

    model = load_embedding_model()

    with task("Computing embeddings"):
        embeddings = model.encode([text for (_, text) in lines])

    with task("Writing to database"):
        with db_connect() as conn:
            with conn.cursor() as cur:
                for (xpath, text), embedding in zip(lines, embeddings):
                    cur.execute(
                        """
                            INSERT INTO chunks (embedding, file_name, xpath, text)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (file_name, xpath) DO UPDATE SET
                                embedding = EXCLUDED.embedding,
                                text = EXCLUDED.text;
                        """,
                        (embedding, file_name, xpath, text),
                    )


if __name__ == "__main__":
    with Pool(processes=8) as pool:
        pool.map(
            load_play,
            [
                file_name
                for file_name in os.listdir("shaks200")
                if file_name.endswith(".xml")
            ],
        )
