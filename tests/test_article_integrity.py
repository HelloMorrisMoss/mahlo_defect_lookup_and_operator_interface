from app.help_system.utils.article_processor import ensure_article_integrity


def test_ensure_article_integrity_empty():
    data = []
    result = ensure_article_integrity(data, "Default Title")
    assert len(result) == 1
    assert result[0]["type"] == "title"
    assert result[0]["content"] == "Default Title"


def test_ensure_article_integrity_has_title():
    data = [{"type": "title", "content": "Existing Title"}, {"type": "paragraph", "content": "hello"}]
    result = ensure_article_integrity(list(data))
    assert result == data


def test_ensure_article_integrity_moves_title():
    data = [{"type": "paragraph", "content": "hello"}, {"type": "title", "content": "Found Title"}]
    result = ensure_article_integrity(list(data))
    assert result[0]["type"] == "title"
    assert result[0]["content"] == "Found Title"
    assert result[1]["type"] == "paragraph"


def test_ensure_article_integrity_converts_header():
    data = [{"type": "header", "content": "Header as Title"}, {"type": "paragraph", "content": "hello"}]
    result = ensure_article_integrity(list(data))
    assert result[0]["type"] == "title"
    assert result[0]["content"] == "Header as Title"
    assert result[1]["type"] == "paragraph"


def test_ensure_article_integrity_adds_title():
    data = [{"type": "paragraph", "content": "hello"}]
    result = ensure_article_integrity(list(data), "Backup Title")
    assert result[0]["type"] == "title"
    assert result[0]["content"] == "Backup Title"
    assert result[1]["type"] == "paragraph"
