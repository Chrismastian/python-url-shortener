"""Data layer: {code: url} map + persist to a JSON file."""
import json
import secrets
from pathlib import Path

DATA_FILE = Path("data.json")


def load(path=DATA_FILE):
    if not path.exists():
        return {}
    return json.loads(path.read_text("utf-8"))


def save(mapping, path=DATA_FILE):
    path.write_text(json.dumps(mapping, indent=2), "utf-8")


def new_code():
    """Random short code, e.g. 'aB3xQw'."""
    return secrets.token_urlsafe(6)


def shorten(mapping, url):
    """Store url -> return its code. If the same url already exists, reuse its code."""
    for code, existing in mapping.items():
        if existing == url:
            return code
    code = new_code()
    mapping[code] = url
    return code


def get_url(mapping, code):
    """Return the url for a code, or None if missing."""
    return mapping.get(code)
