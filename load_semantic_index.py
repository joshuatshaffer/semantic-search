from db import db_connect
from task_log import start_task, end_task
from lxml import etree
import sys


cached_model = None


def load_model():
    global cached_model
    if cached_model is None:
        start_task("Importing sentence_transformers")

        from sentence_transformers import SentenceTransformer

        end_task()

        start_task("Loading model")
        cached_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        end_task()

    return cached_model


def load_play(file_name):
    start_task("Loading lines")
    tree = etree.parse("shaks200/" + file_name)
    lines = [
        (
            str(tree.getpath(line)),
            str(line.text),
        )
        for line in tree.findall("//SPEECH/LINE")
    ]
    end_task()

    model = load_model()

    start_task("Computing embeddings")
    embeddings = model.encode([text for (_, text) in lines])
    end_task()

    start_task("Writing to database")
    with db_connect() as conn:
        with conn.cursor() as cur:
            for (xpath, text), embedding in zip(lines, embeddings):
                cur.execute(
                    "insert into chunks (embedding, file_name, xpath, text) values (%s, %s, %s, %s);",
                    ([float(e) for e in embedding], file_name, xpath, text),
                )
    end_task()


if __name__ == "__main__":
    for file_name in sys.argv[1:]:
        if not file_name.endswith(".xml"):
            continue
        load_play(file_name)
