import argparse
import json
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


def main():
    parser = argparse.ArgumentParser(description="Příprava a kontrola povinných UTM pro Meta Ads.")
    parser.add_argument("action", choices=("prepare", "check"))
    parser.add_argument("--url", required=True)
    parser.add_argument("--tags", default="")
    parser.add_argument("--ref-code")
    args = parser.parse_args()

    try:
        expected = prepare(args.url, args.tags, args.ref_code)
    except ValueError as error:
        parser.exit(1, f"{error}\n")

    if args.action == "check":
        if expected != {"url": args.url, "url_tags": args.tags}:
            parser.exit(1, "Uložená URL nebo url_tags neodpovídají povinné UTM šabloně.\n")
        print("UTM ověřeny.")
        return

    print(json.dumps(expected, ensure_ascii=False))


if __name__ == "__main__":
    main()
