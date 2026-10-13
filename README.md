# python-url-shortener

[![CI](https://github.com/Chrismastian/python-url-shortener/actions/workflows/ci.yml/badge.svg)](https://github.com/Chrismastian/python-url-shortener/actions/workflows/ci.yml)

A simple URL shortener built with the **stdlib `http.server`** (no dependencies) while learning Python: HTTP redirects (302 + Location), a `{code: url}` map, file I/O, and integration testing.

## Usage

```bash
python -m short.server          # runs at http://localhost:8000
```

Then from another terminal:

```bash
# send a long URL -> get a short code
curl -X POST http://localhost:8000/shorten -d '{"url":"https://youtube.com/watch?v=abc123"}'
# {"code": "SggjMAzc", "url": "https://youtube.com/watch?v=abc123"}

# open the code -> redirect to the original URL
curl -L http://localhost:8000/SggjMAzc
```

Data is stored in `data.json` (created automatically).

## Endpoints

| Method | URL | Description | Status |
|--------|-----|-------------|--------|
| POST | `/shorten` | create a short code from a URL | 201 / 400 |
| GET | `/{code}` | redirect to the original URL | 302 / 404 |

## Development

```bash
pip install pytest
pytest
```

## Structure

```
short/
  store.py   # data layer: {code: url} map + persist to JSON
  server.py  # HTTP layer: redirect (302) + reply JSON
tests/
  test_store.py    # unit tests for logic
  test_server.py   # integration test (start server, hit it with urllib)
```
