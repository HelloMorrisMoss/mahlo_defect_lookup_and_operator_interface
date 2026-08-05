# Feature Specification: Webapp Core & Authentication

**Feature Branch**: `n/a` (migrated)
**Created**: 2026-08-05
**Status**: migrated

## Description

The core Flask application infrastructure, including user authentication (login, logout, registration) and the primary
Dash landing page.

## User Scenarios

1. **User Login**: As a registered user, I want to securely log in to the application so I can access the dashboards.
2. **User Registration**: As a new operator or supervisor, I want to create a new account so I can use the system.
3. **Secure Access**: As a site administrator, I want to ensure that all dashboards are protected and only accessible to
   authenticated users.

## Technical Requirements

### Flask Routes

- `/`: Index page rendering `index.html`.
- `/login/`: Handles user authentication via `LoginForm`.
- `/logout/`: Terminates the user session.
- `/register/`: Allows creation of new user accounts via `RegistrationForm`.

### Data Model & Schema

- `User` model: Stores `username` and `password_hash`.
- Uses Flask-SQLAlchemy for database interactions and Flask-Login for session management.

### Dash Integration

- Dash multi-page plugin is enabled and the home page is registered at `/`.
- All Dash views are protected by a `login_required` decorator in the app factory.

## Success Criteria

- [x] Users can successfully register and then log in with their credentials.
- [x] Unauthenticated users are redirected to the login page when attempting to access `/dashboard/`.
- [x] Password security is maintained using Werkzeug password hashing.

## Assumptions

- SQLite is used as the primary database for user storage.
- The `migrations/` directory contains the necessary schema evolution scripts.
