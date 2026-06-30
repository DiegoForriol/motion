"""Renderizado del informe de diagnóstico en consola usando rich."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from adstool.diagnostics.models import DiagnosticReport, Severity

SEVERITY_STYLE = {
    Severity.CRITICAL: "bold red",
    Severity.WARNING: "bold yellow",
    Severity.OK: "bold green",
}


def render_report(report: DiagnosticReport, console: Console | None = None) -> None:
    console = console or Console()

    console.print(
        Panel(
            f"Cuenta: {report.customer_id}\nAlcance: {report.campaign_scope}",
            title="Diagnóstico de Google Ads — lockercuenca.es",
        )
    )

    table = Table(show_lines=True)
    table.add_column("Severidad", width=10)
    table.add_column("Hallazgo")
    table.add_column("Detalle")
    table.add_column("Acción sugerida")

    for finding in report.sorted_findings():
        style = SEVERITY_STYLE[finding.severity]
        table.add_row(
            f"[{style}]{finding.severity.icon} {finding.severity.value}[/{style}]",
            finding.title_es,
            finding.detail_es,
            finding.suggested_action or "-",
        )

    console.print(table)

    console.print(
        f"\nResumen: {len(report.critical_findings)} crítico(s), "
        f"{len(report.warning_findings)} advertencia(s), "
        f"{len(report.ok_findings)} sin problemas."
    )

    root_cause = report.likely_root_cause
    if root_cause:
        console.print(
            Panel(
                f"{root_cause.title_es}\n{root_cause.detail_es}",
                title="Causa más probable de las cero impresiones",
                border_style="red",
            )
        )
    else:
        console.print(
            "\nNo se ha detectado ninguna causa crítica obvia de la falta de "
            "impresiones; revisa las advertencias anteriores."
        )
