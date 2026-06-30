from adstool.diagnostics.checks import (
    check_ad_approval,
    check_budgets,
    check_campaign_status,
    check_conversions,
    check_customer,
    check_geo_language,
    check_keywords,
    check_negative_keywords,
)
from adstool.diagnostics.models import Severity
from fixtures.sample_rows import (
    ad_approval_row,
    budget_row,
    campaign_row,
    conversion_action_row,
    customer_row,
    keyword_row,
    language_row,
    location_row,
    negative_keyword_row,
)


def test_campaign_paused_is_critical():
    findings = check_campaign_status([campaign_row(status="PAUSED")])
    assert len(findings) == 1
    assert findings[0].severity == Severity.CRITICAL


def test_campaign_enabled_with_no_reasons_is_ok():
    findings = check_campaign_status([campaign_row(status="ENABLED", primary_status_reasons=[])])
    assert len(findings) == 1
    assert findings[0].severity == Severity.OK


def test_campaign_enabled_but_budget_constrained_is_critical():
    findings = check_campaign_status(
        [campaign_row(status="ENABLED", primary_status_reasons=["BUDGET_CONSTRAINED"])]
    )
    assert len(findings) == 1
    assert findings[0].severity == Severity.CRITICAL
    assert "presupuesto" in findings[0].detail_es.lower()


def test_budget_zero_is_critical():
    findings = check_budgets([budget_row(amount_micros=0)])
    assert findings[0].severity == Severity.CRITICAL
    assert findings[0].check_id == "budget_zero"


def test_budget_far_below_recommended_is_warning():
    findings = check_budgets(
        [budget_row(amount_micros=1_000_000, recommended_budget_amount_micros=5_000_000)]
    )
    assert findings[0].severity == Severity.WARNING


def test_budget_reasonable_is_ok():
    findings = check_budgets([budget_row(amount_micros=5_000_000, recommended_budget_amount_micros=0)])
    assert findings[0].severity == Severity.OK


def test_ad_disapproved_is_critical():
    findings = check_ad_approval([ad_approval_row(approval_status="DISAPPROVED")])
    assert findings[0].severity == Severity.CRITICAL


def test_ad_under_review_is_warning():
    findings = check_ad_approval([ad_approval_row(approval_status="UNDER_REVIEW")])
    assert findings[0].severity == Severity.WARNING


def test_ad_approved_is_ok():
    findings = check_ad_approval([ad_approval_row(approval_status="APPROVED")])
    assert findings[0].severity == Severity.OK


def test_ad_group_with_no_active_keywords_is_critical():
    rows = [keyword_row(status="PAUSED", ad_group_id=10)]
    findings = check_keywords(rows)
    critical = [f for f in findings if f.check_id == "ad_group_no_keywords"]
    assert len(critical) == 1
    assert critical[0].severity == Severity.CRITICAL


def test_keyword_bid_below_first_page_cpc_is_warning():
    rows = [
        keyword_row(
            status="ENABLED",
            first_page_cpc_micros=3_000_000,
            effective_cpc_bid_micros=500_000,
        )
    ]
    findings = check_keywords(rows)
    bid_findings = [f for f in findings if f.check_id == "keyword_bid_below_first_page"]
    assert len(bid_findings) == 1
    assert bid_findings[0].severity == Severity.WARNING


def test_negative_keyword_blocks_matching_positive():
    keyword_rows = [keyword_row(text="cerrajero gratis")]
    negative_rows = [negative_keyword_row(text="cerrajero gratis")]
    findings = check_negative_keywords(keyword_rows, negative_rows)
    assert len(findings) == 1
    assert findings[0].severity == Severity.CRITICAL


def test_no_location_or_language_targeting_warns():
    findings = check_geo_language(location_rows=[], language_rows=[])
    assert findings == []  # sin campañas referenciadas, no hay nada que comprobar


def test_campaign_present_but_missing_location_warns():
    findings = check_geo_language(
        location_rows=[], language_rows=[language_row(campaign_id=1)]
    )
    location_findings = [f for f in findings if f.check_id == "campaign_no_location_targeting"]
    assert len(location_findings) == 1
    assert location_findings[0].severity == Severity.WARNING


def test_smart_bidding_without_conversions_is_critical():
    findings = check_conversions(
        conversion_rows=[],
        campaign_rows=[campaign_row(bidding_strategy_type="TARGET_CPA")],
    )
    assert findings[0].severity == Severity.CRITICAL
    assert findings[0].check_id == "no_conversion_actions_with_smart_bidding"


def test_manual_cpc_without_conversions_is_only_warning():
    findings = check_conversions(
        conversion_rows=[],
        campaign_rows=[campaign_row(bidding_strategy_type="MANUAL_CPC")],
    )
    assert findings[0].severity == Severity.WARNING


def test_active_conversion_action_is_ok():
    findings = check_conversions(
        conversion_rows=[conversion_action_row(status="ENABLED")],
        campaign_rows=[campaign_row(bidding_strategy_type="MANUAL_CPC")],
    )
    assert findings[0].severity == Severity.OK


def test_customer_disabled_is_critical():
    findings = check_customer([customer_row(status="SUSPENDED")])
    assert findings[0].severity == Severity.CRITICAL
