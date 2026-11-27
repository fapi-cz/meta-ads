import argparse
import json
import sys
from pathlib import Path


SKILLS = Path(__file__).resolve().parents[2]
for skill in ("meta-ads-setup", "meta-ads-test", "meta-ads-utm"):
    sys.path.insert(0, str(SKILLS / skill / "scripts"))
from test_ads import check_budget, check_time
from meta_reads import cli_read, require_account, rows, selected_account
from utm import check_ad, check_url, creative_links, read_ad_creative


def form_ids(value):
    if isinstance(value, list):
        for item in value:
            yield from form_ids(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            if key in {"lead_gen_form_id", "leadgen_form_id"}:
                yield str(item)
            elif isinstance(item, (dict, list)):
                yield from form_ids(item)


def check_form(ad, page_id, form_id, ref_code):
    creative = read_ad_creative(ad, cli_read)
    story = creative.get("object_story_spec") or {}
    if str(story.get("page_id")) != page_id:
        raise ValueError(f"Reklama {ad['id']} používá jinou Facebook stránku.")
    creative_spec = [story, creative.get("asset_feed_spec")]
    ids = set(form_ids(creative_spec))
    if ids != {form_id}:
        raise ValueError(f"Reklama {ad['id']} neprokázala vazbu na formulář {form_id}.")
    for link in set(creative_links(creative_spec, allow_forms=True)):
        if link.rstrip("/") not in {"http://fb.me", "https://fb.me"}:
            check_url(link, creative.get("url_tags") or "", ref_code)
    return {"creative_id": str(creative["id"]), "form_id": form_id}


def require_saved(entity, expected_id, account):
    require_account(entity, account)
    if str(entity.get("id")) != expected_id or entity.get("status") != "PAUSED":
        raise ValueError(f"Meta nevrátila očekávaný objekt {expected_id} ve stavu PAUSED.")


def check(args):
    expected_ads = set(args.ad_id)
    if len(expected_ads) != len(args.ad_id) or not all(
        value.isdigit() for value in (args.campaign_id, args.adset_id, *expected_ads)
    ):
        raise ValueError("Zadejte jedinečná číselná ID objektů.")
    if args.budget_minor <= 0:
        raise ValueError("Zadejte kladný rozpočet v menších jednotkách.")
    if args.form_id and (not args.page_id or not args.page_id.isdigit() or not args.form_id.isdigit()):
        raise ValueError("Pro okamžitý formulář zadejte číselné ID formuláře a Facebook stránky.")

    account = selected_account()
    campaign = cli_read(
        "campaign", "get", args.campaign_id, "--fields",
        "id,account_id,status,objective,daily_budget,lifetime_budget",
    )
    require_saved(campaign, args.campaign_id, account)
    adsets = rows(cli_read(
        "adset", "list", args.campaign_id, "--limit", "2", "--fields",
        "id,account_id,campaign_id,status,daily_budget,lifetime_budget,start_time,end_time,destination_type,optimization_goal,promoted_object",
    ))
    if len(adsets) != 1 or str(adsets[0].get("campaign_id")) != args.campaign_id:
        raise ValueError("Uložená kampaň musí mít právě jednu odpovídající sadu.")
    adset = adsets[0]
    require_saved(adset, args.adset_id, account)
    check_budget(campaign, adset, args.type, args.budget_minor)
    check_time(adset.get("start_time"), args.start_time, "Začátek")
    check_time(adset.get("end_time"), args.end_time, "Konec")
    if args.form_id:
        page = (adset.get("promoted_object") or {}).get("page_id")
        native_route = (
            campaign.get("objective") == "OUTCOME_LEADS"
            and adset.get("destination_type") == "ON_AD"
            and adset.get("optimization_goal") == "LEAD_GENERATION"
            and str(page) == args.page_id
        )
        if not native_route:
            raise ValueError("Uložený cíl, místo konverze nebo stránka neodpovídá okamžitému formuláři.")
    elif adset.get("destination_type") != "WEBSITE":
        raise ValueError("Uložená sada nevede na web.")

    ads = rows(cli_read(
        "ad", "list", args.adset_id, "--limit", str(len(expected_ads) + 1), "--fields",
        "id,account_id,adset_id,status,creative",
    ))
    if len(ads) != len(expected_ads) or {str(ad["id"]) for ad in ads} != expected_ads:
        raise ValueError("Uložená sada obsahuje jiný počet nebo jiná ID reklam, než vznikla pro briefing.")
    verified = []
    for ad in ads:
        ad_id = str(ad["id"])
        require_saved(ad, ad_id, account)
        if str(ad.get("adset_id")) != args.adset_id:
            raise ValueError(f"Reklama {ad_id} patří do jiné sady.")
        if args.form_id:
            result = check_form(ad, args.page_id, args.form_id, args.ref_code)
        else:
            result = check_ad(ad, args.ref_code, cli_read, args.web_url)
        verified.append({"ad_id": ad_id, **result})

    return {
        "account": account,
        "campaign_id": args.campaign_id,
        "adset_id": args.adset_id,
        "ads": verified,
        "status": "PAUSED",
        "budget_type": args.type,
        "budget_minor": args.budget_minor,
        "start_time": adset["start_time"],
        "end_time": adset["end_time"],
    }


def main():
    parser = argparse.ArgumentParser(description="Ověř uložení pozastavené webinářové kampaně.")
    parser.add_argument("--campaign-id", required=True)
    parser.add_argument("--adset-id", required=True)
    parser.add_argument("--ad-id", action="append", required=True)
    parser.add_argument("--type", choices=("daily", "lifetime"), required=True)
    parser.add_argument("--budget-minor", type=int, required=True)
    parser.add_argument("--start-time", required=True)
    parser.add_argument("--end-time", required=True)
    route = parser.add_mutually_exclusive_group(required=True)
    route.add_argument("--web-url")
    route.add_argument("--form-id")
    parser.add_argument("--page-id")
    parser.add_argument("--ref-code")
    try:
        print(json.dumps(check(parser.parse_args()), ensure_ascii=False))
    except (KeyError, TypeError, AttributeError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
