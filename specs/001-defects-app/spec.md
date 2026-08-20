# Feature Specification: Defects App

**Feature Branch**: `track-used-defect-records-table`
**Created**: 2026-08-05
**Status**: Refined
**Refined**: 2026-08-20 — Added requirements for defect request source attribution when querying the popup server.

## Description

A Dash-based dashboard for looking up and visualizing production defects within a specified date range.

## User Scenarios

1. **Date-Based Filtering**: As a production supervisor, I want to select a start and end date so I can review defects
   that occurred during a specific shift or time period.
2. **Data Inspection**: As a quality analyst, I want to view defect details in a sortable and filterable table so I can
   identify patterns or specific problematic lots.
3. **Active Row Highlighting**: As a user, I want the currently selected row to be clearly highlighted so I don't lose
   track of which record I am examining.
4. **Defect Request Attribution**: As a system administrator, I want requesting systems to identify themselves as the source when requesting defect
   records from the central server so that data access can be audited.

## Technical Requirements

### Dash Components

- `dcc.DatePickerRange`: Used for date selection (`id='defect_start_ts_range_picker'`).
- `dash_table.DataTable`: Used for data display (`id='defect_table'`).

### Flask Routes

- Integrated via Dash multi-page plugin (`app/pages/defects.py` mapped to `/defects`).

### Database Schema (SQLAlchemy)

- Queries defect data via `app.connections.get_defects`.
- **API-001**: MUST pass `source=mahlo_defect_lookup_table` when calling the central defect query endpoint.

## Success Criteria

- [x] Date picker correctly triggers table updates.
- [x] Table columns dynamically adjust based on database results.
- [x] Active rows and cells are highlighted using conditional styling.
- [ ] 100% of defect requests from the lookup table are correctly attributed to `mahlo_defect_lookup_table`.

## Assumptions

- The database connection (`app.connections`) is configured and accessible.
- The `get_defects` function returns a Pandas DataFrame compatible with `dash_table`.
