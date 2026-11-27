import argparse
import json
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path


def number(value):
    if value is None or value == "":
        return None
    try:
        parsed = Decimal(str(value))
    except InvalidOperation:
        raise ValueError("Report obsahuje neplatnou číselnou hodnotu.") from None
    if not parsed.is_finite():
        raise ValueError("Report obsahuje nekonečnou nebo neurčitou hodnotu.")
    return parsed


def ratio(numerator, denominator, multiplier=1):
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return (numerator * multiplier / denominator).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def action_value(row, field, action_type):
    entries = row.get(field)
    if action_type is None or entries is None:
        return None
    values = [number(event.get("value")) for event in entries if event.get("action_type") == action_type]
    if len(values) > 1:
        raise ValueError(f"Pole {field} obsahuje více hodnot typu {action_type}. Ověřte dimenzi reportu.")
    return values[0] if values else None


def report_row(row, action_type, purchase_type, fapi):
    spend = number(row.get("spend"))
    impressions = number(row.get("impressions"))
    clicks = number(row.get("inline_link_clicks"))
    results = action_value(row, "actions", action_type)
    purchases = action_value(row, "actions", purchase_type)
    purchase_value = action_value(row, "action_values", purchase_type)
    report = {
        key: row.get(key)
        for key in ("campaign_id", "adset_id", "ad_id", "date_start", "date_stop", "account_currency")
    }
    report.update({
        "spend": spend,
        "impressions": impressions,
        "reach": number(row.get("reach")),
        "frequency": number(row.get("frequency")),
        "link_clicks": clicks,
        "link_ctr_percent": ratio(clicks, impressions, 100),
        "link_cpc": ratio(spend, clicks),
        "cpm": ratio(spend, impressions, 1000),
        "action_type": action_type,
        "results": results,
        "cost_per_result": ratio(spend, results),
        "meta_purchases": purchases,
        "meta_purchase_value": purchase_value,
        "meta_roas": ratio(purchase_value, spend),
    })
    fapi_values = fapi.get(str(row["ad_id"])) if row.get("ad_id") else None
    if fapi_values is not None:
        net_revenue = number(fapi_values.get("net_revenue"))
        new_customers = number(fapi_values.get("new_customers"))
        same_currency = bool(row.get("account_currency")) and row["account_currency"] == fapi_values.get("currency")
        report["fapi"] = {
            "currency": fapi_values.get("currency"),
            "paid_orders": number(fapi_values.get("paid_orders")),
            "refunds": number(fapi_values.get("refunds")),
            "net_revenue": net_revenue,
            "new_customers": new_customers,
            "roas": ratio(net_revenue, spend) if same_currency else None,
            "cac": ratio(spend, new_customers) if same_currency else None,
        }
    return report


def main():
    parser = argparse.ArgumentParser(description="Spočítej metriky z Meta Insights v JSON.")
    parser.add_argument("--action-type")
    parser.add_argument("--purchase-action-type")
    parser.add_argument("--fapi-summary", type=Path)
    args = parser.parse_args()

    try:
        payload = json.load(sys.stdin)
        data = payload.get("data") if isinstance(payload, dict) else payload
        if not isinstance(data, list):
            raise ValueError("Zadejte JSON s řádky Meta Insights.")
        fapi = json.loads(args.fapi_summary.read_text(encoding="utf-8")) if args.fapi_summary else {}
        output = {"data": [report_row(row, args.action_type, args.purchase_action_type, fapi) for row in data]}
        if isinstance(payload, dict) and payload.get("has_more"):
            output["has_more"] = True
    except (OSError, KeyError, TypeError, AttributeError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    print(json.dumps(output, default=str, ensure_ascii=False))


if __name__ == "__main__":
    main()
