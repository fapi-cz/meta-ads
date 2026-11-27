---
name: meta-ads-setup
description: Pomoz mi vytvořit propojení s Meta Ads. Proveď účastníka kurzu FAPI připojením reklamního účtu v Codexu nebo Claude Code, nejdřív přes oficiální Meta Ads MCP a potom přes oficiální CLI. Sprav také kontrolu připojení a výměnu tokenů.
---

# Propojení s Meta Ads

Začni v jazyce účastníka. Na větu **„Pomoz mi vytvořit propojení s Meta Ads“** nejdřív stručně vypiš, co bude potřeba.

- Místní relace Codexu nebo Claude Code na macOS či Linuxu, na Windows v relaci vedené ve WSL.
- Přihlášení do Meta for Developers, přístup správce k firemnímu portfoliu nebo pomoc jeho správce, reklamní účet a jeho ID.
- Pro MCP aplikace s použitím **Create & manage ads with ads MCP server**, systémový uživatel s přístupem k účtu a token. Pro CLI se poté použije stejný token se správnými oprávněními nebo druhý token.

Otevři [návod pro Meta](references/meta-browser.md) a začni prvním chybějícím krokem. Tokeny zadává účastník ve formuláři na `127.0.0.1`. Příkazy spouští agent ze skutečné absolutní cesty `scripts/course-ads.sh` přes Bash. Pokud aplikace požádá o schválení místní instalace nebo přístupu k síti, pojmenuj konkrétní operaci.

## 1. Meta Ads MCP

1. Spusť `install-mcp` a zjisti stav pomocí `status`. Pokud schází token, proveď účastníka Meta kroky pro MCP a spusť `connect-mcp` na pozadí. Pošli mu přesný odkaz vypsaný skriptem. Do místního formuláře vloží ID účtu a token MCP. Po uložení přístupu na něj navaž.
2. Připoj místní server `fapi-course-meta-ads` v daném klientovi.
   - V Codexu spusť `codex mcp add fapi-course-meta-ads -- bash /absolutní/cesta/course-ads.sh mcp`. Pro macOS desktop použij také známou cestu `/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex`. Při chybějícím příkazu ukaž hodnoty do polí **Settings → MCP servers → Add server → STDIO**.
   - V Claude Code server načte kurzový plugin nebo soubor `.mcp.json` z otevřeného kurzového repozitáře. U samostatně zkopírovaných skillů může agent server připojit pomocí `claude mcp add --scope user fapi-course-meta-ads -- bash /absolutní/cesta/course-ads.sh mcp`. Pokud aplikace žádá o povolení projektového serveru, účastník jej potvrdí v aplikaci.
3. `install-cli` nejprve samo zavolá přes MCP `ads_get_ad_accounts` a zkontroluje vybraný účet. Pokračuj podle výsledku skriptu. Chybu MCP řeš podle [nápovědy](references/meta-browser.md#když-krok-nefunguje) a příkaz zopakuj až po opravě. Při obnovení klienta lze v novém chatu pokračovat stejnou úvodní větou. Pokud registrace vyžaduje novou relaci, řekni účastníkovi, kde server po otevření relace uvidí.

## 2. Meta Ads CLI

1. Po kladném ověření MCP `install-cli` nainstaluje oficiální CLI. Spusť `check-cli`. Skript ověří stejné ID účtu a načte výpis kampaní. K prázdnému účtu stačí úspěšný prázdný výpis.
2. Pokud společný token pro CLI nestačí, projdi [kroky pro CLI](references/meta-browser.md#2-přístup-pro-cli). Spusť `connect-cli` a dej účastníkovi jeho adresu. Po uložení tokenu spusť znovu `check-cli`.
3. Uveď ID účtu a výsledek pro každou cestu podle výstupu skriptů. Dostupnost nástrojů přímo v klientovi uveď podle toho, co ukázala aktuální relace.

## Další práce

- Při žádosti o ověření přístupu spusť `check-mcp` a poté `check-cli`. Při výměně tokenu obnov příslušný místní formulář, znovu ověř přístup a případně obnov relaci s MCP serverem.
- K práci s Meta Ads používej připojené MCP nástroje nebo `cli-json` pro oficiální CLI. Vybraný účet je uložený ve formuláři. Do MCP operací vyžadujících účet předej toto ID. Při zápisu s nejasným výsledkem ověř uložený stav před dalším pokusem.
- Použij [meta-ads-test](../meta-ads-test/SKILL.md) pro vytvoření testu, [meta-ads-utm](../meta-ads-utm/SKILL.md) při práci s kreativitou a před zapnutím reklam s webovým odkazem a [meta-ads-evaluate](../meta-ads-evaluate/SKILL.md) pro vyhodnocení.
