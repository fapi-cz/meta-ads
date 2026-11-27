# Meta Ads v Codexu a Claude Code

Účastník kurzu nastaví přístupy ve svém účtu Meta. Agent nainstaluje oficiální Meta Ads CLI, připojí Meta Ads MCP a ověří reklamní účet oběma cestami. Průvodce běží v místní relaci Codexu nebo Claude Code na macOS nebo Linuxu. Na Windows potřebuje místní relaci ve WSL.

## Co skilly umí

| Skill | Co napsat agentovi |
| --- | --- |
| [Připojení Meta Ads](skills/meta-ads-setup/SKILL.md) | **Nastav mi Meta Ads podle kurzu FAPI.** |
| [Testovací reklama](skills/meta-ads-test/SKILL.md) | **Založ mi pozastavený test podle kurzu FAPI. Použij přiložené video, odkaz a text. Rozpočet je 200 Kč denně.** |
| [Kontrola a oprava UTM](skills/meta-ads-utm/SKILL.md) | **Zkontroluj, jestli má reklama s ID … správně nastavené UTM.** Pro potvrzenou opravu napište **Oprav UTM u této reklamy.** |

Každý test má **jednu kampaň, jednu sadu a jednu reklamu**. Připravte cílovou stránku, podklady k reklamě, publikum, rozpočet a plán testu. Agent před spuštěním ověří UTM na uložené reklamě. U kampaně měřené ve FAPI mu doplňte také kód kampaně pro `ref_code`.

## Codex Desktop

1. Otevřete Codex v desktopové aplikaci a zvolte místní práci na vašem počítači.
2. Do chatu vložte tento text.

   > $skill-installer Nainstaluj mi skilly z https://github.com/fapi-cz/meta-ads-course-skills. Použij cesty skills/meta-ads-setup, skills/meta-ads-test a skills/meta-ads-utm. Pokud už mám starší kurzový skill z tohoto repozitáře, stáhni aktuální verzi do dočasné složky a aktualizuj tuhle instalovanou kopii. Zachovej moje připojení k Metě.

3. V novém místním chatu napište **Nastav mi Meta Ads podle kurzu FAPI.** Codex vás provede vytvořením přístupu v Metě, nabídne místní formulář pro token a ověří spojení.

[Skilly v Codexu](https://learn.chatgpt.com/docs/build-skills)

## Claude Code v desktopové aplikaci

1. Otevřete **Customize → Plugins → Add → Add marketplace → Add from a repository** a vložte adresu [repozitáře](https://github.com/fapi-cz/meta-ads-course-skills).
2. Nainstalujte **fapi-meta-ads-course**. Otevřete kartu **Code** a spusťte místní relaci.
3. Napište **Nastav mi Meta Ads podle kurzu FAPI.**

Pokud už máte plugin nainstalovaný, obnovte jeho zdroj **fapi-kurzy** a aktualizujte plugin v **Customize → Plugins**.

[Přidání zdroje pluginů v Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) · [Místní relace Claude Code](https://code.claude.com/docs/en/desktop)

## Co si připravit

- **Reklamní účet a přístup ke kampaním.** ID najdete ve Správci reklam u názvu účtu. Pokud nastavení firemního portfolia spravuje kolega, může vám pomoct s vytvořením aplikace a přiřazením přístupů.
- **Token zadávejte do formuláře, který vám agent otevře na vašem počítači.** Jeho adresa začíná na <code>http://127.0.0.1:</code>. Hodnotu vložte do pole typu heslo. Formulář uloží přístup do soukromé uživatelské složky mimo repozitář.
- **Když Meta nenabízí krok nebo oprávnění, napište agentovi jeho název nebo text chyby.** Stačí třeba „V Generovat token nevidím ads_mcp_management.“ Agent postupuje podle ověřených [kroků v Metě](skills/meta-ads-setup/references/meta-browser.md).

Na konci agent ukáže název a ID účtu, který načetl zvlášť přes CLI a přes MCP. Když spojení později přestane fungovat, napište **Ověř mi připojení k Meta Ads.** Při výměně tokenu použijte **Otevři formulář pro výměnu Meta Ads tokenu.**
