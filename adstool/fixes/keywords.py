"""Añadir palabras clave nuevas a un grupo de anuncios."""

from __future__ import annotations

from adstool.fixes.plan import ChangeOperation, ChangePlan

# Lista semilla para el sector de cerrajería, editable por el usuario vía
# --keywords-file. Match type por defecto: PHRASE.
SEED_KEYWORDS_CERRAJERIA = [
    ("cerrajero cuenca", "PHRASE"),
    ("cerrajero urgente cuenca", "PHRASE"),
    ("apertura puertas cuenca", "PHRASE"),
    ("cambio cerradura cuenca", "PHRASE"),
    ("cerrajero 24 horas cuenca", "PHRASE"),
]


def build_add_keywords_plan(
    client,
    customer_id: str,
    ad_group_id: str,
    keywords: list[tuple[str, str]],
) -> ChangePlan:
    """Construye un ChangePlan para añadir `keywords` (texto, match_type) a un
    grupo de anuncios. No realiza ninguna llamada mutate hasta que se
    invoque plan.apply()."""
    ad_group_service = client.get_service("AdGroupService")
    ad_group_resource_name = ad_group_service.ad_group_path(customer_id, ad_group_id)
    criterion_service = client.get_service("AdGroupCriterionService")

    plan = ChangePlan()
    for text, match_type in keywords:
        plan.add(
            ChangeOperation(
                kind="add_keyword",
                description_es=f"Añadir palabra clave '{text}' ({match_type})",
                before_value="(no existe)",
                after_value=f"{text} [{match_type}]",
                resource_name=ad_group_resource_name,
                apply_fn=_make_apply_fn(
                    client, criterion_service, customer_id, ad_group_resource_name, text, match_type
                ),
            )
        )
    return plan


def _make_apply_fn(client, criterion_service, customer_id, ad_group_resource_name, text, match_type):
    def apply_fn() -> str:
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.create
        criterion.ad_group = ad_group_resource_name
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        criterion.keyword.text = text
        criterion.keyword.match_type = getattr(
            client.enums.KeywordMatchTypeEnum, match_type
        )
        response = criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id, operations=[operation]
        )
        return response.results[0].resource_name

    return apply_fn
