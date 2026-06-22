from __future__ import annotations

"""
Purpose:
    Application dependency container.

Used By:
    main.py

Responsibilities:
    - Hold loaded settings.
    - Hold application state.
    - Hold shared configuration used by services.

Notes:
    This is not a service loader.
    This is simply a strongly-typed configuration container.
"""


from dataclasses import dataclass

from app.core.app_state import AppState


@dataclass(slots=True)
class AppContext:
    settings: dict

    state: AppState

    required_columns: list[str]

    type_categories: dict

    types_per_hour_per_thread: dict

    archive_pairs: list[list[str]]

    selection_rules: dict

    status_markers: dict

    sql_settings: dict

    ui_settings: dict

    report_settings: dict

    @property
    def do_not_move_markers(self) -> list[str]:
        return self.status_markers.get("do_not_move", [])

    @property
    def prod_markers(self) -> list[str]:
        return self.status_markers.get("already_in_prod", [])

    @property
    def qual_markers(self) -> list[str]:
        return self.status_markers.get("already_in_qual", [])
