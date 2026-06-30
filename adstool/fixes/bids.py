"""Subir la puja de una palabra clave (CPC manual) o el objetivo de una
estrategia de Smart Bidding (Target CPA / Target ROAS)."""

from __future__ import annotations

from adstool.fixes.plan import ChangeOperation, ChangePlan


def build_update_keyword_bid_plan(
    client,
    customer_id: str,
    criterion_resource_name: str,
    current_bid_micros: int,
    new_bid_micros: int,
) -> ChangePlan:
    criterion_service = client.get_service("AdGroupCriterionService")
    plan = ChangePlan()
    plan.add(
        ChangeOperation(
            kind="update_keyword_bid",
            description_es="Actualizar puja CPC manual de la palabra clave",
            before_value=f"{current_bid_micros / 1_000_000:.2f}",
            after_value=f"{new_bid_micros / 1_000_000:.2f}",
            resource_name=criterion_resource_name,
            apply_fn=_make_keyword_bid_apply_fn(
                client, criterion_service, customer_id, criterion_resource_name, new_bid_micros
            ),
        )
    )
    return plan


def _make_keyword_bid_apply_fn(client, criterion_service, customer_id, resource_name, new_bid_micros):
    def apply_fn() -> str:
        operation = client.get_type("AdGroupCriterionOperation")
        operation.update.resource_name = resource_name
        operation.update.cpc_bid_micros = new_bid_micros
        client.copy_from(
            operation.update_mask,
            client.get_type("FieldMask")(paths=["cpc_bid_micros"]),
        )
        response = criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id, operations=[operation]
        )
        return response.results[0].resource_name

    return apply_fn


def build_update_target_cpa_plan(
    client,
    customer_id: str,
    campaign_resource_name: str,
    current_target_cpa_micros: int,
    new_target_cpa_micros: int,
) -> ChangePlan:
    campaign_service = client.get_service("CampaignService")
    plan = ChangePlan()
    plan.add(
        ChangeOperation(
            kind="update_target_cpa",
            description_es="Actualizar Target CPA de la estrategia de pujas automáticas",
            before_value=f"{current_target_cpa_micros / 1_000_000:.2f}",
            after_value=f"{new_target_cpa_micros / 1_000_000:.2f}",
            resource_name=campaign_resource_name,
            apply_fn=_make_target_cpa_apply_fn(
                client, campaign_service, customer_id, campaign_resource_name, new_target_cpa_micros
            ),
        )
    )
    return plan


def _make_target_cpa_apply_fn(client, campaign_service, customer_id, resource_name, new_target_cpa_micros):
    def apply_fn() -> str:
        operation = client.get_type("CampaignOperation")
        operation.update.resource_name = resource_name
        operation.update.target_cpa.target_cpa_micros = new_target_cpa_micros
        client.copy_from(
            operation.update_mask,
            client.get_type("FieldMask")(paths=["target_cpa.target_cpa_micros"]),
        )
        response = campaign_service.mutate_campaigns(
            customer_id=customer_id, operations=[operation]
        )
        return response.results[0].resource_name

    return apply_fn
