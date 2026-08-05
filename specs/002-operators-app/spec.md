# Feature Specification: Operators App

**Feature Branch**: `n/a` (migrated)
**Created**: 2026-08-05
**Status**: migrated

## Description

A Dash sub-app for managing operator information, including names, initials, and certification status for specific
laminators.

## User Scenarios

1. **Operator Overview**: As an administrator, I want to see a list of all current operators and their certification
   status at a glance.
2. **Inline Editing**: As an administrator, I want to edit operator details (e.g., certification status) directly in the
   table and save changes in bulk.
3. **Adding Operators**: As an administrator, I want a dedicated area to input new operator data and add them to the
   system.
4. **Deactivation Management**: As an administrator, I want to disable or enable operators and toggle the visibility of
   deactivated records.

## Technical Requirements

### Dash Components

- `dash_ag_grid.AgGrid`: Primary tool for data display and editing (`id='operator_ag_grid'` and
  `id='new_operator_ag_grid'`).
- `dbc.Checkbox`: Toggle for showing/hiding deactivated operators.
- `html.Button`: Triggers for saving edits, saving new operators, and toggling status.

### External Integration

- Communicates with an external data service via `PUT` and `POST` requests to `operator_data_address`.

## Success Criteria

- [x] Changes in the main grid are successfully persisted to the backend.
- [x] New operator entries are added and the grid refreshes.
- [x] Operator status (enabled/disabled) can be toggled and is reflected in the UI.

## Assumptions

- `untracked_config/server_address.py` contains the correct API endpoint.
- The backend service handles the logic for `date_added` and `date_removed` when receiving status updates.
