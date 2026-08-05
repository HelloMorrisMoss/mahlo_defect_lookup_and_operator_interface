# Implementation Plan: Operators App

**Feature**: Operators App
**Status**: migrated

## Technical Context

- **Frameworks**: Dash Ag-Grid, Requests, Pandas.
- **Integration**: External REST API for operator data.
- **UI Strategy**: Two-grid layout (Current Operators vs. New Operator Entry).

## Project Structure

- `app/operators_app/`: Main logic and layout.
- `app/pages/operators.py`: Dash page registration.
- `untracked_config/server_address.py`: API endpoint configuration.

## Implementation Phases

### Phase 1: Data Integration

- Implemented `get_operator_data` in `app.connections` (proxied in callbacks).
- Configured API endpoints for `PUT` and `POST` operations.

### Phase 2: Ag-Grid Layout

- Defined `editable_columns` to control user permissions in the grid.
- Implemented `get_operator_layout` with two `dag.AgGrid` instances.
- Added control buttons and state stores (`operator_edits_store`, `new_op_data_store`).

### Phase 3: Callback Logic

- **Save Edits**: Compares grid data with backend data using Pandas merge to identify changes, then sends `PUT`
  requests.
- **New Operator**: Sends `POST` request with data from the entry grid and clears the form.
- **Enable/Disable**: Toggles `date_removed` status for selected rows via `PUT` requests.
- **Filter**: Updates the grid based on the "Show deactivated" checkbox.

## Complexity Assessment

- **Component Count**: 2 Ag-Grids, multiple buttons/checkboxes.
- **Data Flow**: High (Bidirectional communication with external API).
- **Risk**: Dependency on external service availability and performance of delta detection.
