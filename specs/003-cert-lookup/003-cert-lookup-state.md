# Feature State: Cert Lookup

**Status**: On Hold / Incomplete

## Findings

During the brownfield migration analysis, the following issues were identified in the `app/cert_lookup/` directory:

1. **Incomplete Development**: The feature appears to have been permanently put on hold during development.
2. **Broken Imports**:
    - `from app.cert_lookup.data_loading.customer_specification_list import csl_df`
    - `from app.cert_lookup.searching import fuzzy_filter_df`
      These modules (`data_loading` and `searching`) are missing from the project, causing the code to be
      non-functional.
3. **Orphaned Components**:
    - The feature is not registered in the main Dash app factory (`app/__init__.py`).
    - There is no entry point in `app/pages/`, meaning it is not accessible via the UI.
4. **Redundant Logic**:
    - The widgets in `app/cert_lookup/widgets/` (e.g., `data_table.py`) are mostly copy-pasted from the `defects_app`
      and still contain references to "defects".

## Recommendation

This feature should remain excluded from the SDD workflow until a decision is made to resume development, at which point
it will require significant refactoring and completion of missing modules.
