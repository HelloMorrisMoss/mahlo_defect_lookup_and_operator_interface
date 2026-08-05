# Dash on Flask Constitution

## Core Principles

### I. Integrated Monolith

The project is a monolithic application where Dash is integrated into a Flask server. Flask handles authentication,
session management, and base routing, while Dash provides interactive data visualizations and tools.

### II. Component-Based Dash Development

Dash applications must be modular. Layouts and callbacks should be separated into their respective sub-packages (e.g.,
`app/defects_app/`, `app/operators_app/`). Use `dash-bootstrap-components` for UI consistency and `dash-ag-grid` for
data tables.

### III. Database Integrity with SQLAlchemy

All data access must go through SQLAlchemy models defined in `app/models.py`. Direct SQLite queries are discouraged.
Database migrations must be managed via `Flask-Migrate`.

### IV. Environment-Aware Configuration

Sensitive information and environment-specific settings must reside in `.env` or the `untracked_config/` directory. Use
`config.py` to load these settings.

### V. Package Management with `uv`

`uv` is the primary package manager. Use `uv.lock` for reproducible environments. Always use `uv run` for executing
scripts and `uv add` for new dependencies.

## Coding Standards

### Naming Conventions

- **Python Files/Directories**: `snake_case` (e.g., `defects_app`, `callbacks.py`).
- **Variables/Functions**: `snake_case`.
- **Classes**: `PascalCase`.
- **Dash Component IDs**: `snake_case` or `kebab-case` (consistency within a module is required).

### Directory Structure

- `app/`: Main application source.
- `app/webapp.py`: Flask-specific routes and blueprints.
- `app/help_system/`: Integrated help article management and versioning system.
- `app/[sub_app]/`: Integrated Dash apps.
- `migrations/`: Database migration scripts.
- `untracked_config/`: Local configuration templates and overrides.
- `ARCHITECTURE.md`: High-level system design and tech stack documentation.

## Development Workflow

### Feature Implementation

1. Define SQLAlchemy models if schema changes are needed.
2. Implement Flask routes or Dash layouts.
3. Register Dash callbacks in the appropriate sub-app.
4. Update navigation in `multipage_app.py` if adding a new page.

### Quality Gates

- Code must follow PEP 8 standards.
- All new dependencies must be added via `uv`.
- Migrations must be generated and tested for schema changes.

## Governance

This constitution and the `ARCHITECTURE.md` file serve as the primary guidelines for development within this project.
Amendments require documentation in `.specify/memory/` and updates to these files.

**Version**: 1.0.3 | **Ratified**: 2026-08-05 | **Last Amended**: 2026-08-05
