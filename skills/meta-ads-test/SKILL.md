---
name: meta-ads-test
description: Připrav, založ a ověř testovací reklamu na Facebooku nebo Instagramu. Použij jednu kampaň, jednu sadu a jednu reklamu, výchozí denní rozpočet 200 Kč a povinné UTM.
---

# Testovací reklama v Metě

Pro jednu testovanou variantu použij **1 kampaň → 1 sada reklam → 1 reklama**. Zjisti, co má test ověřit a podle jakého výsledku ho majitel vyhodnotí. Pokud porovnává více variant, drž rozpočet, publikum, čas a umístění srovnatelné. Rozměry téhož banneru nebo videa pro různá umístění patří do jedné reklamy, pokud to zvolený formát v Metě podporuje.

## Příprava

1. Ověř název a ID reklamního účtu, měnu a časové pásmo. Při chybějícím připojení použij [meta-ads-setup](../meta-ads-setup/SKILL.md). Pro čtení, tvorbu a případnou aktivaci použij přednostně oficiální Meta Ads CLI přes `cli-json`. Meta Ads MCP použij, pokud CLI daný krok nepodporuje nebo není dostupné. Skripty spouštěj přes `meta-ads.sh python` podle [postupu pro daný systém](../meta-ads-setup/references/platforms.md).
2. Z briefu, dostupných podkladů a případné referenční kampaně zjisti cíl, cílovou URL, identitu FB stránky či IG účtu, text a soubor nebo ID média, publikum, rozpočet, měnu a dobu běhu. Pro konverzní cíl ověř také odpovídající datovou sadu a událost. Dotaž se pouze na chybějící rozhodnutí. Při kopírování použij jen nastavení, která odpovídají zadání testu.
3. Urči rozpočet podle pravidel níže. Před vytvořením nebo duplikováním reklamy použij [meta-ads-utm](../meta-ads-utm/SKILL.md) na cílový odkaz a případnou zděděnou kreativu. Hodnotu `url_tags` připrav předem a při tvorbě kreativy tohoto testu ji ulož přednostně přes CLI. Chybějící nebo neověřitelné UTM blokuje uložení reklamy k doručování i její spuštění.

## Rozpočet

- Pro jeden test v CZK použij **200 Kč denně na kampaň**, pokud uživatel neurčí jinou částku nebo typ rozpočtu. U účtu v jiné měně si vyžádej částku v jeho měně. Pro běžnou netestovací kampaň FAPI platí samostatný výchozí rozpočet **1 000 Kč denně na kampaň**. Ve FAPI se zadání „1 000 Kč na kampaň“ bez dalšího upřesnění chápe jako denní rozpočet.
- Rozpočet nastav na kampani. Pro denní rozpočet použij `daily_budget` a pro částku za celou dobu použij `lifetime_budget` s termínem konce. Částku za celou dobu přebírej ze zadání. Výchozí denní částky v účtu s měnou CZK odpovídají hodnotám `20000` u testu a `100000` u běžné kampaně. Zkontroluj uloženou hodnotu a typ. Vlastní rozpočet sady je při rozpočtu na kampani prázdný.
- Před spuštěním uveď počet testovacích kampaní a součet denních rozpočtů. Částky za celou dobu uveď s jejich termínem konce. Tři varianty při výchozí částce znamenají tři samostatné testy za 600 Kč denně celkem. Různá umístění téhož média v jedné reklamě sdílejí její rozpočet. Pokud Meta částku odmítne kvůli minimu, zjisti požadovanou mez a vyžádej si schválenou částku.
- Po zápisu ověř uložený rozpočet, jeho typ, termín a počet kampaní v požadovaném testu. Při změně běžícího testu načti i dosavadní útratu a aktuální stav doručování. [Rozpočet kampaně v Marketing API](https://developers.facebook.com/docs/marketing-api/reference/adcampaigngroup/)

Výpočet udělá `scripts/test_ads.py budget --currency CZK`. Skript vrací `budget_minor` pro jednu kampaň a `total_minor` pro zadaný `--count`. Podporuje také `--kind campaign`, `--type lifetime` a `--amount` ze zadání. U jiné měny předáš i ověřený `--minor-digits`. Použij Python z instalace [meta-ads-setup](../meta-ads-setup/SKILL.md).

## Založení v účtu

- Na požadavek na vytvoření založ kampaň, její jednu sadu, kreativu s připraveným `url_tags` a jednu reklamu navázanou na tuto sadu a kreativu. Kampaň, sadu i reklamu vytvoř se stavem `PAUSED`. U rozpracovaného testu nejdřív přečti jeho uložené objekty a pokračuj od prvního chybějícího kroku. Po nejasném výsledku zápisu ověř stav v Metě, než použiješ jinou cestu nebo pokus zopakuješ.
- Zkontroluj uložený test pomocí `scripts/test_ads.py check --campaign-id ID --type daily --budget-minor HODNOTA --status PAUSED`. Skript načte skutečné objekty a ověří účet, vazby a počty **1 / 1 / 1**, rozpočet, stav a UTM. Předej dostupná očekávání ze zadání jako `--adset-id`, `--ad-id`, `--start-time` a `--end-time` v ISO 8601 s časovým posunem, `--countries CZ,SK` a `--ref-code KOD` u FAPI. Čas, měnu a cílení určuj ze schváleného briefu. U složitějšího cílení zkontroluj význam nastavení podle briefu.
- Pokud uživatel požádal i o spuštění, po ověření UTM aktivuj požadovanou reklamu a sadu v pozastavené kampani a kampaň zapni jako poslední. Znovu přečti ID, UTM a stav. Rozliš uložený stav `ACTIVE` od doručování, kontroly Metou nebo plánovaného startu.
- Vrať název a ID účtu, všech tří objektů, rozpočet, termín, stav a výsledek kontroly UTM. Při rozpracovaném testu uveď uložená ID a chybějící krok.
- Až uživatel požádá o výsledky, načti je pomocí [meta-ads-evaluate](../meta-ads-evaluate/SKILL.md). Použij uložená ID a cíl testu.

## Příkazy pro agenta

Se skutečnými hodnotami použij kategorie `campaign create`, `adset create --campaign-id`, `creative create --link-url --url-tags` a `ad create --adset-id --creative-id`. Doplň povinné parametry podle `--help` u každé kategorie. Pro doručování v EU přidej jméno příjemce výhod a plátce do údajů sady. Použij absolutní cestu k souboru. Rozpočet se předává v menších jednotkách měny účtu, například 200 Kč je `20000` v účtu s měnou CZK.

Spuštění uděláš příslušnými příkazy `update --status ACTIVE`. Zopakuj `scripts/test_ads.py check` s očekávaným stavem `ACTIVE`. [Struktura objektů v Marketing API](https://developers.facebook.com/docs/marketing-api/reference/v27.0/)
