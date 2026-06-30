"""Subir el presupuesto diario de una campaña."""

from __future__ import annotations

from adstool.fixes.plan import ChangeOperation, ChangePlan, GuardrailExceeded

DEFAULT_MAX_MULTIPLIER = 5.0


def build_update_budget_plan(
    client,
    customer_id: str,
    budget_resource_name: str,
    current_amount_micros: int,
    new_amount_micros: int,
    *,
    force: bool = False,
    max_multiplier: float = DEFAULT_MAX_MULTIPLIER,
) -> ChangePlan:
    """Construye un ChangePlan para actualizar el presupuesto diario.

    Lanza GuardrailExceeded si la subida supera `max_multiplier` veces el
    presupuesto actual y no se pasó force=True, para evitar un gasto
    descontrolado por un valor mal introducido.
    """
    if current_amount_micros > 0 and not force:
        ratio = new_amount_micros / current_amount_micros
        if ratio > max_multiplier:
            raise GuardrailExceeded(
                f"La subida propuesta ({ratio:.1f}x el presupuesto actual) supera el "
                f"límite de seguridad ({max_multiplier}x). Usa --force si realmente "
                "quieres aplicar este cambio."
            )

    budget_service = client.get_service("CampaignBudgetService")

    plan = ChangePlan()
    plan.add(
        ChangeOperation(
            kind="update_budget",
            description_es="Actualizar presupuesto diario de la campaña",
            before_value=f"{current_amount_micros / 1_000_000:.2f}",
            after_value=f"{new_amount_micros / 1_000_000:.2f}",
            resource_name=budget_resource_name,
            apply_fn=_make_apply_fn(
                client, budget_service, customer_id, budget_resource_name, new_amount_micros
            ),
        )
    )
    return plan


def _make_apply_fn(client, budget_service, customer_id, budget_resource_name, new_amount_micros):
    def apply_fn() -> str:
        operation = client.get_type("CampaignBudgetOperation")
        operation.update.resource_name = budget_resource_name
        operation.update.amount_micros = new_amount_micros
        client.copy_from(
            operation.update_mask,
            client.get_type("FieldMask")(paths=["amount_micros"]),
        )
        response = budget_service.mutate_campaign_budgets(
            customer_id=customer_id, operations=[operation]
        )
        return response.results[0].resource_name

    return apply_fn
