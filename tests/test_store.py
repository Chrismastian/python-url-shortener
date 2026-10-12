from short import store


def test_shorten_creates_code():
    mapping = {}
    code = store.shorten(mapping, "https://a.com")
    assert code in mapping
    assert mapping[code] == "https://a.com"


def test_shorten_same_url_reuses_code():
    mapping = {}
    code1 = store.shorten(mapping, "https://a.com")
    code2 = store.shorten(mapping, "https://a.com")
    assert code1 == code2
    assert len(mapping) == 1


def test_get_url():
    mapping = {"abc": "https://a.com"}
    assert store.get_url(mapping, "abc") == "https://a.com"
    assert store.get_url(mapping, "zzz") is None


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "data.json"
    store.save({"abc": "https://a.com"}, path)
    assert store.load(path) == {"abc": "https://a.com"}


def test_load_missing_file(tmp_path):
    assert store.load(tmp_path / "nope.json") == {}
