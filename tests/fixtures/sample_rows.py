"""Filas GAQL simuladas para probar adstool.diagnostics.checks sin llamar a
la API real."""

from __future__ import annotations

from types import SimpleNamespace


class FakeEnum:
    """Imita un enum de proto-plus: expone `.name`."""

    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:  # pragma: no cover - solo ayuda a depurar
        return f"FakeEnum({self.name!r})"


def campaign_row(
    *,
    id: int = 1,
    name: str = "Cerrajería Cuenca",
    status: str = "ENABLED",
    primary_status_reasons: list[str] | None = None,
    bidding_strategy_type: str = "MANUAL_CPC",
):
    return SimpleNamespace(
        campaign=SimpleNamespace(
            id=id,
            name=name,
            status=FakeEnum(status),
            primary_status_reasons=[FakeEnum(r) for r in (primary_status_reasons or [])],
            bidding_strategy_type=FakeEnum(bidding_strategy_type),
        )
    )


def budget_row(
    *,
    campaign_id: int = 1,
    campaign_name: str = "Cerrajería Cuenca",
    amount_micros: int = 1_000_000,
    recommended_budget_amount_micros: int = 0,
    resource_name: str = "customers/123/campaignBudgets/1",
):
    return SimpleNamespace(
        campaign=SimpleNamespace(id=campaign_id, name=campaign_name),
        campaign_budget=SimpleNamespace(
            amount_micros=amount_micros,
            recommended_budget_amount_micros=recommended_budget_amount_micros,
            resource_name=resource_name,
        ),
    )


def ad_approval_row(
    *,
    ad_id: int = 1,
    campaign_id: int = 1,
    campaign_name: str = "Cerrajería Cuenca",
    approval_status: str = "APPROVED",
):
    return SimpleNamespace(
        campaign=SimpleNamespace(id=campaign_id, name=campaign_name),
        ad_group_ad=SimpleNamespace(
            ad=SimpleNamespace(id=ad_id),
            policy_summary=SimpleNamespace(approval_status=FakeEnum(approval_status)),
        ),
    )


def keyword_row(
    *,
    criterion_id: int = 1,
    text: str = "cerrajero cuenca",
    status: str = "ENABLED",
    system_serving_status: str = "ELIGIBLE",
    first_page_cpc_micros: int = 0,
    effective_cpc_bid_micros: int = 0,
    ad_group_id: int = 10,
    ad_group_name: str = "Cerrajería - Urgencias",
    campaign_id: int = 1,
    campaign_name: str = "Cerrajería Cuenca",
):
    return SimpleNamespace(
        campaign=SimpleNamespace(id=campaign_id, name=campaign_name),
        ad_group=SimpleNamespace(id=ad_group_id, name=ad_group_name),
        ad_group_criterion=SimpleNamespace(
            criterion_id=criterion_id,
            keyword=SimpleNamespace(text=text),
            status=FakeEnum(status),
            system_serving_status=FakeEnum(system_serving_status),
            position_estimates=SimpleNamespace(first_page_cpc_micros=first_page_cpc_micros),
            effective_cpc_bid_micros=effective_cpc_bid_micros,
        ),
    )


def negative_keyword_row(
    *, text: str = "cerrajero gratis", campaign_id: int = 1, campaign_name: str = "Cerrajería Cuenca"
):
    return SimpleNamespace(
        campaign=SimpleNamespace(id=campaign_id, name=campaign_name),
        campaign_criterion=SimpleNamespace(keyword=SimpleNamespace(text=text)),
    )


def location_row(*, campaign_id: int = 1, campaign_name: str = "Cerrajería Cuenca"):
    return SimpleNamespace(campaign=SimpleNamespace(id=campaign_id, name=campaign_name))


def language_row(*, campaign_id: int = 1, campaign_name: str = "Cerrajería Cuenca"):
    return SimpleNamespace(campaign=SimpleNamespace(id=campaign_id, name=campaign_name))


def conversion_action_row(*, status: str = "ENABLED"):
    return SimpleNamespace(conversion_action=SimpleNamespace(status=FakeEnum(status)))


def customer_row(*, id: int = 123, descriptive_name: str = "lockercuenca.es", status: str = "ENABLED"):
    return SimpleNamespace(
        customer=SimpleNamespace(
            id=id,
            descriptive_name=descriptive_name,
            currency_code="EUR",
            time_zone="Europe/Madrid",
            status=FakeEnum(status),
        )
    )
