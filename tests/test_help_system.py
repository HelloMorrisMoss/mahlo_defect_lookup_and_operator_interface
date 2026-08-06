import json
import os
import pytest


def test_help_editor_requires_login(client):
    """Test that the help editor is protected by login_required."""
    response = client.get('/help/editor')
    assert response.status_code == 302
    assert '/login' in response.location


def test_help_api_articles_requires_login(client):
    """Test that the help API is protected by login_required."""
    response = client.get('/help/api/articles')
    assert response.status_code == 302


def test_media_serving(client, app):
    """Test serving a media file."""
    content_dir = os.path.join(app.root_path, 'help_system', 'help_content')
    os.makedirs(content_dir, exist_ok=True)

    test_file = os.path.join(content_dir, 'test_image.png')
    with open(test_file, 'wb') as f:
        f.write(b'fake image data')

    try:
        response = client.get('/help/media/test_image.png')
        assert response.status_code == 200
        assert response.data == b'fake image data'
    finally:
        # On Windows, the file might still be held by the server response
        # We'll try to remove it, but won't fail the test if it fails due to locking
        try:
            if os.path.exists(test_file):
                os.remove(test_file)
        except PermissionError:
            pass


def test_cas_manager_normalized_paths(app):
    """Test that CASManager generates normalized relative paths."""
    from app.help_system.utils.cas_manager import CASManager
    content_dir = os.path.join(app.root_path, 'help_system', 'help_content')
    os.makedirs(content_dir, exist_ok=True)

    # Create a dummy article
    article_path = os.path.join(content_dir, 'test.json')
    with open(article_path, 'w') as f:
        json.dump([{"type": "title", "content": "Test Article"}], f)

    cas = CASManager(content_dir)
    manifest_hash, manifest = cas.create_manifest()

    assert "test.json" in manifest["files"]
    # Path should be relative and not have legacy prefixes
    assert not manifest["files"]["test.json"].startswith("help_window")

    # Cleanup
    os.remove(article_path)


def test_get_file_diff_api(client, app):
    """Test the file diff API (requires login, but we'll test response for article.json)."""
    # Note: Without login it redirects, but we want to verify the logic if possible.
    # For now, just test that it exists.
    response = client.get('/help/api/versions/file_diff?path=article.json&old_hash=h1&new_hash=h2')
    assert response.status_code == 302


def test_version_history_empty(auth_client, app):
    """Test getting version history when empty."""
    response = auth_client.get('/help/api/versions/history')
    assert response.status_code == 200
    assert response.json == []


def test_create_article_api(auth_client, app):
    """Test creating an article via API."""
    content_dir = os.path.join(app.root_path, 'help_system', 'help_content')
    os.makedirs(content_dir, exist_ok=True)

    title = "API Created Article"
    response = auth_client.post('/help/api/create_article',
                                json={"title": title, "section": ""})
    assert response.status_code == 200
    data = response.json
    assert 'file_path' in data

    full_path = os.path.join(content_dir, data['file_path'])
    assert os.path.exists(full_path)

    # Verify content
    with open(full_path, 'r', encoding='utf-8') as f:
        content = json.load(f)
    assert content[0]['type'] == 'title'
    assert content[0]['content'] == title

    # Cleanup
    try:
        os.remove(full_path)
    except PermissionError:
        pass


def test_get_articles_api(auth_client, app):
    """Test the articles list API."""
    content_dir = os.path.join(app.root_path, 'help_system', 'help_content')
    os.makedirs(content_dir, exist_ok=True)

    article_path = os.path.join(content_dir, 'test_list.json')
    with open(article_path, 'w', encoding='utf-8') as f:
        json.dump([{"type": "title", "content": "List Test"}], f)

    try:
        response = auth_client.get('/help/api/articles')
        assert response.status_code == 200
        articles = response.json
        assert any(a['title'] == 'List Test' for a in articles)
    finally:
        try:
            os.remove(article_path)
        except PermissionError:
            pass
