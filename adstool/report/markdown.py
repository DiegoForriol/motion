"""Generación del informe de diagnóstico en Markdown, guardado en reports/."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from adstool.diagnostics.models import DiagnosticReport

DEFAULT_OUTPUT_DIR = Path("reports")


def write_report(
    report: DiagnosticReport, output_dir: Path | str = DEFAULT_OUTPUT_DIR
) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = output_dir / f"diagnose-{report.customer_id}-{timestamp}.md"
    path.write_text(render_markdown(report), encoding="utf-8")
    return path


def render_markdown(report: DiagnosticReport) -> str:
    lines = [
        f"# Diagnóstico de Google Ads — {report.customer_id}",
        "",
        f"- Fecha: {datetime.now().isoformat(timespec='seconds')}",
        f"- Alcance: {report.campaign_scope}",
        "",
        "## Resumen",
        "",
        f"- 🔴 Críticos: {len(report.critical_findings)}",
        f"- 🟡 Advertencias: {len(report.warning_findings)}",
        f"- 🟢 Sin problemas: {len(report.ok_findings)}",
        "",
    ]

    root_cause = report.likely_root_cause
    if root_cause:
        lines += [
            "## Causa más probable de las cero impresiones",
            "",
            f"**{root_cause.title_es}**",
            "",
            root_cause.detail_es,
            "",
        ]

    lines.append("## Hallazgos")
    lines.append("")
    for finding in report.sorted_findings():
        lines.append(f"### {finding.severity.icon} {finding.title_es}")
        lines.append("")
        lines.append(finding.detail_es)
        if finding.suggested_action:
            lines.append("")
            lines.append(f"Acción sugerida: `{finding.suggested_action}`")
        if finding.resource_name:
            lines.append("")
            lines.append(f"Recurso: `{finding.resource_name}`")
        lines.append("")

    return "\n".join(lines)


def append_applied_changes(path: Path, change_results: list[str]) -> None:
    """Añade una sección 'Cambios aplicados' al informe markdown existente,
    sirviendo de auditoría ya que no hay rollback automático."""
    if not change_results:
        return
    with path.open("a", encoding="utf-8") as f:
        f.write("\n## Cambios aplicados\n\n")
        for result in change_results:
            f.write(f"- {result}\n")
