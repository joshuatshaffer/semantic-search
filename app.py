from flask import Flask, Response, render_template, request, url_for
from db import db_connect
from embedding import load_embedding_model
from lxml import etree

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
                        SELECT file_name, xpath, text
                        FROM chunks
                        ORDER BY embedding <-> %s, id
                        LIMIT 10;
                    """,
                    (query_embedding,),
                )
                results = [
                    dict(
                        file_name=file_name,
                        xpath=xpath,
                        text=text,
                        url=url_for(
                            "static",
                            filename=f"shaks200/{file_name}",
                            _anchor=f"xpointer({xpath})",
                        ),
                    )
                    for file_name, xpath, text in cur.fetchall()
                ]
    else:
        results = []

    return render_template(
        "search_page.html", q=q, results=results, canonical_url=canonical_url
    )


@app.route("/play/<file_name>")
def play(file_name):
    tree = etree.parse("static/shaks200/" + file_name + ".xml")

    if request.args.get("xml") is not None:
        return Response(
            "\n".join(
                [
                    '<?xml version="1.0"?>',
                    '<?xml-stylesheet type="text/xsl" href="/static/play.xsl"?>',
                    etree.tostring(tree.getroot(), encoding="unicode"),
                ]
            ),
            mimetype="text/xml",
        )

    transform = etree.XSLT(etree.parse("static/play.xsl"))
    return "<!DOCTYPE html>\n" + str(transform(tree))
