---
name: meta-ads-setup
description: Připoj reklamní účet Meta Ads v Codexu nebo Claude Code přes oficiální MCP a CLI. Proveď založením aplikace a systémového uživatele, ověř přístup nebo pomoz vyměnit token.
---

# Propojení Meta Ads

Pracuj v místní relaci a otevři [postup pro daný systém](references/platforms.md). Podle `status` využij uložený token a zjisti, které nástroje jsou nainstalované. Na podporovaném systému doinstaluj chybějící CLI příkazem `install-cli`. Pro přístup přes MCP připrav `install-mcp`. Každý instalátor si v případě potřeby vytvoří místní prostředí.

## Připoj účet

1. Pro nové připojení otevři [nastavení v Metě](references/meta-browser.md) a dej uživateli všechny zbývající kroky s přímými odkazy v jednom seznamu. Zahrň aplikaci, systémového uživatele s rolí **Employee**, přiřazení účtu a případně stránky, vygenerování tokenu a nalezení ID účtu. Pokud se ptá jen na první krok, dej první chybějící krok a odkaz na celý návod.
2. Pokud token chybí nebo ho měníš, připrav skryté zadání před jeho vytvořením. Na Macu můžeš otevřít Terminál příkazem `open-connect-mcp`. Pro ruční spuštění dej přesný příkaz `connect-mcp` s absolutní cestou podle [platformy](references/platforms.md). Uživatel zadá ID a vloží celý token do výzvy. V chatu stačí potvrzení uložení.
3. S uloženým tokenem spusť `check-cli` a `check-mcp` samostatně pro nainstalované nástroje. CLI ověří vybraný účet a výpis kampaní. Prázdný výpis nového účtu stačí. Při odmítnutí přístupu postupuj podle [řešení potíží](references/meta-browser.md#když-krok-nefunguje). Samostatný token CLI připrav jen tehdy, pokud společný token nemůže získat potřebná oprávnění.
4. Po úspěšném `check-mcp` použij funkční registraci nebo přidej STDIO server `fapi-meta-ads` podle [platformy](references/platforms.md). Pokud Meta pro účet ještě nezpřístupnila Ads MCP, pokračuj ověřeným CLI. Uveď ověřené ID, použitelné připojení a případný krok potřebný k obnovení MCP v klientovi.

## Kontrola, výměna a další práce

- Pokud uživatel používá vlastní spojení přes OAuth, ověř MCP nástrojem `ads_get_ad_accounts` přímo v klientovi. Při výměně otevři odpovídající výzvu `connect-mcp` nebo `connect-cli` a ověř nový přístup. ID uloženého účtu lze potvrdit Enterem. Pokud klient používá původní token, obnov jeho relaci.
- Pro práci s reklamami používej Meta Ads MCP nebo oficiální CLI přes `cli-json`. ID vybraného účtu převezmi ze `status`. Při zápisu s nejasným výsledkem ověř uložený stav před dalším pokusem.
- Pro reklamy použij [meta-ads-test](../meta-ads-test/SKILL.md), pro UTM [meta-ads-utm](../meta-ads-utm/SKILL.md) a pro výkonnost [meta-ads-evaluate](../meta-ads-evaluate/SKILL.md).
