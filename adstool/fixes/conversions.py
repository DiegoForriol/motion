"""Crear acciones de conversión.

Importante: crear el recurso ConversionAction vía API solo registra la
acción en la cuenta. Para que las conversiones se cuenten de verdad hace
falta instalar el Google Tag (o configurar el desvío de llamadas para
PHONE_CALL_LEAD) en el sitio web — eso es un paso manual aparte que esta
herramienta no automatiza.
"""

from __future__ import annotations

from adstool.fixes.plan import ChangeOperation, ChangePlan

CONVERSION_ACTION_CAVEAT_ES = (
    "Crear esta acción de conversión solo registra el recurso en la cuenta. "
    "Para que cuente conversiones reales, instala el Google Tag en la web "
    "(o configura el desvío de llamadas si es de tipo PHONE_CALL_LEAD)."
)


def build_create_conversion_action_plan(
    client,
    customer_id: str,
    name: str,
    category: str,
    type_: str = "WEBPAGE",
) -> ChangePlan:
    conversion_action_service = client.get_service("ConversionActionService")
    plan = ChangePlan()
    plan.add(
        ChangeOperation(
            kind="create_conversion_action",
            description_es=f"Crear acción de conversión '{name}' ({category}/{type_})",
            before_value="(no existe)",
            after_value=f"{name} [{category}/{type_}] — {CONVERSION_ACTION_CAVEAT_ES}",
            resource_name="(nuevo recurso)",
            apply_fn=_make_apply_fn(
                client, conversion_action_service, customer_id, name, category, type_
            ),
        )
    )
    return plan


def _make_apply_fn(client, conversion_action_service, customer_id, name, category, type_):
    def apply_fn() -> str:
        operation = client.get_type("ConversionActionOperation")
        action = operation.create
        action.name = name
        action.category = getattr(client.enums.ConversionActionCategoryEnum, category)
        action.type_ = getattr(client.enums.ConversionActionTypeEnum, type_)
        action.status = client.enums.ConversionActionStatusEnum.ENABLED
        action.value_settings.always_use_default_value = True
        action.value_settings.default_value = 0.0
        action.value_settings.default_currency_code = "EUR"
        response = conversion_action_service.mutate_conversion_actions(
            customer_id=customer_id, operations=[operation]
        )
        return response.results[0].resource_name

    return apply_fn
