"""Chequeos de diagnóstico: convierten filas GAQL en Finding.

Cada función `check_*` es pura (recibe filas ya obtenidas y no llama a la
API), lo que permite probarla con filas simuladas en los tests. El
orquestador `run_diagnostics` es el único punto que combina estas funciones
con llamadas reales a través de `diagnostics.runner`.
"""

from __future__ import annotations

from adstool.diagnostics import queries
from adstool.diagnostics.models import DiagnosticReport, Finding, Severity
from adstool.diagnostics.runner import run_query

# Traducción de los motivos más comunes de campaign.primary_status_reasons
# a una explicación breve en español.
PRIMARY_STATUS_REASON_ES = {
    "CAMPAIGN_PAUSED": "La campaña está pausada manualmente.",
    "CAMPAIGN_REMOVED": "La campaña ha sido eliminada.",
    "CAMPAIGN_ENDED": "La fecha de fin de la campaña ya ha pasado.",
    "CAMPAIGN_PENDING": "La campaña tiene una fecha de inicio futura.",
    "AD_GROUP_PAUSED": "Todos los grupos de anuncios están pausados.",
    "AD_GROUP_AD_PAUSED": "Todos los anuncios están pausados.",
    "AD_GROUP_AD_DISAPPROVED": "Los anuncios han sido rechazados por políticas.",
    "AD_GROUP_AD_UNDER_REVIEW": "Los anuncios están pendientes de revisión.",
    "KEYWORDS_PAUSED": "Todas las palabras clave están pausadas.",
    "NO_KEYWORDS": "El grupo de anuncios no tiene palabras clave activas.",
    "KEYWORD_LOW_QUALITY_SCORE": "Las palabras clave tienen un nivel de calidad bajo.",
    "KEYWORDS_LOW_SEARCH_VOLUME": "Las palabras clave tienen muy poco volumen de búsqueda.",
    "BUDGET_CONSTRAINED": "El presupuesto diario está limitando la entrega de anuncios.",
    "BUDGET_LIMITED": "El presupuesto diario está limitando la entrega de anuncios.",
    "PENDING_REVIEW": "La campaña está pendiente de revisión de políticas.",
    "DISAPPROVED": "La campaña ha sido rechazada por políticas.",
    "LOW_QUALITY": "La calidad general de la campaña es baja.",
    "MISCONFIGURED_TRACKING": "El seguimiento de conversiones está mal configurado.",
}

SMART_BIDDING_STRATEGIES = {
    "TARGET_CPA",
    "TARGET_ROAS",
    "MAXIMIZE_CONVERSIONS",
    "MAXIMIZE_CONVERSION_VALUE",
}


def _enum_name(value) -> str:
    """Devuelve el nombre legible de un enum proto-plus o de un str/objeto simulado."""
    name = getattr(value, "name", None)
    return name if name is not None else str(value)


def check_campaign_status(rows: list) -> list[Finding]:
    findings: list[Finding] = []
    for row in rows:
        campaign = row.campaign
        status = _enum_name(campaign.status)
        reasons = [_enum_name(r) for r in campaign.primary_status_reasons]

        if status != "ENABLED":
            findings.append(
                Finding(
                    check_id="campaign_status",
                    severity=Severity.CRITICAL,
                    title_es=f"Campaña '{campaign.name}' no está activa",
                    detail_es=f"Estado actual: {status}.",
                    suggested_action="Activa la campaña desde la UI de Google Ads si quieres que sirva anuncios.",
                    resource_name=f"campaigns/{campaign.id}",
                )
            )
            continue

        if reasons:
            for reason in reasons:
                explanation = PRIMARY_STATUS_REASON_ES.get(
                    reason, f"Motivo reportado por Google Ads: {reason}."
                )
                findings.append(
                    Finding(
                        check_id="campaign_primary_status_reason",
                        severity=Severity.CRITICAL,
                        title_es=f"Campaña '{campaign.name}' no sirve anuncios ({reason})",
                        detail_es=explanation,
                        resource_name=f"campaigns/{campaign.id}",
                    )
                )
        else:
            findings.append(
                Finding(
                    check_id="campaign_status",
                    severity=Severity.OK,
                    title_es=f"Campaña '{campaign.name}' activa y sin problemas reportados",
                    detail_es="El estado principal de la campaña no indica ningún bloqueo.",
                    resource_name=f"campaigns/{campaign.id}",
                )
            )
    return findings


