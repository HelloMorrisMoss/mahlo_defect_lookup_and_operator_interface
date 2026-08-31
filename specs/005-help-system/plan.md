# Plan: Help System Migration & Integration

**Refined: 2026-08-31 — Video Comparison in Versioning**
**Refined: 2026-08-18 — UI/UX Polish & Link Selection Refactor**

## Architecture
- **Flask Blueprint**: `app.help_system` registered at `/help`.
- **UI**: 
  - `web_editor.html`: Main SPA for article management.
  - `versioning.html`: Dashboard for snapshot and publishing management.
- **Backend**:
  - `routes.py`: Controller logic for APIs and view rendering.
  - `CASManager`: Service for file-level versioning and deduplication.
  - `ContentVersion` & `BlobMetadata`: Database models for tracking state.

## UI/UX Enhancements (Refined 2026-08-18)

- **Article Icons**: Default to "ℹ️", images to "📷", videos to "🎥", customizable via "icon" block.
- **Tree View**:
  - Pencil icon for folder options (sticky right, visible on hover).
  - Click folder name/triangle to toggle expansion.
  - Hide `staging` folder.
- **Image Editor**:
  - Right-aligned buttons.
  - "Select Existing Media" option.
  - Responsive path input.
- **Media Preview (New)**:
  - Split-pane layout for image/video preview in the editor.
  - Border highlight for selected media in the tree.
  - Integrated close button for media preview.
- **Video Comparison (New 2026-08-31)**:
  - Visual side-by-side comparison for videos in the versioning diff view.
  - Support for `mp4`, `webm`, `ogg`, `mov`, `avi` formats.
- **Tree-based Media & Link Selection (Refined 2026-08-18)**:
  - Interactive tree selection for block media paths and article links.
  - Non-modal popup for validation and confirmation.
  - Link block "Browse..." button renamed to "Select...".
- **Tree-based Selection for Destinations (New)**:
  - Use tree selection for destination folders when creating articles or moving content/folders.
  - Cycle validation for folder moves (prevent moving into self/descendants).

## Data Strategy

- **Dual Databases**:
  - Main application uses `app.db` for user authentication.
  - Help System uses `help_versions.db` for version history and blob metadata.
- **SQLAlchemy Binds**: Configured via `SQLALCHEMY_BINDS` to allow seamless model integration while maintaining separate
  storage files.
- **Storage & Pathing**:
  - JSON-based help articles and binary blobs are stored in `app/help_system/help_content/`.
  - All paths in articles (images, videos, links) are normalized to be relative to the `help_content/` root.
  - Legacy prefixes like `help_window/help_content/` are stripped during migration and enforced for new content.
  - Media files are organized by the article's top-level category folder (e.g., `help_content/Category/media/`).
- **Media Serving**:
  - Media is served via the `/help/media/<path>` route, which maps directly to the `help_content/` directory.
  - This allows the editor preview to show "draft" content accurately.

## Implementation Phases

### Phase 1: Migration & Setup (Completed)
- [x] Extract `help_window` history from `mahlo_popup`.
- [x] Merge into `app/help_system/` in this project.
- [x] Add SQLAlchemy models to `app/models.py`.

### Phase 2: Refactoring (Completed)
- [x] Create Flask Blueprint in `app/help_system/__init__.py`.
- [x] Port `flask_app.py` logic to `app/help_system/routes.py`.
- [x] Secure all routes with `@login_required`.
- [x] Update JS to use relative API paths for Blueprint compatibility.
- [x] Update `file_manager.py` paths to match `app/help_system/help_content`.

### Phase 3: Integration (Completed)
- [x] Register Blueprint in `app/__init__.py`.
- [x] Add "Help System Editor" to Dash navigation.

### Phase 4: Verification (Completed)

- [x] Run the application and verify login access.
- [x] Test the full article lifecycle (Create -> Edit -> Save -> Media Upload).
- [x] Test the versioning lifecycle (Create Version -> Diff -> Publish).
- [x] Verify split-pane media preview.
- [x] Verify tree-based media selection for blocks.

### Phase 5: Media & Link Experience Refinement (Refined 2026-08-18)

- [x] Implement split preview container in `web_editor.html`.
- [x] Implement tree item border highlight for media.
- [x] Implement media selection state machine in `web_editor.js`.
- [x] Replace modal media selector with tree-integrated workflow.
- [x] Refactor link block article selection to use tree-integrated workflow.
- [x] Update link block UI text to "Select...".

### Phase 6: Destination Selection Refinement (2026-08-18)

- [x] Generalize tree selection state in `web_editor.js`.
- [x] Implement folder selection support in `renderTreeNode`.
- [x] Refactor `createNewArticle` to use tree selection for destination.
- [x] Refactor `moveArticle` and `moveFolderPrompt` to use tree selection.
- [x] Implement cycle validation for folder moves.

### Phase 7: Versioning Enhancements (2026-08-31)

- [x] Implement visual video comparison in `versioning.html`.
- [x] Add CSS styling for video elements in diff view.
