from __future__ import annotations

"""
Purpose:
    Build and hold application-wide services and settings.

Used By:
    main.py
    MainWindow

Notes:
    MainWindow should create UI widgets only.
    AppContext owns service creation.
"""

from pathlib import Path

from app.config.settings_loader import SettingsLoader
from app.core.app_state import AppState
from app.reports.report_registry import ReportRegistry
from app.services.data_loader import DataLoader
from app.services.db_service import DBService
from app.services.element_service import ElementService
from app.services.exporter import Exporter
from app.services.mainframe_location_service import MainframeLocationService
from app.services.stats_service import StatsService
from app.services.status_marker_service import StatusMarkerService
from app.services.validation_service import ValidationService
from app.ui.theme_manager import ThemeManager


class AppContext:
    def __init__(self, base_dir: str | Path, settings_path: str | Path) -> None:
        self.base_dir = Path(base_dir)
        self.settings_path = Path(settings_path)

        self.settings = SettingsLoader(
            self.settings_path,
        ).load()

        default_input = Path(self.settings["files"]["default_input_file"])

        if not default_input.exists():
            default_input = self.prompt_for_inventory_file()

        self.input_file = Path(default_input)

        self.state = AppState(
            current_xls_path=self.input_file,
        )

        self.ui_settings = self.settings["ui"]
        self.workload_settings = self.settings["workload"]
        self.selection_rules = self.settings["selection_rules"]
        self.archive_pairs = self.settings["type_archive_pairs"]
        self.status_markers = self.settings["status_markers"]
        self.db_settings = self.settings["database"]
        self.required_columns = self.settings["required_columns"]

        self.theme_manager = ThemeManager(
            ui_settings=self.ui_settings,
        )

        self.data_loader = DataLoader(
            file_path=self.input_file,
            required_columns=self.required_columns,
        )
        self.data_loader.load()

        self.db_service = DBService(
            db_settings=self.db_settings,
        )

        self.element_service = ElementService()

        self.status_marker_service = StatusMarkerService(
            status_markers=self.status_markers,
        )

        self.validation_service = ValidationService(
            selection_rules=self.selection_rules,
            archive_pairs=self.archive_pairs,
            status_marker_service=self.status_marker_service,
        )

        self.stats_service = StatsService(
            workload_settings=self.workload_settings,
        )

        self.exporter = Exporter(
            settings=self.settings,
            base_dir=self.base_dir,
        )

        self.report_registry = ReportRegistry(
            stats_service=self.stats_service,
        )

        self.location_service: MainframeLocationService | None = None

    def load_location_file(
        self,
        file_path: str | Path,
    ) -> MainframeLocationService:
        service = MainframeLocationService()
        service.load_file(file_path)

        self.location_service = service

        return service
