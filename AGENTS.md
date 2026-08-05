# Application Agents

This project uses a modular monolith architecture. Development responsibilities are divided among the following agents.

## 1. Webapp Agent

- **Ownership**: `app/webapp.py`, `app/models.py`, `app/forms.py`, `app/extensions.py`, `app/connections.py`,
  `app/templates/`
- **Responsibilities**: Flask routes, authentication, database models, external API connections, and server-side
  templates.
- **Interactions**: Provides the data models and authentication context for Dash sub-apps.

## 2. Defects App Agent

- **Ownership**: `app/defects_app/`
- **Responsibilities**: Logic and layout for the defect lookup tool.
- **Interactions**: Uses SQLAlchemy models from `app/models.py`.

## 3. Operators App Agent

- **Ownership**: `app/operators_app/`
- **Responsibilities**: Logic and layout for operator management.
- **Interactions**: Uses SQLAlchemy models from `app/models.py`.

## 4. Platform Agent

- **Ownership**: `app/__init__.py`, `app/pages/`, `multipage_app.py`, `dashapp.py`, `config.py`, `pyproject.toml`,
  `uv.lock`
- **Responsibilities**: Application orchestration, navigation, configuration, Dash page registry, and dependency
  management.
- **Interactions**: Integrates all sub-apps into the main Flask/Dash server.

## 5. Cert Lookup Agent

- **Ownership**: `app/cert_lookup/`
- **Responsibilities**: Logic and layout for the certificate lookup tool.
- **Interactions**: Uses SQLAlchemy models from `app/models.py` and external connections.

## 6. Help System Agent

- **Ownership**: `app/help_system/`
- **Responsibilities**: Management of help articles, media, and content versioning.
- **Interactions**: Uses SQLAlchemy binds for `help_versions.db` and integrated auth from the Webapp Agent.

## Communication Rules

- Sub-apps should remain decoupled from each other.
- Shared logic (e.g., logging, database access) must reside in the `app/` root or a dedicated `shared/` module (if
  created).
- All UI components should follow the styling defined in `multipage_app.py`.
