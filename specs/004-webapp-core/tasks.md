# Tasks: Webapp Core & Authentication

**Feature**: Webapp Core

## Implementation Tasks

### [Story] Core Infrastructure

- [x] Implement application factory `create_app` | `app/__init__.py`
- [x] Configure extensions (`db`, `login`, `migrate`) | `app/__init__.py`
- [x] Define `User` model and password hashing | `app/models.py`

### [Story] Authentication Flow

- [x] Create Login and Registration forms | `app/forms.py`
- [x] Implement login/logout/register routes | `app/webapp.py`
- [x] Protect Dash endpoints with `login_required` | `app/__init__.py`

### [Story] Landing Page

- [x] Create Dash home page layout | `app/pages/home.py`
- [x] Configure Dash to use Flask server | `app/__init__.py`

## Verification Tasks

- [ ] Add unit tests for `User` model password hashing (Gap)
- [ ] Add integration tests for login/logout flow (Gap)
- [ ] Verify CSRF protection on registration and login forms (Gap)
