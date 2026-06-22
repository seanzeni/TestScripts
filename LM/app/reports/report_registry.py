from __future__ import annotations

"""
Purpose:
    Central registry for available reports.

Used By:
    ReportsDialog
    MainWindow

Responsibilities:
    - Register all report generators.
    - Provide display names.
    - Create report instances.

Notes:
    Add new reports here instead of modifying the UI.
"""

from app.reports.effort_summary_report import EffortSummaryReport
from app.reports.issues_report import IssuesReport
from app.reports.osg_cops_report import OsgCopsReport
from app.reports.release_estimate_report import ReleaseEstimateReport
from app.reports.release_inventory_report import ReleaseInventoryReport
from app.reports.resync_report import ResyncReport


class ReportRegistry:

    def __init__(
        self,
        stats_service,
    ) -> None:

        self._reports = {
            "Issues Report": lambda: IssuesReport(),
            "Effort Summary Report": lambda: (
                EffortSummaryReport(
                    stats_service=stats_service,
                )
            ),
            "Release Estimate Report": lambda: (
                ReleaseEstimateReport(
                    stats_service=stats_service,
                )
            ),
            "Release Inventory Report": lambda: (ReleaseInventoryReport()),
            "OSG/COPS Report": lambda: (OsgCopsReport()),
            "Resync Report": lambda: (ResyncReport()),
        }

    def get_names(
        self,
    ) -> list[str]:
        return sorted(self._reports.keys())

    def create(
        self,
        name: str,
    ):
        if name not in self._reports:
            raise KeyError(f"Unknown report: {name}")

        return self._reports[name]()
