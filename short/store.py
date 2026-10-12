"""Data layer: peta {kode: url} + simpan ke file JSON."""
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
    """Kode pendek acak, contoh: 'aB3xQw'."""
    return secrets.token_urlsafe(6)


def shorten(mapping, url):
    """Simpan url -> balikin kode. Kalau url sama sudah ada, pakai kode lama."""
    for code, existing in mapping.items():
        if existing == url:
            return code
    code = new_code()
    mapping[code] = url
    return code


def get_url(mapping, code):
    """Balikin url untuk kode, atau None kalau tidak ada."""
    return mapping.get(code)
