"""Modelos de datos para el informe de diagnóstico."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Severity(Enum):
    OK = "OK"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

    @property
    def icon(self) -> str:
        return {"OK": "🟢", "WARNING": "🟡", "CRITICAL": "🔴"}[self.value]

    @property
    def sort_key(self) -> int:
        return {"CRITICAL": 0, "WARNING": 1, "OK": 2}[self.value]


@dataclass
class Finding:
    check_id: str
    severity: Severity
    title_es: str
    detail_es: str
    suggested_action: str | None = None
    resource_name: str | None = None


@dataclass
class DiagnosticReport:
    customer_id: str
    account_name: str | None = None
    campaign_scope: str = "todas las campañas activas"
    findings: list[Finding] = field(default_factory=list)

    def add(self, finding: Finding) -> None:
        self.findings.append(finding)

    @property
    def critical_findings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == Severity.CRITICAL]

    @property
    def warning_findings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == Severity.WARNING]

    @property
    def ok_findings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == Severity.OK]

    def sorted_findings(self) -> list[Finding]:
        return sorted(self.findings, key=lambda f: f.severity.sort_key)

    @property
    def likely_root_cause(self) -> Finding | None:
        """El primer hallazgo crítico es la causa más probable de cero impresiones."""
        criticals = self.critical_findings
        return criticals[0] if criticals else None
