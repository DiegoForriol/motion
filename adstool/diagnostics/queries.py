"""Consultas GAQL usadas por los chequeos de diagnóstico."""

CAMPAIGN_STATUS = """
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  campaign.primary_status,
  campaign.primary_status_reasons,
  campaign.serving_status,
  campaign.advertising_channel_type,
  campaign.bidding_strategy_type,
  campaign.campaign_budget
FROM campaign
WHERE campaign.status != 'REMOVED'
"""

CAMPAIGN_BUDGET = """
SELECT
  campaign_budget.id,
  campaign_budget.name,
  campaign_budget.amount_micros,
  campaign_budget.status,
  campaign_budget.delivery_method,
  campaign_budget.recommended_budget_amount_micros,
  campaign.id,
  campaign.name
FROM campaign_budget
WHERE campaign.status != 'REMOVED'
"""

AD_GROUP_STATUS = """
SELECT
  ad_group.id,
  ad_group.name,
  ad_group.status,
  campaign.id,
  campaign.name
FROM ad_group
WHERE campaign.status != 'REMOVED' AND ad_group.status != 'REMOVED'
"""

AD_APPROVAL_STATUS = """
SELECT
  ad_group_ad.ad.id,
  ad_group_ad.ad.type,
  ad_group_ad.status,
  ad_group_ad.policy_summary.approval_status,
  ad_group_ad.policy_summary.review_status,
  ad_group.id,
  ad_group.name,
  campaign.id,
  campaign.name
FROM ad_group_ad
WHERE ad_group_ad.status != 'REMOVED'
"""

KEYWORD_VIEW = """
SELECT
  ad_group_criterion.criterion_id,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.status,
  ad_group_criterion.system_serving_status,
  ad_group_criterion.approval_status,
  ad_group_criterion.quality_info.quality_score,
  ad_group_criterion.position_estimates.first_page_cpc_micros,
  ad_group_criterion.effective_cpc_bid_micros,
  ad_group.id,
  ad_group.name,
  campaign.id,
  campaign.name
FROM keyword_view
WHERE ad_group_criterion.status != 'REMOVED'
"""

CAMPAIGN_NEGATIVE_KEYWORDS = """
SELECT
  campaign_criterion.criterion_id,
  campaign_criterion.keyword.text,
  campaign_criterion.keyword.match_type,
  campaign_criterion.negative,
  campaign.id,
  campaign.name
FROM campaign_criterion
WHERE campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = true
"""

CAMPAIGN_LOCATION_TARGETING = """
SELECT
  campaign_criterion.location.geo_target_constant,
  campaign_criterion.negative,
  campaign.id,
  campaign.name
FROM campaign_criterion
WHERE campaign_criterion.type = 'LOCATION'
"""

CAMPAIGN_LANGUAGE_TARGETING = """
SELECT
  campaign_criterion.language.language_constant,
  campaign.id,
  campaign.name
FROM campaign_criterion
WHERE campaign_criterion.type = 'LANGUAGE'
"""

CONVERSION_ACTIONS = """
SELECT
  conversion_action.id,
  conversion_action.name,
  conversion_action.status,
  conversion_action.type,
  conversion_action.category,
  conversion_action.primary_for_goal
FROM conversion_action
"""

CUSTOMER_INFO = """
SELECT
  customer.id,
  customer.descriptive_name,
  customer.currency_code,
  customer.time_zone,
  customer.status
FROM customer
"""
