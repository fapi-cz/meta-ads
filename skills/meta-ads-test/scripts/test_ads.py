import argparse
import json
import sys
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


SKILLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILLS / "meta-ads-setup" / "scripts"))
sys.path.insert(0, str(SKILLS / "meta-ads-utm" / "scripts"))
from meta_reads import cli_read, require_account, rows, selected_account
from utm import check_ad


def budget(args):
    currency = args.currency.upper()
    amount = args.amount
    digits = args.minor_digits
    if currency == "CZK":
        digits = 2
        if amount is None and args.type == "daily":
            amount = "200" if args.kind == "test" else "1000"
    if amount is None or digits is None:
        raise ValueError("Zadejte schválenou částku a počet desetinných míst měny účtu.")
    if args.count < 1 or not 0 <= digits <= 4:
        raise ValueError("Počet kampaní musí být kladný a měna musí mít platnou přesnost.")
    try:
        minor = Decimal(amount).scaleb(digits)
    except InvalidOperation:
        raise ValueError("Rozpočet musí být číslo.") from None
    if not minor.is_finite() or minor <= 0 or minor != minor.to_integral_value():
        raise ValueError("Částka musí být kladná a vyjádřitelná v měně účtu.")
    return {
        "currency": currency,
        "type": args.type,
        "campaign_count": args.count,
        "budget_minor": int(minor),
        "total_minor": int(minor) * args.count,
    }


def only_child(entity, parent, fields):
    children = rows(cli_read(entity, "list", str(parent), "--limit", "2", "--fields", fields))
    if len(children) != 1:
        raise ValueError(f"Pod objektem {parent} musí být právě jeden {entity}. Načteno {len(children)}.")
    return children[0]


def check_time(value, expected, label):
    if expected is None:
        return
    try:
        saved_time = datetime.fromisoformat(value or "")
        expected_time = datetime.fromisoformat(expected)
    except (TypeError, ValueError):
        raise ValueError(f"{label} chybí nebo nemá platný formát ISO 8601.") from None
    if saved_time.utcoffset() is None or expected_time.utcoffset() is None or saved_time != expected_time:
        raise ValueError(f"{label} u uložené sady se liší od zadání.")


def check_budget(campaign, adset, budget_type, budget_minor):
    for field in ("daily_budget", "lifetime_budget"):
        expected = budget_minor if field == f"{budget_type}_budget" else 0
        if int(campaign.get(field) or 0) != expected or int(adset.get(field) or 0) != 0:
            raise ValueError("Uložená výše, typ nebo úroveň rozpočtu neodpovídá zadání.")


def check(args):
    if args.budget_minor <= 0 or not args.campaign_id.isdigit():
        raise ValueError("Zadejte číselné ID kampaně a kladný rozpočet v menších jednotkách.")
    account = selected_account()
    campaign = cli_read(
        "campaign", "get", args.campaign_id, "--fields",
        "id,account_id,status,effective_status,daily_budget,lifetime_budget",
    )
    adset = only_child(
        "adset", args.campaign_id,
        "id,account_id,campaign_id,status,effective_status,daily_budget,lifetime_budget,start_time,end_time,targeting",
    )
    ad = only_child("ad", adset["id"], "id,account_id,adset_id,status,effective_status,creative")
    if str(campaign["id"]) != args.campaign_id or str(adset.get("campaign_id")) != args.campaign_id:
        raise ValueError("Sada nepatří do ověřované kampaně.")
    if str(ad.get("adset_id")) != str(adset["id"]):
        raise ValueError("Reklama nepatří do ověřované sady.")
    for entity, expected_id in ((adset, args.adset_id), (ad, args.ad_id)):
        if expected_id is not None and str(entity["id"]) != expected_id:
            raise ValueError(f"Vrácený objekt {entity['id']} neodpovídá ID {expected_id} v zadání.")
    for entity in (campaign, adset, ad):
        require_account(entity, account)
        if entity.get("status") != args.status:
            raise ValueError(f"Objekt {entity['id']} nemá uložený stav {args.status}.")

    check_budget(campaign, adset, args.type, args.budget_minor)
    check_time(adset.get("start_time"), args.start_time, "Začátek")
    check_time(adset.get("end_time"), args.end_time, "Konec")
    if args.countries:
        targeting = adset.get("targeting") or {}
        countries = (targeting.get("geo_locations") or {}).get("countries") or []
        if set(countries) != set(args.countries.split(",")):
            raise ValueError("Uložené země cílení se liší od zadání.")

    return {
        "account": account,
        "campaign_id": args.campaign_id,
        "adset_id": str(adset["id"]),
        "ad_id": str(ad["id"]),
        "status": args.status,
        "effective_status": ad.get("effective_status"),
        "type": args.type,
        "budget_minor": args.budget_minor,
        "start_time": adset.get("start_time"),
        "end_time": adset.get("end_time"),
        "utm": check_ad(ad, args.ref_code, cli_read),
    }


def main():
    parser = argparse.ArgumentParser(description="Připrav a zkontroluj rozpočet nebo nastavení testu 1/1/1.")
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("budget")
    plan.add_argument("--currency", required=True)
    plan.add_argument("--type", choices=("daily", "lifetime"), default="daily")
    plan.add_argument("--kind", choices=("test", "campaign"), default="test")
    plan.add_argument("--amount")
    plan.add_argument("--minor-digits", type=int)
    plan.add_argument("--count", type=int, default=1)
    verify = commands.add_parser("check")
    verify.add_argument("--type", choices=("daily", "lifetime"), required=True)
    verify.add_argument("--budget-minor", type=int, required=True)
    verify.add_argument("--campaign-id", required=True)
    verify.add_argument("--adset-id")
    verify.add_argument("--ad-id")
    verify.add_argument("--status", choices=("PAUSED", "ACTIVE"), required=True)
    verify.add_argument("--start-time")
    verify.add_argument("--end-time")
    verify.add_argument("--countries")
    verify.add_argument("--ref-code")
    args = parser.parse_args()

    try:
        answer = budget(args) if args.command == "budget" else check(args)
    except (KeyError, TypeError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    print(json.dumps(answer, ensure_ascii=False))


if __name__ == "__main__":
    main()
