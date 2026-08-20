# Tasks: Help System Migration

## Implementation Polish (Refined 2026-08-18)

- [x] Default article icon changed to "ℹ️".
- [x] Image icon "📷" and Video icon "🎥" added for media files in the tree view.
- [x] Custom "icon" block support added to editor and backend.
- [x] "Add Icon" button in `add-block-toolbar`.
- [x] Folder "pencil" icon for options popup (sticky right, visible on hover).
- [x] Folder name/triangle both toggle expansion.
- [x] `staging` folder hidden from tree view.
- [x] Image block: right-aligned buttons + "Select Existing Media".
- [x] Image block: path input flex fill.
- [x] Split-pane media preview in `preview-pane`.
- [x] On-hover close button for media preview.
- [x] Border highlight for selected media in tree.
- [x] Tree-based media selection popup (non-modal).
- [x] Media type validation in selection workflow.
- [x] Refactor link block article selection to use tree-integrated workflow.
- [x] Rename link block "Browse..." button to "Select...".
- [x] Generalize tree selection state in `web_editor.js`.
- [x] Implement folder selection support in `renderTreeNode`.
- [x] Refactor `createNewArticle` to use tree selection for destination.
- [x] Refactor `moveArticle` to use tree selection.
- [x] Refactor `moveFolderPrompt` to use tree selection.
- [x] Implement cycle validation for folder moves (prevent moving into self/descendants).
- [x] Fix `web_editor.html` to use `cancelSelection()` for the selection popup.

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
- [x] Manual test: Create a "Test Article" and save it.
- [x] Manual test: Upload an image to the "Test Article".
- [x] Manual test: Create a content version with a comment.
- [x] Manual test: Verify the diff shows the new article and image.
- [x] Manual test: Publish the new version.
- [x] Manual test: Verify tree-based link selection works and updates block.