def check_budgets(rows: list) -> list[Finding]:
    findings: list[Finding] = []
    for row in rows:
        budget = row.campaign_budget
        campaign = row.campaign
        amount = budget.amount_micros / 1_000_000
        recommended = getattr(budget, "recommended_budget_amount_micros", 0) or 0

        if amount <= 0:
            findings.append(
                Finding(
                    check_id="budget_zero",
                    severity=Severity.CRITICAL,
                    title_es=f"Presupuesto de '{campaign.name}' es 0 o no está definido",
                    detail_es="Sin presupuesto diario la campaña no puede pujar en subastas.",
                    suggested_action=f"adstool update-budget --campaign-id {campaign.id} --daily-budget <importe> --apply",
                    resource_name=budget.resource_name,
                )
            )
        elif recommended and recommended / 1_000_000 > amount * 1.5:
            findings.append(
                Finding(
                    check_id="budget_low",
                    severity=Severity.WARNING,
                    title_es=f"Presupuesto de '{campaign.name}' parece bajo",
                    detail_es=(
                        f"Presupuesto actual: {amount:.2f}. Google sugiere "
                        f"aproximadamente {recommended / 1_000_000:.2f} para una entrega estable."
                    ),
                    suggested_action=f"adstool update-budget --campaign-id {campaign.id} --daily-budget <importe> --apply",
                    resource_name=budget.resource_name,
                )
            )
        else:
            findings.append(
                Finding(
                    check_id="budget_ok",
                    severity=Severity.OK,
                    title_es=f"Presupuesto de '{campaign.name}' parece razonable",
                    detail_es=f"Presupuesto actual: {amount:.2f}.",
                    resource_name=budget.resource_name,
                )
            )
    return findings


def check_ad_approval(rows: list) -> list[Finding]:
    findings: list[Finding] = []
    for row in rows:
        ad = row.ad_group_ad
        campaign = row.campaign
        approval = _enum_name(ad.policy_summary.approval_status)

        if approval == "DISAPPROVED":
            findings.append(
                Finding(
                    check_id="ad_disapproved",
                    severity=Severity.CRITICAL,
                    title_es=f"Anuncio rechazado en campaña '{campaign.name}'",
                    detail_es="El anuncio ha sido rechazado por políticas de Google Ads y no se mostrará.",
                    suggested_action="Revisa el resumen de políticas en la UI de Google Ads y corrige o apela el anuncio.",
                    resource_name=f"ads/{ad.ad.id}",
                )
            )
        elif approval in ("AREA_OF_INTEREST_ONLY", "UNDER_REVIEW", "REVIEW_IN_PROGRESS"):
            findings.append(
                Finding(
                    check_id="ad_under_review",
                    severity=Severity.WARNING,
                    title_es=f"Anuncio pendiente de revisión en campaña '{campaign.name}'",
                    detail_es="Mientras esté en revisión, el anuncio puede mostrarse con alcance limitado o no mostrarse.",
                    resource_name=f"ads/{ad.ad.id}",
                )
            )
        elif approval == "APPROVED":
            findings.append(
                Finding(
                    check_id="ad_approved",
                    severity=Severity.OK,
                    title_es=f"Anuncio aprobado en campaña '{campaign.name}'",
                    detail_es="Sin problemas de políticas detectados.",
                    resource_name=f"ads/{ad.ad.id}",
                )
            )
    return findings


