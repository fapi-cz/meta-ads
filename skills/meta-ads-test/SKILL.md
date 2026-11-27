---
name: meta-ads-test
description: Připrav, založ a ověř testovací reklamu na Facebooku nebo Instagramu v kurzu FAPI. Jeden test tvoří jedna kampaň, jedna sada reklam a jedna reklama s povinným UTM měřením.
---

# Testovací reklama v Metě

Pro jednu testovanou variantu použij **1 kampaň → 1 sada reklam → 1 reklama**. Zjisti, co má test ověřit a podle jakého výsledku ho majitel vyhodnotí. Pokud porovnává více variant, drž rozpočet, publikum, čas a umístění srovnatelné. Rozměry téhož banneru nebo videa pro různá umístění patří do jedné reklamy, pokud to zvolený formát v Metě podporuje.

## Příprava

1. Ověř název a ID reklamního účtu, měnu a časové pásmo. Při chybějícím připojení použij [meta-ads-setup](../meta-ads-setup/SKILL.md). Použij ověřené nástroje Meta Ads MCP nebo `cli-json` ze stejného skillu. Příkazy spouští agent.
2. Z briefu, dostupných podkladů a případné referenční kampaně zjisti cíl, cílovou URL, identitu FB stránky či IG účtu, text a soubor nebo ID média, publikum, rozpočet, měnu a dobu běhu. Pro konverzní cíl ověř také odpovídající datovou sadu a událost. Dotaž se pouze na chybějící rozhodnutí. Při kopírování použij jen nastavení, která odpovídají zadání testu.
3. Pro ukázku v kurzu můžeš navrhnout 200 Kč denně. Ulož částku zadanou nebo přijatou uživatelem. Rozpočet nastav na jedné úrovni, u běžného testu na kampani. Ukaž, zda je denní, nebo za celou dobu testu. Při více testech uveď i součet ve stejné měně a za stejné období.
4. Před vytvořením nebo duplikováním reklamy použij [meta-ads-utm](../meta-ads-utm/SKILL.md) na cílový odkaz a případnou zděděnou kreativu. Hodnotu `url_tags` připrav předem. Chybějící nebo neověřitelné UTM blokuje uložení reklamy k doručování i její spuštění.

## Založení v účtu

- Na požadavek na vytvoření založ kampaň, její jednu sadu, kreativu s připraveným `url_tags` a jednu reklamu navázanou na tuto sadu a kreativu. Kampaň, sadu i reklamu vytvoř se stavem `PAUSED`. U rozpracovaného testu nejdřív přečti jeho uložené objekty a pokračuj od prvního chybějícího kroku. Po nejasném výsledku zápisu ověř stav v Metě, než použiješ jinou cestu nebo pokus zopakuješ.
- Přečti zpět kampaň a její sady, potom reklamy dané sady. Ověř, že jde o správné vazby a počty **1 / 1 / 1**. Zkontroluj uložený rozpočet i typ, čas běhu, publikum a stavy. Na kreativě skutečně připojené k uložené reklamě ověř cílovou URL a `url_tags` podle UTM skillu.
- Pokud uživatel požádal i o spuštění, po ověření UTM aktivuj požadovanou reklamu a sadu v pozastavené kampani a kampaň zapni jako poslední. Znovu přečti ID, UTM a stav. Rozliš uložený stav `ACTIVE` od doručování, kontroly Metou nebo plánovaného startu.
- Vrať název a ID účtu, všech tří objektů, rozpočet, termín, stav a výsledek kontroly UTM. Při rozpracovaném testu uveď uložená ID a chybějící krok.

## Příkazy pro agenta

Se skutečnými hodnotami použij kategorie `campaign create`, `adset create --campaign-id`, `creative create --link-url --url-tags` a `ad create --adset-id --creative-id`. Doplň povinné parametry podle `--help` u každé kategorie. Pro doručování v EU přidej jméno příjemce výhod a plátce do údajů sady. Použij absolutní cestu k souboru. Rozpočet se předává v menších jednotkách měny účtu, například 200 Kč je `20000` v účtu s měnou CZK.

Ověření proveď pomocí `campaign get <ID>`, `adset list <ID_KAMPANĚ> --limit 2`, `adset get <ID>`, `ad list <ID_SADY> --limit 2` a `ad get <ID> --fields id,adset_id,status,effective_status,creative`. Použij `--fields` pro detaily, které výchozí výpis neobsahuje. U změny stavu použij příslušné `update --status ACTIVE`. [Struktura objektů v Marketing API](https://developers.facebook.com/docs/marketing-api/reference/v27.0/)
