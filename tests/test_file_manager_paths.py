import os

from app.help_system.content_manager import ContentManager
from app.help_system.editor.file_manager import get_media_dir, upload_media


def test_get_media_dir_path_correctness(app):
    """
    Test that get_media_dir correctly resolves paths without redundant 'app' segments.
    This guards against regressions where project_root (app.root_path) is joined with 'app' again.
    """
    # app.root_path is typically /path/to/project/app
    project_root = app.root_path

    # Expected content dir is project_root/help_system/help_content
    # (NOT project_root/app/help_system/help_content)
    expected_base = os.path.join(project_root, "help_system", "help_content")

    # 1. Test top-level media dir
    media_dir = get_media_dir(project_root, None)
    expected_media_dir = os.path.join(expected_base, "media")
    assert os.path.normpath(media_dir) == os.path.normpath(expected_media_dir)

    # Verify we don't have redundant 'app' segments
    # On Windows, paths might use backslashes
    norm_media_dir = os.path.normpath(media_dir)
    # It's hard to check for "app/app" exactly if we don't know the full path,
    # but we can check if the tail matches what we expect from the root.
    assert norm_media_dir.endswith(os.path.normpath("app/help_system/help_content/media"))
    # And specifically NOT end with app/app/...
    assert not norm_media_dir.endswith(os.path.normpath("app/app/help_system/help_content/media"))

    # 2. Test article-specific media dir
    article_path = os.path.join(expected_base, "01 - Folder", "Article.json")
    media_dir = get_media_dir(project_root, article_path)
    expected_article_media_dir = os.path.join(expected_base, "01 - Folder", "media")
    assert os.path.normpath(media_dir) == os.path.normpath(expected_article_media_dir)


def test_upload_media_rel_path_correctness(app, tmp_path):
    """
    Test that upload_media returns a relative path starting from help_content.
    """
    project_root = app.root_path
    content_dir = os.path.join(project_root, "help_system", "help_content")
    os.makedirs(content_dir, exist_ok=True)

    # Create a dummy article and source file
    article_path = os.path.join(content_dir, "test_article.json")
    source_file = tmp_path / "test.png"
    source_file.write_bytes(b"dummy")

    rel_path = upload_media(project_root, article_path, str(source_file))

    # The returned path should be relative to help_content
    # e.g. "media/test.png"
    assert not rel_path.startswith("app/")
    assert not rel_path.startswith("help_system/")
    assert rel_path.startswith("media/")

    # Verify the file actually exists in the right place
    dest_path = os.path.join(content_dir, rel_path)
    assert os.path.exists(dest_path)

    # Cleanup
    if os.path.exists(dest_path):
        os.remove(dest_path)


def test_content_manager_resolve_path_regression(app):
    """
    Test that ContentManager correctly resolves paths starting with the new prefixes.
    """
    content_dir = os.path.join(app.root_path, "help_system", "help_content")
    os.makedirs(content_dir, exist_ok=True)
    cm = ContentManager(content_dir)

    test_article = "test_resolve.json"
    abs_article_path = os.path.join(content_dir, test_article)
    with open(abs_article_path, 'w') as f:
        f.write("[]")

    try:
        # Test with the new project-relative prefix
        path_with_prefix = f"app/help_system/help_content/{test_article}"
        resolved = cm.resolve_resource_path(path_with_prefix)
        assert os.path.normpath(resolved) == os.path.normpath(abs_article_path)

        # Test with another new variant
        path_with_prefix2 = f"help_system/help_content/{test_article}"
        resolved2 = cm.resolve_resource_path(path_with_prefix2)
        assert os.path.normpath(resolved2) == os.path.normpath(abs_article_path)
    finally:
        if os.path.exists(abs_article_path):
            os.remove(abs_article_path)
