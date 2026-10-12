# python-url-shortener

[![CI](https://github.com/Chrismastian/python-url-shortener/actions/workflows/ci.yml/badge.svg)](https://github.com/Chrismastian/python-url-shortener/actions/workflows/ci.yml)

URL shortener sederhana pakai **stdlib `http.server`** (tanpa dependency) untuk belajar Python: HTTP redirect (302 + Location), peta `{kode: url}`, file I/O, dan testing integrasi.

## Cara pakai

```bash
python -m short.server          # jalan di http://localhost:8000
```

Lalu dari terminal lain:

```bash
# kirim URL panjang -> dapat kode pendek
curl -X POST http://localhost:8000/shorten -d '{"url":"https://youtube.com/watch?v=abc123"}'
# {"code": "SggjMAzc", "url": "https://youtube.com/watch?v=abc123"}

# buka kode -> dialihkan ke URL asli
curl -L http://localhost:8000/SggjMAzc
```

Data disimpan di `data.json` (dibuat otomatis).

## Endpoint

| Method | URL | Fungsi | Status |
|--------|-----|--------|--------|
| POST | `/shorten` | bikin kode pendek dari URL | 201 / 400 |
| GET | `/{kode}` | redirect ke URL asli | 302 / 404 |

## Development

```bash
pip install pytest
pytest
```

## Struktur

```
short/
  store.py   # data layer: peta {kode: url} + simpan ke JSON
  server.py  # HTTP layer: redirect (302) + balas JSON
tests/
  test_store.py    # unit test logic
  test_server.py   # integration test (start server, tembak pakai urllib)
```
