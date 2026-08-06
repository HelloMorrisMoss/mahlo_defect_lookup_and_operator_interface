# Spec: Help System (Editor & Versioning)

## Overview
The Help System provides a centralized management hub for creating, editing, and versioning help articles. These articles are intended to be consumed by operational displays (like the Mahlo Popup). 

## User Scenarios
- **Admin edits help articles**: As an admin, I want to use a web-based WYSIWYG editor to manage help content without writing JSON manually.
- **Admin manages media**: As an admin, I want to upload images and videos directly through the editor and have them organized by article category.
- **Admin versions content**: As an admin, I want to create snapshots of the entire help system (versions) and decide which version is "Published" for external subscribers.
- **Admin reviews changes**: As an admin, I want to see a diff of changes between the current draft and previous versions before publishing.

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

## Success Criteria

- [x] Admin can login and access `/help/editor`.
- [x] Articles can be created, edited, and saved.
- [x] Media can be uploaded and correctly referenced in articles.
- [x] Versions can be created, viewed in history, and published.
- [x] Diffs correctly identify added, modified, and removed files between versions.

## History Note
This feature's implementation history was migrated from the `mahlo_popup` repository.
