from __future__ import annotations

"""
Purpose:
    Load and validate settings.json

Used By:
    main.py

Responsibilities:
    - Confirm settings.json exists.
    - Read JSON settings.
    - Validate required top-level sections exist.
    
Notes:
    This file should not apply business rules.
    This file should not calculate workload.
    This file should not connect to SQL.
"""

import json
from pathlib import Path
from typing import Any

from app.core.validators import validate_required_settings


class SettingsLoader:
    REQUIRED_SECTIONS: set[str] = {
        "database",
        "workload",
        "selection_rules",
        "required_columns",
        "ui",
        "reports",
        "type_archive_pairs",
        "status_markers",
    }

    def __init__(
        self,
        settings_path: str | Path,
    ) -> None:
        self.settings_path: Path = Path(settings_path)

    def load(
        self,
    ) -> dict[str, Any]:
        if not self.settings_path.exists():
            raise FileNotFoundError(f"Settings file nto found: {self.settings_path}.")

        with self.settings_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            settings: dict[str, Any] = json.load(file)

        validate_required_settings(
            settings=settings, required_sections=self.REQUIRED_SECTIONS
        )

        return settings
