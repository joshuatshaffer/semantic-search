from http.server import BaseHTTPRequestHandler, HTTPServer

from urllib.parse import urlparse, parse_qs


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        q = query_components["q"][0]
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # TODO: Sanitize q.
        self.wfile.write(
            bytes(
                f"""<!DOCTYPE html>
<html>
    <head>
        <title>Semantic search</title>
    </head>
    <body>
        <form>
            <input type="text" name="q" value="{q}" />
            <input type="submit" />
        </form>
    </body>
</html>
""",
                "utf-8",
            )
        )


if __name__ == "__main__":
    hostName = "localhost"
    serverPort = 8080

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
