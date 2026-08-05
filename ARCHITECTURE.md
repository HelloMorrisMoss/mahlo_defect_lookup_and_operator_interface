# Architecture Documentation

## Overview

This project is a monolithic web application that integrates Plotly Dash into a Flask server. It serves as a tool for
defect lookup and operator management, providing both standard web routes (Flask) and interactive data dashboards (
Dash).

## Tech Stack

- **Primary Language**: Python 3.11+
- **Web Framework**: Flask (Backend) & Plotly Dash (Frontend/Interactive Dashboards)
- **UI Components**: Dash Bootstrap Components (DBC) & Dash Ag-Grid
- **Database**: SQLite (Local Authentication and Help System versioning)
- **External APIs**: Interacts with Mahlo popup server and other services for business data.
- **ORM**: SQLAlchemy (via Flask-SQLAlchemy with multiple binds)
- **Migrations**: Flask-Migrate (Alembic)
- **Package Manager**: `uv`
- **WSGI Server**: Waitress

## Architectural Patterns

### 1. Integrated Monolith

The application follows an "Integrated Dash on Flask" pattern. The Flask server acts as the primary container, handling:

- Authentication (Flask-Login)
- Application Factory (`create_app` in `app/__init__.py`)
- Shared Extensions (DB, Migrate, Login)
- Base HTML Templates (Flask `render_template`)

Dash apps are registered as sub-applications within the Flask server's context, sharing the same underlying server
instance and session.

### 2. Modular Dash Apps

Dash functionality is partitioned into sub-packages within the `app/` directory:

- `app/defects_app/`: Logic and layout for defect tracking.
- `app/operators_app/`: Logic and layout for operator management.
- `app/pages/`: Multi-page registry for Dash `use_pages`.

### 3. Help System Blueprint

The application includes a Help System integrated as a Flask Blueprint (`/help`). This system provides:

- **Article Editor**: A web-based interface for managing help content in JSON format.
- **Versioning**: A Content-Addressable Storage (CAS) based versioning system for articles and media.
- **Media Serving**: Dedicated routes for serving images and videos referenced in help articles.
- **Authentication**: Secured via the same Flask-Login session as the rest of the application.

### 4. Data Integration Strategy

- **Local Persistence**:
  - `app.db`: User accounts and authentication data.
  - `help_versions.db`: Version history and metadata for the Help System (managed via SQLAlchemy binds).
- **External Data**: Defect records and operator data are fetched dynamically from external REST APIs (defined in
  `app/connections.py`).
- **Unified Interface**: Dash callbacks use `app.connections` to abstract the data source, whether it's local or remote.

## Directory Structure

- `dashapp.py`: Production entry point using Waitress.
- `app/`: Core application package.
    - `__init__.py`: App factory and Dash registration.
    - `webapp.py`: Flask blueprints and routes (Login, Register, Logout).
    - `models.py`: SQLAlchemy database models (User).
    - `extensions.py`: Initialized Flask extensions.
    - `connections.py`: Data fetchers for external APIs.
  - `help_system/`: Flask Blueprint for the integrated Help System.
    - `help_content/`: Storage for articles and media blobs.
    - `defects_app/`: Defect-specific Dash logic.
    - `operators_app/`: Operator-specific Dash logic.
    - `pages/`: Registry for Dash `use_pages`.
- `multipage_app.py`: Navigation bar and main Dash layout configuration.
- `config.py`: Environment-based configuration loader.
- `untracked_config/`: Local environment settings (database URLs, keys, API addresses).
- `migrations/`: Database schema versioning.

## Data Flow

1. **Request**: User accesses a route (e.g., `/dashboard/defects`).
2. **Auth**: Flask-Login intercepts the request if the route is protected.
3. **Routing**: Flask serves the initial Dash index page.
4. **Dash Initialization**: Dash loads the layout from `multipage_app.py` and the specific page from `app/pages/`.
5. **Interaction**: User interacts with a Dash component (e.g., Ag-Grid).
6. **Callbacks**: Dash triggers a callback in `app/[sub_app]/callbacks.py`.
7. **Data Access**: The callback calls a function in `app/connections.py`.
8. **API/DB Call**: `connections.py` makes a `requests` call to an external service or queries SQLite via SQLAlchemy
   models.
9. **Update**: Dash updates the UI reactively.

## Authentication & Security

- **Flask-Login**: Used for session management.
- **Protected Views**: Dash views are wrapped with `login_required` during registration in `app/__init__.py`.
- **Environment Variables**: Sensitive data (SECRET_KEY, DATABASE_URL) and API addresses are stored in `.env` and
  `untracked_config/`.

## Development Workflow

- **Spec-Driven Development**: The project uses `speckit` located in `.specify/`.
- **Dependencies**: Managed via `uv`. Use `uv add` for new packages.
- **Database**: Use `flask db migrate` and `flask db upgrade` for schema changes affecting the local `app.db`.
