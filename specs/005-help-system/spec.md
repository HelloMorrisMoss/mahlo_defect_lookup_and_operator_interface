# Spec: Help System (Editor & Versioning)

**Status**: Refined: 2026-08-18 — Refactored link selection to use tree-based workflow.
**Refined**: 2026-08-18 — UI/UX polish for editor and tree view.
**Refined**: 2026-08-18 — Added Media Preview and Tree-based Media Selection functionality.
**Refined**: 2026-08-18 — Refactored Link block to use tree-based selection and renamed "Browse..." to "Select...".

## Overview
The Help System provides a centralized management hub for creating, editing, and versioning help articles. These articles are intended to be consumed by operational displays (like the Mahlo Popup). 

## User Scenarios
- **Admin edits help articles**: As an admin, I want to use a web-based WYSIWYG editor to manage help content without writing JSON manually.
- **Admin manages media**: As an admin, I want to upload images and videos directly through the editor and have them organized by article category.
- **Admin versions content**: As an admin, I want to create snapshots of the entire help system (versions) and decide which version is "Published" for external subscribers.
- **Admin reviews changes**: As an admin, I want to see a diff of changes between the current draft and previous versions before publishing.
- **Admin customizes article icons**: As an admin, I want to set a custom unicode icon for specific articles to make
  them stand out in the list.
- **Admin navigates content efficiently**: As an admin, I want to expand/collapse folders by clicking their names, and
  use a dedicated edit button for folder actions.
- **Admin previews media**: As an admin, I want to click an image or video in the navigation tree to see a preview of it
  alongside the current article I'm editing.
- **Admin selects media from tree**: As an admin, I want to select media for an image or video block by clicking it
  directly in the navigation tree, with real-time validation.
- **Admin selects links from tree**: As an admin, I want to select target articles for link blocks by clicking them
  directly in the navigation tree, replacing the old modal browser.

## Requirements
- **Integrated Auth**: The Help Editor must be accessible only to authenticated users of the Nitto Lakewood Dash App.
- **Content-Addressable Storage (CAS)**: Media and manifests must be stored using SHA-256 hashes in the `blobs/`
  directory to ensure deduplication and integrity.
- **Path Normalization**: All internal article references and manifest entries must use paths relative to the
  `help_content/` root, stripping legacy repository prefixes.
- **Blueprint Isolation**: The help system logic must be isolated in a Flask Blueprint mounted at `/help` to avoid
  interference with Dash components.
- **Navigation Integration**: The editor must be reachable via the main application navigation menu.
- **Dual-Database Support**: Versioning data must be stored in a dedicated `help_versions.db` using SQLAlchemy binds.
- **Article Icons**:
  - Default icon for articles is "ℹ️".
  - Images display "📷" by default.
  - Videos display "🎥" by default.
  - Support an optional "icon" block in the article editor that specifies a unicode symbol for the list view (overrides
    default for articles).
  - This "icon" block should not be visible in the rendered article content.
  - Add an "Add Icon" button to the `add-block-toolbar`.
- **Tree View Navigation**:
  - Folders must display a pencil "✏" edit icon on the right side of the `folder-item` div, visible only on hover.
  - Clicking the pencil icon opens the 'Folder Options' popup.
  - Clicking either the expansion triangle ("▼"/"▶") OR the folder name should toggle the folder open/closed.
  - The `staging` folder must be hidden from the tree view.
- **Image/Video Block Layout**:
  - Add a "Select Existing Media" button next to "Upload Media...".
  - Both buttons must be right-aligned in the entry row.
  - The path text input must fill the remaining horizontal space.
- **Media Preview**:
  - Clicking an image or video in the tree splits the 'Live Preview' pane horizontally.
  - Top half: Article preview (continues showing the currently selected article).
  - Bottom half: Image or video preview.
  - The `preview-header` remains at the top; the media preview does not have its own header.
  - The article remains selected in the tree; the clicked image/video gets a border around its `article-item` div (same
    color as selection).
  - An on-hover close button on the media preview returns the pane to full-height article preview.
  - Selecting a different image/video updates the bottom preview and the border highlight.
- **Tree-based Selection for Destinations**:
  - Use the 'select in tree' functionality for selecting destination folders when:
    - Creating a new article (Enter section).
    - Moving an article ('Move Article').
    - Moving a folder ('Move Folder' from Folder Options).
  - Validation: Ensure the selection for these actions is a folder.
  - Validation for 'Move Folder': Prevent moving a folder into itself or its subfolders.
  - The selection popup should display appropriate titles and messages for each context.

## Success Criteria

- [x] Admin can login and access `/help/editor`.
- [x] Articles can be created, edited, and saved.
- [x] Media can be uploaded and correctly referenced in articles.
- [x] Versions can be created, viewed in history, and published.
- [x] Diffs correctly identify added, modified, and removed files between versions.
- [x] Articles display "ℹ️" by default in the tree view.
- [x] Images display "📷" in the tree view.
- [x] Videos display "🎥" in the tree view.
- [x] Custom icons set via the "icon" block are correctly displayed in the tree view.
- [x] Folders expand/collapse when clicking the name.
- [x] Pencil icon triggers folder options popup.
- [x] `staging` folder is hidden from the tree view.
- [x] Image block layout matches the new right-aligned button requirement.
- [x] Admin can preview images/videos in a split pane by clicking them in the tree.
- [x] Media preview can be closed to return to full article preview.
- [x] Selected media in tree is visually distinguished with a border.
- [x] Media selection for editor blocks uses the tree navigation with validation.
- [x] Article selection for link blocks uses the tree navigation.
- [x] Link block button text is updated to "Select...".
- [x] Destination folder selection for new articles uses the tree navigation.
- [x] Destination folder selection for moving articles uses the tree navigation.
- [x] Destination folder selection for moving folders uses the tree navigation with cycle validation.

## History Note
This feature's implementation history was migrated from the `mahlo_popup` repository.
