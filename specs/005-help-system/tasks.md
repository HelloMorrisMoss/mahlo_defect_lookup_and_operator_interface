# Tasks: Help System Migration

## Migration
- [x] Create feature branch `feature/migrate-help-system`.
- [x] Extract `help_window` history via `git subtree split`.
- [x] Merge unrelated histories and resolve conflicts.
- [x] Move files to `app/help_system/` using `git mv`.

## Implementation
- [x] Implement `ContentVersion` and `BlobMetadata` in `app/models.py`.
- [x] Initialize `Blueprint` in `app/help_system/__init__.py`.
- [x] Implement all API and View routes in `app/help_system/routes.py`.
- [x] Refactor `app/help_system/editor/file_manager.py` for new paths.
- [x] Update `web_editor.html` and `versioning.html` templates.
- [x] Update `web_editor.js` to use relative API paths.
- [x] Register Blueprint in `app/__init__.py`.
- [x] Add link to `multipage_app.py` navbar.

## Bug Fixes

- [x] Fix "Publishing" button visibility in `web_editor.html`.
- [x] Fix `web_editor.js` template literal syntax for article loading.
- [x] Configure `SQLALCHEMY_BINDS` for `help_versions.db` in `config.py`.
- [x] Apply `__bind_key__ = 'help_system'` to help system models.
- [x] Fix `.env` syntax error and improve `config.py` SQLite path handling.
- [x] Fix 404 for media by serving from `help_content` instead of `blobs`.
- [x] Normalize JSON paths to be relative to `help_content` (strip legacy prefixes).
- [x] Implement `<video>` and functional links in `web_editor.js` preview.

## Verification

- [x] Manual test: Login and access `/help/editor`.
- [x] Manual test: Verify images and videos render correctly in preview.
- [x] Manual test: Verify article links in preview are functional.
- [x] Manual test: Verify "Publishing" button is visible in the sidebar header.
- [ ] Manual test: Create a "Test Article" and save it.
- [ ] Manual test: Upload an image to the "Test Article".
- [ ] Manual test: Create a content version with a comment.
- [ ] Manual test: Verify the diff shows the new article and image.
- [ ] Manual test: Publish the new version.
