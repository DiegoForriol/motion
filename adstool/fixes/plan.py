"""Plan de cambios: agrupa operaciones, las muestra en dry-run y las aplica
solo tras confirmación explícita."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


class GuardrailExceeded(Exception):
    """Se lanza cuando una operación supera los límites de seguridad (p. ej.
    una subida de presupuesto desproporcionada) y no se pasó --force."""


@dataclass
class ChangeOperation:
    kind: str
    description_es: str
    before_value: str
    after_value: str
    resource_name: str
    # Función sin argumentos que ejecuta la mutación real y devuelve un
    # mensaje de confirmación. No debe llamarse nunca fuera de
    # ChangePlan.apply() tras confirmación explícita.
    apply_fn: Callable[[], str]


@dataclass
class ChangePlan:
    operations: list[ChangeOperation] = field(default_factory=list)

    def add(self, operation: ChangeOperation) -> None:
        self.operations.append(operation)

    def is_empty(self) -> bool:
        return not self.operations

    def render_dry_run(self) -> str:
        if self.is_empty():
            return "No hay cambios propuestos."
        lines = ["Plan de cambios (dry-run, no se ha aplicado nada todavía):", ""]
        for i, op in enumerate(self.operations, start=1):
            lines.append(f"{i}. [{op.kind}] {op.description_es}")
            lines.append(f"   Antes: {op.before_value}")
            lines.append(f"   Después: {op.after_value}")
            lines.append(f"   Recurso: {op.resource_name}")
            lines.append("")
        return "\n".join(lines)

    def apply(self, *, assume_yes: bool = False, confirm_fn: Callable[[str], bool] | None = None) -> list[str]:
        """Aplica todas las operaciones del plan tras confirmación explícita.

        `confirm_fn` permite inyectar la confirmación en tests; por defecto
        usa un prompt interactivo y[N].
        """
        if self.is_empty():
            return []

        print(self.render_dry_run())

        if not assume_yes:
            ask = confirm_fn or (lambda prompt: input(prompt).strip().lower() == "y")
            if not ask("¿Aplicar estos cambios a la cuenta real de Google Ads? [y/N]: "):
                print("Operación cancelada. No se ha aplicado ningún cambio.")
                return []

        results: list[str] = []
        for op in self.operations:
            try:
                outcome = op.apply_fn()
                results.append(f"OK: {op.description_es} -> {outcome}")
            except Exception as exc:  # noqa: BLE001 - se reporta tal cual al usuario
                results.append(f"ERROR: {op.description_es} -> {exc}")
        return results
