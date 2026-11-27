---
name: meta-ads-setup
description: Připoj reklamní účet Meta Ads v Codexu nebo Claude Code přes oficiální MCP a CLI. Proveď založením aplikace a systémového uživatele, ověř přístup nebo pomoz vyměnit token.
---

# Propojení Meta Ads

Pracuj v místní relaci na macOS, Linuxu nebo Windows. Pro příkazy a registraci MCP použij [přesný postup pro daný systém](references/platforms.md). Otevři [nastavení v Metě](references/meta-browser.md). Pomocí `status` zjisti, zda už je místně uložený token. Pokud ano, pokračuj ověřením. Při novém připojení přijmi už potvrzené nastavení a začni prvním chybějícím krokem. Při výslovné žádosti o celý návod vypiš postup bodově.

## Nastav přístup ve třech krocích

V každé etapě pošli uživateli do chatu přímý klikací odkaz do Mety a krátký bodový postup z odpovídající části reference.

1. **Aplikace.** V první odpovědi pošli odkaz na [registraci vývojáře](references/meta-browser.md#registrace-vývojáře) a přímé odkazy pro [vytvoření a nastavení aplikace](references/meta-browser.md#založení-aplikace). Když už je vývojářský účet připravený, začni rovnou aplikací. Navrhni název podle firmy a uveď kontaktní e-mail, přesné použití a správné portfolio. Vyčkej na potvrzení aplikace a jejího nastavení.
2. **Systémový uživatel.** Po potvrzení aplikace pošli odkaz do nastavení systémových uživatelů a kroky pro [uživatele s rolí Employee](references/meta-browser.md#systémový-uživatel). Vyčkej na potvrzení, že má přiřazenou aplikaci a vybraný reklamní účet. Pro tvorbu reklam ověř i přiřazení Facebook stránky.
3. **Token.** Po potvrzení obou kroků pošli odkaz do nastavení [systémových uživatelů](references/meta-browser.md#token-pro-mcp), kde se volí **Generate Token**, a odkaz do Správce reklam pro ID účtu. Spusť `install-mcp` a dej uživateli přesný příkaz `connect-mcp` pro jeho [místní terminál](references/platforms.md). Zadá ID účtu a vloží token do skryté výzvy. Na macOS ho uloží Klíčenka, na Linuxu a ve WSL soukromý soubor mimo repozitář. Do chatu stačí potvrzení uložení. Potom spusť `status` a navaž ověřením.

Pro běžné nastavení použij kroky a názvy voleb uvedené v referenci. Při zádrhelu zjisti, u kterého kroku je uživatel a jakou hlášku vidí. Navazuj podle [řešení potíží](references/meta-browser.md#když-krok-nefunguje). Příkazy kromě zadání tokenu spouští agent.

## Připoj Meta Ads MCP

Meta podporuje OAuth i token systémového uživatele. Knihovna používá systémového uživatele pro opakovaný přístup k vybranému účtu. Stejný typ tokenu podporuje také CLI. [Ověřování v Meta Ads MCP](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-get-started#authentication)

1. Spusť `check-mcp`. Příkaz zavolá oficiální server na `https://mcp.facebook.com/ads` a přes `ads_get_ad_accounts` ověří vybrané ID účtu. Při chybě postupuj podle [nápovědy](references/meta-browser.md#když-krok-nefunguje).
2. V klientovi použij funkční připojení k této knihovně nebo zaregistruj místní STDIO server `fapi-meta-ads` podle [příkazů pro Codex a Claude Code](references/platforms.md).
3. Zkontroluj dostupnost Meta Ads nástrojů v klientovi. Pokud se načtou až po obnovení, uveď cestu **Settings → MCP servers** a příkaz `/mcp` pro kontrolu v nové místní relaci Codexu.

## Ověř oficiální Meta Ads CLI

1. Po ověření MCP spusť `install-cli` a `check-cli`. Kontrola ověří stejné ID účtu a výpis kampaní. Úspěšný prázdný výpis u nového účtu stačí.
2. Pokud společný token nestačí, dej postup pro [samostatný token CLI](references/meta-browser.md#token-pro-cli) a přesný příkaz `connect-cli` pro místní terminál. Po potvrzení zopakuj `check-cli`.
3. Uveď ověřené ID účtu, výsledek MCP a CLI a dostupnost MCP nástrojů v aktuálním klientovi.

## Kontrola, výměna a další práce

- Při ověření přístupu spusť `check-mcp` a `check-cli`. Pokud uživatel používá vlastní spojení přes OAuth, ověř MCP nástrojem `ads_get_ad_accounts` přímo v klientovi. Při výměně dej odpovídající příkaz `connect-mcp` nebo `connect-cli` pro Terminál a ověř nový přístup. Pokud klient používá původní token, obnov jeho relaci.
- Pro práci s reklamami používej Meta Ads MCP nebo oficiální CLI přes `cli-json`. ID vybraného účtu převezmi ze `status`. Při zápisu s nejasným výsledkem ověř uložený stav před dalším pokusem.
- Pro reklamy použij [meta-ads-test](../meta-ads-test/SKILL.md), pro UTM [meta-ads-utm](../meta-ads-utm/SKILL.md) a pro výkonnost [meta-ads-evaluate](../meta-ads-evaluate/SKILL.md).