def check_keywords(rows: list) -> list[Finding]:
    findings: list[Finding] = []
    active_count_by_ad_group: dict[int, int] = {}

    for row in rows:
        criterion = row.ad_group_criterion
        ad_group = row.ad_group
        campaign = row.campaign
        status = _enum_name(criterion.status)
        serving_status = _enum_name(criterion.system_serving_status)

        if status == "ENABLED":
            active_count_by_ad_group[ad_group.id] = (
                active_count_by_ad_group.get(ad_group.id, 0) + 1
            )

        if status != "ENABLED":
            continue

        if serving_status not in ("ELIGIBLE", "UNKNOWN", "UNSPECIFIED"):
            findings.append(
                Finding(
                    check_id="keyword_not_serving",
                    severity=Severity.WARNING,
                    title_es=f"Palabra clave '{criterion.keyword.text}' no entrega ({serving_status})",
                    detail_es=f"Grupo de anuncios '{ad_group.name}', campaña '{campaign.name}'.",
                    resource_name=f"criteria/{criterion.criterion_id}",
                )
            )

        first_page_cpc = getattr(
            criterion.position_estimates, "first_page_cpc_micros", 0
        )
        current_bid = getattr(criterion, "effective_cpc_bid_micros", 0)
        if first_page_cpc and current_bid and current_bid < first_page_cpc:
            findings.append(
                Finding(
                    check_id="keyword_bid_below_first_page",
                    severity=Severity.WARNING,
                    title_es=f"Puja insuficiente para '{criterion.keyword.text}'",
                    detail_es=(
                        f"Puja actual: {current_bid / 1_000_000:.2f}, "
                        f"CPC estimado de primera página: {first_page_cpc / 1_000_000:.2f}."
                    ),
                    suggested_action=(
                        f"adstool update-bid --criterion-id {criterion.criterion_id} "
                        f"--cpc-bid {first_page_cpc / 1_000_000:.2f} --apply"
                    ),
                    resource_name=f"criteria/{criterion.criterion_id}",
                )
            )

    seen_ad_groups: set[int] = set()
    for row in rows:
        ad_group = row.ad_group
        campaign = row.campaign
        if ad_group.id in seen_ad_groups:
            continue
        seen_ad_groups.add(ad_group.id)

        if active_count_by_ad_group.get(ad_group.id, 0) == 0:
            findings.append(
                Finding(
                    check_id="ad_group_no_keywords",
                    severity=Severity.CRITICAL,
                    title_es=f"Grupo de anuncios '{ad_group.name}' sin palabras clave activas",
                    detail_es=f"Campaña '{campaign.name}' no puede competir en subastas sin palabras clave.",
                    suggested_action=f"adstool add-keywords --ad-group-id {ad_group.id} --keywords-file <archivo.csv> --apply",
                    resource_name=f"adGroups/{ad_group.id}",
                )
            )

    return findings


def check_negative_keywords(keyword_rows: list, negative_rows: list) -> list[Finding]:
    findings: list[Finding] = []
    negatives_by_campaign: dict[int, list[str]] = {}
    for row in negative_rows:
        negatives_by_campaign.setdefault(row.campaign.id, []).append(
            row.campaign_criterion.keyword.text.lower()
        )

    for row in keyword_rows:
        criterion = row.ad_group_criterion
        campaign = row.campaign
        text = criterion.keyword.text.lower()
        negatives = negatives_by_campaign.get(campaign.id, [])
        if text in negatives:
            findings.append(
                Finding(
                    check_id="keyword_blocked_by_negative",
                    severity=Severity.CRITICAL,
                    title_es=f"Palabra clave '{criterion.keyword.text}' bloqueada por un negativo exacto",
                    detail_es=f"Campaña '{campaign.name}' tiene un negativo idéntico que impide que esta keyword sirva.",
                    suggested_action="Elimina o ajusta la palabra clave negativa en conflicto desde la UI de Google Ads.",
                    resource_name=f"criteria/{criterion.criterion_id}",
                )
            )
    return findings


def check_geo_language(location_rows: list, language_rows: list) -> list[Finding]:
    findings: list[Finding] = []
    campaigns_with_location = {row.campaign.id: row.campaign.name for row in location_rows}
    campaigns_with_language = {row.campaign.id: row.campaign.name for row in language_rows}

    all_campaign_ids = set(campaigns_with_location) | set(campaigns_with_language)
    for campaign_id in all_campaign_ids:
        name = campaigns_with_location.get(campaign_id) or campaigns_with_language.get(campaign_id)
        if campaign_id not in campaigns_with_location:
            findings.append(
                Finding(
                    check_id="campaign_no_location_targeting",
                    severity=Severity.WARNING,
                    title_es=f"Campaña '{name}' sin segmentación geográfica explícita",
                    detail_es="Sin ubicación definida, Google Ads puede mostrar anuncios fuera de tu zona de servicio (p. ej. fuera de Cuenca).",
                    resource_name=f"campaigns/{campaign_id}",
                )
            )
        if campaign_id not in campaigns_with_language:
            findings.append(
                Finding(
                    check_id="campaign_no_language_targeting",
                    severity=Severity.WARNING,
                    title_es=f"Campaña '{name}' sin idioma de segmentación explícito",
                    detail_es="Sin idioma definido, los anuncios pueden no mostrarse a usuarios que buscan en español.",
                    resource_name=f"campaigns/{campaign_id}",
                )
            )
    return findings


