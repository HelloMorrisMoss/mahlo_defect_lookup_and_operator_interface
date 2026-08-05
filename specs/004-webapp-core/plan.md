# Implementation Plan: Webapp Core & Authentication

**Feature**: Webapp Core
**Status**: migrated

## Technical Context

- **Frameworks**: Flask, Flask-Login, Flask-SQLAlchemy, Flask-WTF.
- **Security**: Werkzeug password hashing, `login_required` decorators.
- **Project Structure**: Monolith architecture with Dash integrated via `dash.Dash(server=flask_app)`.

## Project Structure

- `app/__init__.py`: App factory and extension initialization.
- `app/webapp.py`: Flask blueprint and route handlers.
- `app/models.py`: Database models (User).
- `app/forms.py`: WTForms for Login and Registration.
- `app/templates/`: Jinja2 templates for auth pages.

## Implementation Phases

### Phase 1: Core Factory & Extensions

- Implemented `create_app` factory.
- Initialized `db`, `login`, and `migrate` extensions.

### Phase 2: Data Models

- Created `User` model with `UserMixin` and password hashing methods.
- Configured SQLite database URI in `config.py`.

### Phase 3: Authentication Logic

- Implemented `LoginForm` and `RegistrationForm`.
- Created Blueprint routes for `/login/`, `/logout/`, and `/register/`.
- Configured `login_loader` for session restoration.

### Phase 4: Dash Integration & Security

- Configured Dash to use the Flask server.
- Implemented `_protect_dashviews` to programmatically apply `login_required` to all Dash endpoints.
- Set up `app/pages/home.py` as the default Dash landing page.

## Complexity Assessment

- **Component Count**: 4 core Flask routes, 1 User model, 2 Forms.
- **Risk**: Security of the `/register/` endpoint and session persistence.
