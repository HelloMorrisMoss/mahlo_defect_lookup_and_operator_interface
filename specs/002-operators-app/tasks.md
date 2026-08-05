# Tasks: Operators App

**Feature**: Operators App

## Implementation Tasks

### [Story] UI Layout with Ag-Grid

- [x] Configure `editable_columns` mapping | `app/operators_app/layout.py`
- [x] Implement main `AgGrid` for current operators | `app/operators_app/layout.py`
- [x] Implement entry `AgGrid` for new operators | `app/operators_app/layout.py`
- [x] Add control buttons and status checkbox | `app/operators_app/layout.py`

### [Story] CRUD Operations & Logic

- [x] Implement `save_operator_edits` with delta detection | `app/operators_app/callbacks.py`
- [x] Implement `save_new_operator` with API POST | `app/operators_app/callbacks.py`
- [x] Implement `disable_or_enable_selected_operator` | `app/operators_app/callbacks.py`
- [x] Implement `show_hide_deactivated_operators` filter | `app/operators_app/callbacks.py`
- [x] Register page route `/operators` | `app/pages/operators.py`

## Verification Tasks

- [ ] Add error handling for API timeouts/failures (Gap)
- [ ] Implement confirmation dialogs before saving/deleting (Gap)
- [ ] Add unit tests for delta detection logic (Gap)
