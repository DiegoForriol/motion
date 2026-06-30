import pytest

from adstool.fixes.budgets import build_update_budget_plan
from adstool.fixes.conversions import build_create_conversion_action_plan
from adstool.fixes.keywords import build_add_keywords_plan
from adstool.fixes.plan import GuardrailExceeded
from fixtures.fake_client import FakeClient


def test_add_keywords_plan_does_not_mutate_until_apply():
    client = FakeClient()
    plan = build_add_keywords_plan(
        client, "123", "10", [("cerrajero cuenca", "PHRASE")]
    )

    assert not client.all_calls
    assert "cerrajero cuenca" in plan.render_dry_run()


def test_plan_apply_without_confirmation_does_not_mutate():
    client = FakeClient()
    plan = build_add_keywords_plan(
        client, "123", "10", [("cerrajero cuenca", "PHRASE")]
    )

    results = plan.apply(assume_yes=False, confirm_fn=lambda prompt: False)

    assert results == []
    assert not client.all_calls


def test_plan_apply_with_confirmation_mutates():
    client = FakeClient()
    plan = build_add_keywords_plan(
        client, "123", "10", [("cerrajero cuenca", "PHRASE")]
    )

    results = plan.apply(assume_yes=True)

    assert len(client.all_calls) == 1
    assert client.all_calls[0][0] == "mutate_ad_group_criteria"
    assert results[0].startswith("OK:")


def test_budget_guardrail_blocks_excessive_increase():
    client = FakeClient()
    with pytest.raises(GuardrailExceeded):
        build_update_budget_plan(
            client,
            "123",
            "customers/123/campaignBudgets/1",
            current_amount_micros=1_000_000,
            new_amount_micros=10_000_000,  # 10x
        )


def test_budget_guardrail_allows_with_force():
    client = FakeClient()
    plan = build_update_budget_plan(
        client,
        "123",
        "customers/123/campaignBudgets/1",
        current_amount_micros=1_000_000,
        new_amount_micros=10_000_000,
        force=True,
    )
    assert not plan.is_empty()


def test_create_conversion_action_plan_includes_tracking_caveat():
    client = FakeClient()
    plan = build_create_conversion_action_plan(
        client, "123", "Contacto web", "CONTACT", "WEBPAGE"
    )
    rendered = plan.render_dry_run()
    assert "Google Tag" in rendered
