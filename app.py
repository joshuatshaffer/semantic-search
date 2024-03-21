from flask import Flask, render_template, request, url_for
from db import db_connect
from embedding import load_embedding_model

app = Flask(__name__)


@app.route("/")
def search():
    q = request.args.get("q")
    if q is None:
        q = ""
    q = q.strip()

    canonical_url = url_for("search", q=q if q else None)

    if len(q) > 0:
        query_embedding = load_embedding_model().encode(q)
        with db_connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        SELECT file_name, xpath, text, embedding
                        FROM chunks
                        ORDER BY embedding <-> %s, id
                        LIMIT 10;
                    """,
                    (query_embedding,),
                )
                results = cur.fetchall()
    else:
        results = []

    return render_template(
        "search_page.html", q=q, results=results, canonical_url=canonical_url
    )
