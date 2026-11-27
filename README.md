# Meta Ads v Codexu a Claude Code

Účastník kurzu nastaví přístupy ve svém účtu Meta. Agent nejdřív připojí a ověří Meta Ads MCP, potom nainstaluje a ověří oficiální Meta Ads CLI. Průvodce běží v místní relaci Codexu nebo Claude Code na macOS nebo Linuxu. Na Windows potřebuje místní relaci ve WSL.

## Start ze staženého repozitáře

1. Na GitHubu zvolte **Code → Download ZIP** a složku rozbalte.
2. V Codexu nebo Claude Code otevřete rozbalenou složku jako místní projekt. Pokud se aplikace zeptá na důvěru k projektu, potvrďte ji podle názvu a umístění složky.
3. Napište **Pomoz mi vytvořit propojení s Meta Ads.** Agent vypíše přístupy, které budete potřebovat, a provede vás prvním krokem.

Pro používání ve všech místních projektech lze zkopírovat všechny čtyři složky ze `skills/` do `~/.agents/skills/` v Codexu nebo `~/.claude/skills/` v Claude Code. Spusťte novou místní konverzaci a použijte stejnou větu. Podporovaný je i import přímo z GitHubu podle kroků níže. [Složky Codex skillů](https://learn.chatgpt.com/docs/build-skills) · [Složky Claude Code skillů](https://code.claude.com/docs/en/skills)

## Co skilly umí

| Skill | Co napsat agentovi |
| --- | --- |
| [Připojení Meta Ads](skills/meta-ads-setup/SKILL.md) | **Pomoz mi vytvořit propojení s Meta Ads.** |
| [Testovací reklama](skills/meta-ads-test/SKILL.md) | **Založ mi pozastavený test podle kurzu FAPI. Použij přiložené video, odkaz a text. Rozpočet je 200 Kč denně.** |
| [Kontrola a oprava UTM](skills/meta-ads-utm/SKILL.md) | **Zkontroluj, jestli má reklama s ID … správně nastavené UTM.** Pro potvrzenou opravu napište **Oprav UTM u této reklamy.** |
| [Vyhodnocení kampaní](skills/meta-ads-evaluate/SKILL.md) | **Vyhodnoť tyto testy za posledních 7 celých dní. Porovnej útratu, počet leadů a cenu za lead.** |

Každý test má **jednu kampaň, jednu sadu a jednu reklamu**. Výchozí rozpočet v účtu s měnou CZK je **200 Kč denně na test**. Připravte cílovou stránku, podklady k reklamě, publikum a plán testu. Případný jiný rozpočet uveďte v zadání. Agent před spuštěním ověří UTM na uložené reklamě. U kampaně měřené ve FAPI mu doplňte také kód kampaně pro `ref_code`.

## Codex Desktop

1. Otevřete Codex v desktopové aplikaci a zvolte místní práci na vašem počítači.
2. Do chatu vložte tento text.

   > $skill-installer Nainstaluj mi skilly z https://github.com/fapi-cz/meta-ads-course-skills. Použij cesty skills/meta-ads-setup, skills/meta-ads-test, skills/meta-ads-utm a skills/meta-ads-evaluate. Pokud už mám starší kurzové skilly z tohoto repozitáře, stáhni aktuální verzi do dočasné složky a aktualizuj tyto instalované kopie. Zachovej moje připojení k Metě.

3. V novém místním chatu napište **Pomoz mi vytvořit propojení s Meta Ads.** Codex vypíše potřebné přístupy a nabídne místní formulář pro token k MCP. Po ověření MCP přejde k CLI.

[Skilly v Codexu](https://learn.chatgpt.com/docs/build-skills)

## Claude Code v desktopové aplikaci

1. Otevřete **Customize → Plugins → Add → Add marketplace → Add from a repository** a vložte adresu [repozitáře](https://github.com/fapi-cz/meta-ads-course-skills).
2. Nainstalujte **fapi-meta-ads-course**. Otevřete kartu **Code** a spusťte místní relaci.
3. Napište **Pomoz mi vytvořit propojení s Meta Ads.**

Pokud už máte plugin nainstalovaný, obnovte jeho zdroj **fapi-kurzy**, aktualizujte plugin v **Customize → Plugins** a otevřete novou místní relaci.

[Přidání zdroje pluginů v Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) · [Místní relace Claude Code](https://code.claude.com/docs/en/desktop)

## Co si připravit

- **Reklamní účet a přístup ke kampaním.** ID najdete ve Správci reklam u názvu účtu. Pokud nastavení firemního portfolia spravuje kolega, může vám pomoct s vytvořením aplikace a přiřazením přístupů.
- **Token zadávejte do formuláře, který vám agent otevře na vašem počítači.** Jeho adresa začíná na <code>http://127.0.0.1:</code>. Hodnotu vložte do pole typu heslo. Formulář uloží přístup do soukromé uživatelské složky mimo repozitář.
- **Když Meta nenabízí krok nebo oprávnění, napište agentovi jeho název nebo text chyby.** Stačí třeba „V Generovat token nevidím ads_mcp_management.“ Agent postupuje podle ověřených [kroků v Metě](skills/meta-ads-setup/references/meta-browser.md).

Na konci agent ukáže ID účtu a výsledek obou kontrol ze skriptů. Když spojení později přestane fungovat, napište **Ověř mi připojení k Meta Ads.** Při výměně napište např. **Otevři formulář pro výměnu Meta Ads MCP tokenu.**
