---
name: meta-ads-utm
description: Nastav nebo ověř povinné UTM pro Meta reklamy s odkazem na web v kurzu FAPI. Použij při založení, duplikaci, výměně kreativy, změně URL, spuštění reklamy, sady či kampaně a při kontrole měření, i když zadání UTM nezmiňuje.
---

# Povinné UTM pro Meta Ads

Každý cílový webový odkaz v reklamě musí mít úplné a ověřené UTM před spuštěním. Při zapnutí sady nebo kampaně ověř všechny reklamy s webovým odkazem, které by se mohly rozběhnout. Při vytváření, kopírování a výměně kreativy připrav UTM před zápisem a ověř na uložené kreativě. Při požadavku na pozastavení proveď pozastavení a ověř stav.

## Šablona

```text
utm_source={{site_source_name}}&utm_medium={{placement}}&utm_campaign={{campaign.id}}&utm_term={{adset.id}}&utm_id={{ad.id}}
```

Meta doplní zdroj, umístění a ID při prokliku. Pro kampaň měřenou ve FAPI přidej `&ref_code=KOD_KAMPANE` se skutečným statickým kódem z briefu. Chybějící kód si vyžádej. ID reklamy sleduj v `utm_id`.

## Nastavení a kontrola

1. Ověř reklamní účet a cílové ID. Urči skutečnou cílovou URL každého odkazu a přečti původní `url_tags` u kopírované nebo kontrolované reklamy. V Metě se pole jmenuje **Sledování → Parametry URL**. V Marketing API jde o `url_tags` na kreativě bez úvodního otazníku.
2. Pro přípravu spusť `scripts/utm.py prepare --url '<URL>' --tags '<původní url_tags>'` pomocí Pythonu 3.9 nebo novějšího. Můžeš použít Python z instalace [meta-ads-setup](../meta-ads-setup/SKILL.md) ve složce `~/.local/share/fapi-meta-ads-course/venv/bin/python` nebo ve zvoleném `FAPI_META_ADS_STATE_DIR`. U FAPI kampaně přidej `--ref-code '<kód>'`. Skript vrátí JSON s vyčištěnou `url` a novým `url_tags`. Uložíš tak UTM na jednom místě a zachováš ostatní parametry a fragment odkazu. Zkontroluj i starší aliasy ID reklamy přebrané z kampaně.
3. Ulož oba údaje do nové kreativy přes Meta Ads MCP, pokud jeho nástroj umožňuje nastavení cílové adresy a `url_tags`. Jinak použij `cli-json creative create --link-url '<URL>' --url-tags '<šablona>'` z [meta-ads-setup](../meta-ads-setup/SKILL.md). U změny existující reklamy nejdřív ověř, zda je přípustná úprava dané kreativy. Pokud se sdílí s jinými reklamami nebo změnu pole nástroj nepodporuje, vytvoř novou kreativu se stejnými schválenými podklady a přiřaď ji pouze požadované reklamě pomocí `ad update <ID> --creative-id <ID>`. Pokud by to změnilo formát nebo původní příspěvek, nejdřív vyjasni tuto změnu s uživatelem.
4. Spusť `scripts/utm.py check-ad --ad-id ID` s `--ref-code KOD` u FAPI kampaně. Skript načte přes CLI skutečnou reklamu, ověří její účet a přečte připojenou kreativu včetně odkazů v kartách a umístěních. Zkontroluje uloženou šablonu, kód FAPI, duplicity a makra. Při práci se samotnou URL a známými parametry použij `scripts/utm.py check`. Pokud přesměrování odstraní parametry, oprav cílovou cestu.
5. Při žádosti jen o kontrolu vrať výsledek a chybějící pole. Při povolené opravě a aktivaci ověř každou uloženou změnu. Pokud hodnotu nelze uložit nebo přečíst, pozastavenou reklamu ponech pozastavenou a popiš konkrétní překážku.

Okamžitý formulář, který celý probíhá v Metě, nemá pro odeslání leadu webový proklik. Pro lead použij údaje z Mety a u případného závěrečného odkazu nastav a ověř URL měření samostatně. Při požadavku na test s ověřeným UTM dokonči aktivaci až s ověřitelným webovým odkazem. [Parametry kreativy](https://developers.facebook.com/documentation/ads-commerce/marketing-api/reference/ad-creative) · [Závěrečný odkaz formuláře](https://developers.facebook.com/docs/graph-api/reference/page/leadgen_forms/)
