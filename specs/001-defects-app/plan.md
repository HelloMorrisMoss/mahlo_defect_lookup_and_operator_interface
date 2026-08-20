**Propagated**: 2026-08-20 — Updated to include defect request attribution when querying mahlo_popup.

# Implementation Plan: Defects App

**Feature**: Defects App
**Status**: migrated

## Technical Context

- **Frameworks**: Dash 2.x, Flask, Dash Bootstrap Components.
- **Data Source**: External database via `app.connections.get_defects`.
- **UI Patterns**: Modular widget structure (`app/defects_app/widgets/`).

## Project Structure

- `app/defects_app/`: Main logic and layout.
- `app/pages/defects.py`: Page registration and route handling.
- `app/connections.py`: Data fetching layer.

## Implementation Phases

### Phase 1: Data & Utilities

- Reconstructed `default_dates.py` to handle initial time windows.
- Verified `get_defects` connectivity in `app/connections.py`.

### Phase 2: UI Components (Widgets)

- Created `datepicker.py` wrapper for `dcc.DatePickerRange`.
- Created `data_table.py` for `dash_table.DataTable` configuration and styling.

### Phase 3: Layout & Callbacks

- Integrated widgets in `layout.py`.
- Implemented reactive callbacks in `callbacks.py` for date filtering and row highlighting.

### Phase 4: Page Registration

- Registered the feature as a Dash page in `app/pages/defects.py`.
- Hooked callbacks into the main app factory in `app/__init__.py`.

### Phase 5: Usage Tracking & Attribution
- Update `get_defects` in `app/connections.py` to pass `source='mahlo_defect_lookup_table'`.

## Complexity Assessment

- **Component Count**: 2 main UI widgets.
- **Callback Depth**: 1 level (Direct Input -> Output).
- **Integration Risk**: Low (Self-contained Dash sub-app).
