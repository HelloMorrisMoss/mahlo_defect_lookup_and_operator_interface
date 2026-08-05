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

## Verification
- [ ] Manual test: Login and access `/help/editor`.
- [ ] Manual test: Create a "Test Article" and save it.
- [ ] Manual test: Upload an image to the "Test Article".
- [ ] Manual test: Create a content version with a comment.
- [ ] Manual test: Verify the diff shows the new article and image.
- [ ] Manual test: Publish the new version.
