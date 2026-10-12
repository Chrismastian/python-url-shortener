"""HTTP layer: baca method+URL, panggil store, balas JSON / redirect."""
import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

from short import store


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return None
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def _redirect(self, location):
        # HINT (baris ~27): redirect itu balasan TANPA body.
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()
        pass

    def do_POST(self):
        # Cuma layani POST /shorten, selain itu 404.
        if self.path != "/shorten":
            self._send(404, {"error": "not found"})
            return
 
        body = self._read_body()
        if not body or "url" not in body:
            self._send(400, {"error": "butuh field 'url'"})
            return
 
        mapping = store.load()                       # baca data dari penyimpanan
        code = store.shorten(mapping, body["url"])   # buat kode pendek
        store.save(mapping)                          # simpan lagi
        self._send(201, {"code": code, "url": body["url"]})

    def do_GET(self):
        # GET /<kode> -> redirect ke URL asli.
        code = self.path.lstrip("/")                 # "/aB3xQw" -> "aB3xQw"
        if code == "":
            self._send(404, {"error": "not found"})
            return
 
        mapping = store.load()
        url = store.get_url(mapping, code)
        if url is None:
            self._send(404, {"error": "not found"})
            return
 
        self._redirect(url)


def run(port=8000):
    server = HTTPServer(("localhost", port), Handler)
    print(f"Jalan di http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
