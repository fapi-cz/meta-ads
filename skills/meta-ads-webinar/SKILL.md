---
name: meta-ads-webinar
description: Připrav a založ pozastavenou Meta reklamu na webinář podle briefu nebo předchozí kampaně. Použij okamžitý formulář ve Facebooku se SmartEmailingem nebo registraci na webu. Zpracuj bannery a videa pro umístění, nastav rozpočet a ověř uložené reklamy.
---

# Meta reklama na webinář

Cílem je registrace na konkrétní webinář. Podle potvrzeného zadání založ jednu kampaň, jednu sadu a jednu reklamu na každou schválenou kreativu. Výsledkem je pozastavená kampaň připravená ke kontrole náhledů a registrace. Pro samostatný test jedné varianty využij strukturu a výchozí rozpočet z [meta-ads-test](../meta-ads-test/SKILL.md).

## Připrav zadání

1. Ověř účet, Facebook stránku a případný IG účet. Při chybějícím přístupu otevři [meta-ads-setup](../meta-ads-setup/SKILL.md). Čti a zapisuj přednostně přes oficiální Meta Ads CLI s `cli-json`. Meta Ads MCP využij pro kroky, které CLI neumí. Skripty spouštěj přes `meta-ads.sh python`. [Postup pro daný systém](../meta-ads-setup/references/platforms.md)
2. Z podkladů zjisti téma a termín webináře, texty a CTA, soubory, schválené publikum a umístění, částku, typ rozpočtu, start a konec v časovém pásmu účtu. Před tvorbou rozhodni, zda se lidé registrují **v okamžitém formuláři v Metě**, nebo **na vlastní stránce**. U nového briefu se doptávej jen na údaje, které ještě chybí nebo se rozcházejí.
3. Při zadání „podle minulé kampaně“ načti účet a přesnou referenci, jednu odpovídající sadu a reklamy s kreativami. Navrhni převzetí stránky, schváleného cílení, umístění a struktury copy. Pro nový webinář dosaď nový termín, rozpočet, texty, média a správný formulář či URL. Ověř, která vyloučení z referenční sady mají platit i nyní. Oslovení vlastní databáze řeš jako samostatnou e-mailovou aktivitu.

## Podklady, umístění a hudba

- Počítej s několika kreativami, například dvěma bannery a jedním videem. Různé poměry téhož podkladu připoj k jedné reklamě, pokud to zvolený formát podporuje. Ověř požadavky na konkrétní umístění v Meta Ads Guide. Pro Feed se běžně připravuje export 4:5 a pro Stories či Reels 9:16. Pokud má účastník šablonu v Canvě, použij její kopii nebo vyžádej hotové exporty. [Meta Ads Guide](https://www.facebook.com/business/ads-guide)
- Na místních exportech použij `scripts/check_media.py --asset 4:5 /cesta/feed.png --asset 9:16 /cesta/stories.mp4`, pokud je dostupný `ffprobe`. Skript ověří skutečný poměr stran a přítomnost zvukové stopy. U každého aktivního umístění pak použij skutečný náhled a zkontroluj ořez textu, viditelnost CTA a zvuk. [Náhledy reklam](https://developers.facebook.com/docs/marketing-api/generatepreview/v8.0/)
- Pro video použij schválenou zvukovou stopu. Zamýšlenou hudbu z knihovny Mety ověř v náhledu pro konkrétní umístění. Pokud ji daný nástroj neumí nastavit, označ ji jako krok k výběru ve Správci reklam.

## Registrace a uložení

- **Okamžitý formulář.** Použij schválený formulář na téže Facebook stránce. Zkontroluj, že je určený pro aktuální webinář a že zobrazuje správná pole, odkaz na zásady ochrany údajů a závěrečnou obrazovku. Pokud je potřeba nový formulář a konkrétní nástroj tvorbu umí, vyžádej si schválená pole a texty. Jinak účastníka naveď v Metě do **Okamžitých formulářů** a použij ID, které tam po založení získá. Pro SmartEmailing ověř přiřazení tohoto konkrétního formuláře k odpovídajícímu seznamu nebo automatizaci. Se souhlasem použij testovací registraci a ověř doručení potvrzovacího e-mailu.
- **Registrace na webu.** Použij adresu aktuálního webináře, `WEBSITE` a schválenou událost registrace nebo platby. Připrav a zpětně ověř UTM podle [meta-ads-utm](../meta-ads-utm/SKILL.md). U okamžitého formuláře patří registrace k ID formuláře a reklamy v Metě. Případný závěrečný proklik z formuláře na web ověř se skutečnými UTM samostatně.
- Převeď potvrzený rozpočet skriptem [test_ads.py](../meta-ads-test/scripts/test_ads.py) s příkazem `budget`. Pro ukázkovou částku 3 500 Kč celkem na 14 dní použij `--currency CZK --type lifetime --amount 3500`. Kampaň, sadu i reklamy vytvoř jako `PAUSED`. Při nejasném výsledku zápisu nejdřív načti uložený stav. [Pole, payloady a náhledy](references/meta-cli.md)
- Přečti uložené objekty skriptem `scripts/check_webinar.py` s očekávanými ID a rozpočtem, začátkem a koncem v ISO 8601. Pro web použij `--web-url` s ověřenou adresou z přípravy kreativy a u měření ve FAPI `--ref-code KOD`. Pro okamžitý formulář použij `--form-id ID --page-id ID`. Uveď, co je uložené v Metě, které náhledy byly zkontrolované a zda byla ověřena i registrace a potvrzení.
