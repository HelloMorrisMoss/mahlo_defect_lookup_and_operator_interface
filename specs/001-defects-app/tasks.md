**Propagated**: 2026-08-20 — Added task for defect request attribution.

# Tasks: Defects App

**Feature**: Defects App

## Implementation Tasks

### [Story] UI Layout & Components

- [x] Create `datepicker.py` widget with `DatePickerRange` | `app/defects_app/widgets/datepicker.py`
- [x] Create `data_table.py` with `DataTable` and conditional styling | `app/defects_app/widgets/data_table.py`
- [x] Assemble components in `layout.py` | `app/defects_app/layout.py`

### [Story] Interactive Logic

- [x] Implement `update_table` callback for date range filtering | `app/pages/defects.py`
- [x] Implement `update_selected_row_color` for active row highlighting | `app/pages/defects.py`
- [x] Register page route `/defects` | `app/pages/defects.py`

### [Story] Usage Tracking
- [ ] T001 Update `get_defects` to include `source` parameter in requests | `app/connections.py`

## Verification Tasks

- [ ] Add unit tests for `get_defects` data processing (Gap)
- [ ] Add Dash testing (Selenium/Cypress) for callback verification (Gap)
