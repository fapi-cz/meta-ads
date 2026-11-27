---
name: meta-ads-evaluate
description: Vyhodnoť Meta Ads kampaně a testy. Zjisti útratu, prokliky, leady, nákupy, cenu za výsledek a ROAS. Porovnej varianty nebo výsledky z Mety se zaplacenými objednávkami ve FAPI.
---

# Vyhodnocení Meta Ads

Použij pouze čtení. Ověř název, ID, měnu a časové pásmo účtu. Urči období, kampaň, sadu nebo reklamu podle ID a z briefu převezmi cíl testu a případnou cílovou cenu. Při shodě názvů potvrď cílové ID. Při chybějícím připojení použij [meta-ads-setup](../meta-ads-setup/SKILL.md).

## Načti výsledky

Použij Meta Ads MCP s odpovídajícími parametry nebo spusť oficiální CLI přes `meta-ads.sh`. Pro výpis i report použij [spouštěč pro daný systém](../meta-ads-setup/references/platforms.md). Urči obě hranice období v časovém pásmu účtu. V příkladu nahraď datum a ID hodnotami ze zadání. Případný nedokončený den uveď v reportu.

```bash
bash /absolute/path/to/meta-ads.sh cli-json insights get \
  --campaign-id 123456 --since 2026-11-01 --until 2026-11-07 \
  --time-increment all_days \
  --fields campaign_id,account_currency,date_start,date_stop,spend,impressions,reach,frequency,inline_link_clicks,actions,action_values
```

- Pro sadu nebo reklamu použij `--adset-id` nebo `--ad-id` a příslušné pole s ID. U struktury 1 kampaň / 1 sada / 1 reklama načti výsledek každé testované varianty jednou na stejné úrovni. Pro průběh použij `--time-increment daily`. Když CLI vrátí `has_more: true`, zkrať jednotlivá období nebo použij stránkování v MCP.
- Pro posledních N kampaní načti `id,name,created_time` a seřaď je podle vytvoření od nejnovější. Když výpis dosáhne `--limit`, ověř úplnost vyšším limitem nebo načti další stránky z Marketing API. Pokud uživatel neurčí období útraty, načti ji od vytvoření každé vybrané kampaně do aktuálního dne v časovém pásmu účtu.
- Použij stejné období, měnu, definici konverze a nastavení atribuce pro porovnávané řádky. Uveď okno atribuce, pokud je ověřitelné pro daný report. Pokud zdroj ukazuje jen atribuční nastavení sady, uveď ho jako nastavení sady. Dosah a frekvenci vezmi z celého období na vyhodnocované úrovni.
- Kampaně s malou útratou nejprve posuď podle efektivního stavu a termínu. Pojmenuj chybu přístupu, chybějící řádek nebo neznámou metriku podle toho, co zdroj skutečně vrátil. Zachovej číselnou nulu, pokud je doložená.

## Spočítej metriky a vysvětli výsledek

- Vyber odpovídající `action_type` podle cíle a řádku z Mety. Příbuzné souhrnné a dílčí typy téže konverze použij jen jednou. Surové řádky Insights předej jako JSON na standardní vstup `scripts/report.py --action-type TYP`. Při vyhodnocování nákupů a ROAS předej i `--purchase-action-type TYP_NAKUPU`. Skript spočítá CTR a CPC odkazu, CPM, počet a cenu za výsledek i ROAS. Hodnota `null` je nedostupná metrika.
- Pokud máš přístup k FAPI nebo jeho exportu, hledej uhrazené objednávky podle přesného `utm_id` reklamy. Porovnej `utm_campaign`, `utm_term` a `ref_code`, pokud jsou k dispozici. Samotný společný `ref_code` použij nejvýš pro souhrn kampaně, pokud ho jednoznačně identifikuje. Použij souhrn s každou platbou započítanou jednou i při zálohové a konečné faktuře. Pro výpočet skutečného ROAS a CAC předej soubor `--fapi-summary` jako JSON objekt podle ID reklamy. Hodnoty mohou mít pole `currency`, `paid_orders`, `refunds`, `net_revenue` bez DPH a `new_customers` s novými platícími zákazníky. Skript páruje podle `ad_id` a počítá poměry ve stejné měně. Výsledky z FAPI a konverze přiřazené Metou uveď ve vlastních sloupcích. Při nejasném přiřazení označ výsledek jako neověřený.
- Vrať stručnou tabulku po testech, období, měnu a závěr vzhledem k cíli. Varianty srovnej hlavně podle ceny nebo hodnoty požadovaného výsledku. Uveď počet výsledků, velikost vzorku a případné zpoždění konverzí. Když pro verdikt chybějí data, řekni, které měření pomůže rozhodnout.

[Přehled Meta Insights API](https://developers.facebook.com/docs/marketing-api/insights/)