def check_conversions(conversion_rows: list, campaign_rows: list) -> list[Finding]:
    findings: list[Finding] = []
    active_conversions = [
        row
        for row in conversion_rows
        if _enum_name(row.conversion_action.status) == "ENABLED"
    ]

    smart_bidding_campaigns = [
        row.campaign.name
        for row in campaign_rows
        if _enum_name(row.campaign.bidding_strategy_type) in SMART_BIDDING_STRATEGIES
    ]

    if not active_conversions and smart_bidding_campaigns:
        findings.append(
            Finding(
                check_id="no_conversion_actions_with_smart_bidding",
                severity=Severity.CRITICAL,
                title_es="No hay acciones de conversión activas con Smart Bidding habilitado",
                detail_es=(
                    "Las campañas "
                    + ", ".join(f"'{n}'" for n in smart_bidding_campaigns)
                    + " usan estrategias automáticas (Target CPA/ROAS/Maximizar conversiones) "
                    "que necesitan datos de conversión para pujar correctamente. Sin ellas, "
                    "Google Ads puede limitar drásticamente la entrega."
                ),
                suggested_action="adstool create-conversion-action --name <nombre> --category PHONE_CALL_LEAD --apply",
            )
        )
    elif not active_conversions:
        findings.append(
            Finding(
                check_id="no_conversion_actions",
                severity=Severity.WARNING,
                title_es="No hay acciones de conversión activas",
                detail_es="Sin seguimiento de conversiones no podrás medir leads/llamadas ni optimizar con Smart Bidding en el futuro.",
                suggested_action="adstool create-conversion-action --name <nombre> --category PHONE_CALL_LEAD --apply",
            )
        )
    else:
        findings.append(
            Finding(
                check_id="conversion_actions_ok",
                severity=Severity.OK,
                title_es=f"{len(active_conversions)} acción(es) de conversión activa(s)",
                detail_es="Seguimiento de conversiones configurado.",
            )
        )
    return findings


def check_customer(rows: list) -> list[Finding]:
    findings: list[Finding] = []
    for row in rows:
        customer = row.customer
        status = _enum_name(customer.status)
        if status != "ENABLED":
            findings.append(
                Finding(
                    check_id="customer_status",
                    severity=Severity.CRITICAL,
                    title_es=f"La cuenta '{customer.descriptive_name}' no está activa",
                    detail_es=f"Estado de la cuenta: {status}. Revisa el estado de facturación en la UI de Google Ads.",
                    resource_name=f"customers/{customer.id}",
                )
            )
        else:
            findings.append(
                Finding(
                    check_id="customer_status_ok",
                    severity=Severity.OK,
                    title_es=f"Cuenta '{customer.descriptive_name}' activa",
                    detail_es=f"Moneda: {customer.currency_code}, zona horaria: {customer.time_zone}.",
                    resource_name=f"customers/{customer.id}",
                )
            )
    return findings


def run_diagnostics(client, customer_id: str, campaign_id: str | None = None) -> DiagnosticReport:
    """Ejecuta todas las consultas GAQL y agrega los hallazgos en un DiagnosticReport."""

    def scoped(query: str) -> str:
        if campaign_id:
            connector = "AND" if "WHERE" in query else "WHERE"
            return f"{query.strip()}\n{connector} campaign.id = {campaign_id}"
        return query

    campaign_rows = list(run_query(client, customer_id, scoped(queries.CAMPAIGN_STATUS)))
    budget_rows = list(run_query(client, customer_id, scoped(queries.CAMPAIGN_BUDGET)))
    ad_rows = list(run_query(client, customer_id, scoped(queries.AD_APPROVAL_STATUS)))
    keyword_rows = list(run_query(client, customer_id, scoped(queries.KEYWORD_VIEW)))
    negative_rows = list(
        run_query(client, customer_id, scoped(queries.CAMPAIGN_NEGATIVE_KEYWORDS))
    )
    location_rows = list(
        run_query(client, customer_id, scoped(queries.CAMPAIGN_LOCATION_TARGETING))
    )
    language_rows = list(
        run_query(client, customer_id, scoped(queries.CAMPAIGN_LANGUAGE_TARGETING))
    )
    conversion_rows = list(run_query(client, customer_id, queries.CONVERSION_ACTIONS))
    customer_rows = list(run_query(client, customer_id, queries.CUSTOMER_INFO))

    report = DiagnosticReport(
        customer_id=customer_id,
        campaign_scope=f"campaña {campaign_id}" if campaign_id else "todas las campañas activas",
    )

    for finding in check_customer(customer_rows):
        report.add(finding)
    for finding in check_campaign_status(campaign_rows):
        report.add(finding)
    for finding in check_budgets(budget_rows):
        report.add(finding)
    for finding in check_ad_approval(ad_rows):
        report.add(finding)
    for finding in check_keywords(keyword_rows):
        report.add(finding)
    for finding in check_negative_keywords(keyword_rows, negative_rows):
        report.add(finding)
    for finding in check_geo_language(location_rows, language_rows):
        report.add(finding)
    for finding in check_conversions(conversion_rows, campaign_rows):
        report.add(finding)

    return report
