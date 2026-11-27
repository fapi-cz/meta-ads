import argparse
import json
import sys
from pathlib import Path
from urllib.parse import quote, unquote_plus, urlsplit


META_TAGS = (
    "utm_source={{site_source_name}}",
    "utm_medium={{placement}}",
    "utm_campaign={{campaign.id}}",
    "utm_term={{adset.id}}",
    "utm_id={{ad.id}}",
)


def without_tracking(query, include_ref_code):
    kept = []
    for parameter in filter(None, query.split("&")):
        key, _, value = parameter.partition("=")
        key = unquote_plus(key).casefold()
        if key.startswith("utm_") or (include_ref_code and key == "ref_code"):
            continue
        if unquote_plus(value) == "{{ad.id}}":
            continue
        kept.append(parameter)
    return kept


def prepare(url, tags, ref_code):
    if any(character.isspace() for character in url):
        raise ValueError("Cílová URL obsahuje mezeru nebo řídicí znak.")
    destination = urlsplit(url)
    if destination.scheme not in {"http", "https"} or not destination.hostname:
        raise ValueError("Zadejte úplnou webovou adresu začínající https:// nebo http://.")
    if destination.username is not None:
        raise ValueError("Cílová URL obsahuje přihlašovací údaje.")
    if "#" in tags:
        raise ValueError("Parametry URL obsahují neplatný znak #.")

    include_ref_code = ref_code is not None
    tracking = list(META_TAGS)
    if include_ref_code:
        if not ref_code.strip() or "{" in ref_code or "}" in ref_code:
            raise ValueError("FAPI ref_code musí mít skutečnou statickou hodnotu.")
        tracking.append(f"ref_code={quote(ref_code.strip(), safe='')}")

    query = "&".join(without_tracking(destination.query, include_ref_code))
    tracking.extend(without_tracking(tags.removeprefix("?"), include_ref_code))
    return {"url": destination._replace(query=query).geturl(), "url_tags": "&".join(tracking)}


def check_url(url, tags, ref_code):
    if prepare(url, tags, ref_code) != {"url": url, "url_tags": tags}:
        raise ValueError("Uložená URL nebo url_tags neodpovídají povinné UTM šabloně.")


def creative_links(value, allow_forms=False):
    if isinstance(value, list):
        for item in value:
            yield from creative_links(item, allow_forms)
    elif isinstance(value, dict):
        if not allow_forms and (value.get("lead_gen_form_id") or value.get("leadgen_form_id")):
            raise ValueError("Okamžitý formulář vyžaduje samostatné ověření závěrečného odkazu.")
        if value.get("url_tags"):
            raise ValueError("Kreativa má další parametry na jednotlivých odkazech. Použijte společné url_tags.")
        for key, item in value.items():
            if key in {"link", "website_url"} and isinstance(item, str) and item.startswith(("https://", "http://")):
                yield item
            elif isinstance(item, (list, dict)):
                yield from creative_links(item, allow_forms)


def read_ad_creative(ad, cli_read):
    creative_ref = ad.get("creative")
    creative_id = creative_ref.get("id") if isinstance(creative_ref, dict) else creative_ref
    if not creative_id or not str(creative_id).isdigit():
        raise ValueError("Reklama nevrátila ID uložené kreativy.")
    creative = cli_read(
        "creative", "get", str(creative_id),
        "--fields", "id,url_tags,object_story_spec,asset_feed_spec",
    )
    if str(creative.get("id")) != str(creative_id):
        raise ValueError("Meta vrátila jiné ID kreativy než to připojené k reklamě.")
    return creative


def check_ad(ad, ref_code, cli_read, expected_url=None):
    creative = read_ad_creative(ad, cli_read)
    links = set(creative_links([creative.get("object_story_spec"), creative.get("asset_feed_spec")]))
    if not links:
        raise ValueError("Meta nevrátila ověřitelnou webovou adresu uložené kreativy.")
    if expected_url is not None and links != {expected_url}:
        raise ValueError("Uložený webový odkaz neodpovídá nové potvrzené adrese.")
    for link in sorted(links):
        check_url(link, creative.get("url_tags") or "", ref_code)
    return {"verified": True, "creative_id": str(creative["id"]), "links": len(links)}


def main():
    parser = argparse.ArgumentParser(description="Příprava a kontrola povinných UTM pro Meta Ads.")
    parser.add_argument("action", choices=("prepare", "check", "check-ad"))
    parser.add_argument("--url")
    parser.add_argument("--tags", default="")
    parser.add_argument("--ad-id")
    parser.add_argument("--ref-code")
    args = parser.parse_args()

    try:
        if args.action == "check-ad":
            if not args.ad_id or not args.ad_id.isdigit():
                raise ValueError("Pro kontrolu v Meta Ads zadejte číselné ID reklamy.")
            sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "meta-ads-setup" / "scripts"))
            from meta_reads import cli_read, require_account, selected_account

            ad = cli_read("ad", "get", args.ad_id, "--fields", "id,account_id,creative")
            require_account(ad, selected_account())
            print(json.dumps(check_ad(ad, args.ref_code, cli_read), ensure_ascii=False))
        elif not args.url:
            raise ValueError("Zadejte webovou adresu pomocí --url.")
        elif args.action == "check":
            check_url(args.url, args.tags, args.ref_code)
            print("UTM ověřeny.")
        else:
            print(json.dumps(prepare(args.url, args.tags, args.ref_code), ensure_ascii=False))
    except ValueError as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
