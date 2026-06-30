"""Interfaz de línea de comandos de adstool."""

from __future__ import annotations

import argparse
import csv
import sys

from rich.console import Console

from adstool.client import get_client_and_customer_id
from adstool.diagnostics.checks import run_diagnostics
from adstool.diagnostics.runner import run_query
from adstool.errors import print_friendly_error
from adstool.fixes.budgets import build_update_budget_plan
from adstool.fixes.bids import build_update_keyword_bid_plan, build_update_target_cpa_plan
from adstool.fixes.conversions import build_create_conversion_action_plan
from adstool.fixes.keywords import SEED_KEYWORDS_CERRAJERIA, build_add_keywords_plan
from adstool.fixes.plan import ChangePlan, GuardrailExceeded
from adstool.report.console import render_report
from adstool.report.markdown import append_applied_changes, write_report

MICROS = 1_000_000


def euros_to_micros(value: float) -> int:
    return int(round(value * MICROS))


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--customer-id", help="Customer ID de la cuenta de Google Ads (sin guiones)")
    parser.add_argument("--config", help="Ruta a google-ads.yaml (por defecto: ./google-ads.yaml)")


def _add_apply_args(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry-run", action="store_true", default=True, help="(por defecto) muestra el plan sin aplicar cambios")
    group.add_argument("--apply", action="store_true", help="aplica los cambios tras confirmación")
    parser.add_argument("--yes-i-am-sure", action="store_true", help="aplica sin pedir confirmación interactiva")


def _confirm_and_apply(plan: ChangePlan, args: argparse.Namespace) -> list[str]:
    if not args.apply:
        print(plan.render_dry_run())
        return []
    return plan.apply(assume_yes=args.yes_i_am_sure)


def cmd_diagnose(args: argparse.Namespace) -> int:
    client, customer_id = get_client_and_customer_id(args.config, args.customer_id)
    console = Console()
    try:
        report = run_diagnostics(client, customer_id, campaign_id=args.campaign_id)
    except Exception as exc:  # noqa: BLE001
        print_friendly_error(exc)
        return 1

    if args.output in ("console", "both"):
        render_report(report, console=console)

    if args.output in ("markdown", "both"):
        path = write_report(report, output_dir=args.output_dir)
        console.print(f"\nInforme guardado en: {path}")

    return 0


def _read_keywords_file(path: str) -> list[tuple[str, str]]:
    keywords: list[tuple[str, str]] = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if not row or len(row) < 2:
                continue
            text, match_type = row[0].strip(), row[1].strip().upper()
            if text.lower() == "text" and match_type == "MATCH_TYPE":
                continue  # encabezado opcional
            keywords.append((text, match_type))
    return keywords


def cmd_add_keywords(args: argparse.Namespace) -> int:
    client, customer_id = get_client_and_customer_id(args.config, args.customer_id)

    keywords: list[tuple[str, str]] = []
    if args.keywords_file:
        keywords.extend(_read_keywords_file(args.keywords_file))
    if args.keyword:
        for item in args.keyword:
            text, _, match_type = item.partition(":")
            keywords.append((text.strip(), (match_type or "PHRASE").strip().upper()))
    if not keywords and args.use_seed_list:
        keywords = SEED_KEYWORDS_CERRAJERIA

    if not keywords:
        print(
            "No se han indicado palabras clave. Usa --keywords-file, --keyword "
            "o --use-seed-list.",
            file=sys.stderr,
        )
        return 1

    plan = build_add_keywords_plan(client, customer_id, args.ad_group_id, keywords)
    try:
        _confirm_and_apply(plan, args)
    except Exception as exc:  # noqa: BLE001
        print_friendly_error(exc)
        return 1
    return 0


def cmd_update_budget(args: argparse.Namespace) -> int:
    client, customer_id = get_client_and_customer_id(args.config, args.customer_id)

    rows = list(
        run_query(
            client,
            customer_id,
            "SELECT campaign_budget.resource_name, campaign_budget.amount_micros "
            "FROM campaign_budget WHERE campaign.id = "
            f"{args.campaign_id}",
        )
    )
    if not rows:
        print(f"No se ha encontrado presupuesto para la campaña {args.campaign_id}.", file=sys.stderr)
        return 1
    budget = rows[0].campaign_budget

    try:
        plan = build_update_budget_plan(
            client,
            customer_id,
            budget.resource_name,
            budget.amount_micros,
            euros_to_micros(args.daily_budget),
            force=args.force,
        )
    except GuardrailExceeded as exc:
        print(f"Operación bloqueada por seguridad: {exc}", file=sys.stderr)
        return 1

    try:
        _confirm_and_apply(plan, args)
    except Exception as exc:  # noqa: BLE001
        print_friendly_error(exc)
        return 1
    return 0


def cmd_update_bid(args: argparse.Namespace) -> int:
    client, customer_id = get_client_and_customer_id(args.config, args.customer_id)

    if args.target_cpa is not None:
        rows = list(
            run_query(
                client,
                customer_id,
                "SELECT campaign.resource_name, campaign.target_cpa.target_cpa_micros "
                f"FROM campaign WHERE campaign.id = {args.campaign_id}",
            )
        )
        if not rows:
            print(f"No se ha encontrado la campaña {args.campaign_id}.", file=sys.stderr)
            return 1
        campaign = rows[0].campaign
        plan = build_update_target_cpa_plan(
            client,
            customer_id,
            campaign.resource_name,
            campaign.target_cpa.target_cpa_micros,
            euros_to_micros(args.target_cpa),
        )
    else:
        criterion_service = client.get_service("AdGroupCriterionService")
        if args.criterion_id:
            criterion_ids = [args.criterion_id]
        else:
            rows = list(
                run_query(
                    client,
                    customer_id,
                    "SELECT ad_group_criterion.criterion_id FROM keyword_view "
                    f"WHERE ad_group.id = {args.ad_group_id} "
                    "AND ad_group_criterion.status = 'ENABLED'",
                )
            )
            criterion_ids = [str(row.ad_group_criterion.criterion_id) for row in rows]

        if not criterion_ids:
            print("No se han encontrado palabras clave activas para actualizar.", file=sys.stderr)
            return 1

        combined = ChangePlan()
        new_bid_micros = euros_to_micros(args.cpc_bid)
        for criterion_id in criterion_ids:
            resource_name = criterion_service.ad_group_criterion_path(
                customer_id, args.ad_group_id, criterion_id
            )
            single_plan = build_update_keyword_bid_plan(
                client, customer_id, resource_name, current_bid_micros=0, new_bid_micros=new_bid_micros
            )
            for op in single_plan.operations:
                combined.add(op)
        plan = combined

    try:
        _confirm_and_apply(plan, args)
    except Exception as exc:  # noqa: BLE001
        print_friendly_error(exc)
        return 1
    return 0


def cmd_create_conversion_action(args: argparse.Namespace) -> int:
    client, customer_id = get_client_and_customer_id(args.config, args.customer_id)
    plan = build_create_conversion_action_plan(
        client, customer_id, args.name, args.category, args.type
    )
    try:
        _confirm_and_apply(plan, args)
    except Exception as exc:  # noqa: BLE001
        print_friendly_error(exc)
        return 1
    return 0


def cmd_fix(args: argparse.Namespace) -> int:
    client, customer_id = get_client_and_customer_id(args.config, args.customer_id)
    console = Console()

    try:
        report = run_diagnostics(client, customer_id, campaign_id=args.campaign_id)
    except Exception as exc:  # noqa: BLE001
        print_friendly_error(exc)
        return 1

    render_report(report, console=console)
    md_path = write_report(report, output_dir=args.output_dir)
    console.print(f"\nInforme guardado en: {md_path}")

    combined = ChangePlan()
    for finding in report.findings:
        if finding.check_id == "ad_group_no_keywords" and finding.resource_name:
            ad_group_id = finding.resource_name.rsplit("/", 1)[-1]
            kw_plan = build_add_keywords_plan(
                client, customer_id, ad_group_id, SEED_KEYWORDS_CERRAJERIA
            )
            for op in kw_plan.operations:
                combined.add(op)

        elif finding.check_id in ("no_conversion_actions", "no_conversion_actions_with_smart_bidding"):
            conv_plan = build_create_conversion_action_plan(
                client, customer_id, "Contacto web (lockercuenca.es)", "CONTACT", "WEBPAGE"
            )
            for op in conv_plan.operations:
                combined.add(op)

        elif finding.check_id in ("budget_zero", "budget_low") and finding.resource_name:
            try:
                budget_plan = _propose_budget_fix(client, customer_id, finding.resource_name)
            except GuardrailExceeded as exc:
                console.print(f"[yellow]Aviso: {exc}[/yellow]")
                continue
            if budget_plan:
                for op in budget_plan.operations:
                    combined.add(op)

    console.print("\n[bold]Correcciones automáticas propuestas (seguras y aditivas):[/bold]")
    try:
        results = _confirm_and_apply(combined, args)
    except Exception as exc:  # noqa: BLE001
        print_friendly_error(exc)
        return 1

    if results:
        append_applied_changes(md_path, results)
    return 0


def _propose_budget_fix(client, customer_id: str, budget_resource_name: str) -> ChangePlan | None:
    rows = list(
        run_query(
            client,
            customer_id,
            "SELECT campaign_budget.amount_micros, "
            "campaign_budget.recommended_budget_amount_micros FROM campaign_budget "
            f"WHERE campaign_budget.resource_name = '{budget_resource_name}'",
        )
    )
    if not rows:
        return None
    budget = rows[0].campaign_budget
    current = budget.amount_micros
    recommended = budget.recommended_budget_amount_micros or 0
    new_amount = recommended if recommended > current else max(current * 2, 1_000_000)
    return build_update_budget_plan(client, customer_id, budget_resource_name, current, new_amount)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="adstool",
        description="Diagnóstico y corrección de campañas de Google Ads (lockercuenca.es).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_diagnose = subparsers.add_parser("diagnose", help="Diagnostica por qué una campaña no tiene impresiones")
    _add_common_args(p_diagnose)
    p_diagnose.add_argument("--campaign-id", help="Limita el diagnóstico a una campaña concreta")
    p_diagnose.add_argument("--output", choices=["console", "markdown", "both"], default="both")
    p_diagnose.add_argument("--output-dir", default="reports")
    p_diagnose.set_defaults(func=cmd_diagnose)

    p_add_kw = subparsers.add_parser("add-keywords", help="Añade palabras clave a un grupo de anuncios")
    _add_common_args(p_add_kw)
    p_add_kw.add_argument("--ad-group-id", required=True)
    p_add_kw.add_argument("--keywords-file", help="CSV con columnas text,match_type")
    p_add_kw.add_argument("--keyword", action="append", help="Formato texto:match_type, repetible")
    p_add_kw.add_argument(
        "--use-seed-list",
        action="store_true",
        help="Usa la lista semilla de cerrajería si no se indican keywords",
    )
    _add_apply_args(p_add_kw)
    p_add_kw.set_defaults(func=cmd_add_keywords)

    p_budget = subparsers.add_parser("update-budget", help="Sube el presupuesto diario de una campaña")
    _add_common_args(p_budget)
    p_budget.add_argument("--campaign-id", required=True)
    p_budget.add_argument("--daily-budget", type=float, required=True, help="Importe en la moneda de la cuenta")
    p_budget.add_argument("--force", action="store_true", help="Permite superar el límite de seguridad (5x)")
    _add_apply_args(p_budget)
    p_budget.set_defaults(func=cmd_update_budget)

    p_bid = subparsers.add_parser("update-bid", help="Sube la puja de palabras clave o el Target CPA")
    _add_common_args(p_bid)
    p_bid.add_argument("--ad-group-id", help="Requerido para pujas manuales CPC")
    p_bid.add_argument("--criterion-id", help="Actualiza solo esta keyword (si no se indica, actualiza todas las del ad group)")
    p_bid.add_argument("--cpc-bid", type=float, help="Nueva puja CPC manual")
    p_bid.add_argument("--campaign-id", help="Requerido junto con --target-cpa")
    p_bid.add_argument("--target-cpa", type=float, help="Nuevo Target CPA (campañas con Smart Bidding)")
    _add_apply_args(p_bid)
    p_bid.set_defaults(func=cmd_update_bid)

    p_conv = subparsers.add_parser("create-conversion-action", help="Crea una acción de conversión")
    _add_common_args(p_conv)
    p_conv.add_argument("--name", required=True)
    p_conv.add_argument("--category", default="CONTACT", help="Ej: CONTACT, PHONE_CALL_LEAD, SUBMIT_LEAD_FORM")
    p_conv.add_argument("--type", default="WEBPAGE", help="Ej: WEBPAGE, CLICK_TO_CALL")
    _add_apply_args(p_conv)
    p_conv.set_defaults(func=cmd_create_conversion_action)

    p_fix = subparsers.add_parser("fix", help="Diagnostica y propone/aplica correcciones seguras y aditivas")
    _add_common_args(p_fix)
    p_fix.add_argument("--campaign-id", required=True)
    p_fix.add_argument("--output-dir", default="reports")
    _add_apply_args(p_fix)
    p_fix.set_defaults(func=cmd_fix)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
