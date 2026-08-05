# Plan: Help System Migration & Integration

## Architecture
- **Flask Blueprint**: `app.help_system` registered at `/help`.
- **UI**: 
  - `web_editor.html`: Main SPA for article management.
  - `versioning.html`: Dashboard for snapshot and publishing management.
- **Backend**:
  - `routes.py`: Controller logic for APIs and view rendering.
  - `CASManager`: Service for file-level versioning and deduplication.
  - `ContentVersion` & `BlobMetadata`: Database models for tracking state.

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

### Phase 4: Verification
- [ ] Run the application and verify login access.
- [ ] Test the full article lifecycle (Create -> Edit -> Save -> Media Upload).
- [ ] Test the versioning lifecycle (Create Version -> Diff -> Publish).
