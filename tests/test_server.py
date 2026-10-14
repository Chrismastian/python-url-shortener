import json
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer

import pytest

from short import server


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Disable auto-redirect so the 302 can be captured instead of followed."""

    def redirect_request(self, *args, **kwargs):
        return None


@pytest.fixture
def base_url(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    httpd = HTTPServer(("localhost", 0), server.Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://localhost:{httpd.server_port}"
    httpd.shutdown()
    thread.join()


def request(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, e.headers


def test_shorten_then_redirect(base_url):
    # send a long URL
    status, body = request("POST", f"{base_url}/shorten", {"url": "https://a.com"})
    assert status == 201
    code = body["code"]

    # open the code -> must be 302 + Location (do NOT follow)
    opener = urllib.request.build_opener(NoRedirect)
    try:
        opener.open(f"{base_url}/{code}")
        assert False, "should have redirected (302)"
    except urllib.error.HTTPError as e:
        assert e.code == 302
        assert e.headers["Location"] == "https://a.com"


def test_unknown_code_404(base_url):
    status, _ = request("GET", f"{base_url}/missing")
    assert status == 404


def test_bad_post(base_url):
    assert request("POST", f"{base_url}/shorten", {})[0] == 400
    assert request("POST", f"{base_url}/shorten", None)[0] == 400
    assert request("POST", f"{base_url}/salah", {"url": "https://a.com"})[0] == 404
