# Knihovna Meta Ads pro Codex a Claude Code

Knihovna propojí reklamní účet s oficiálním Meta Ads CLI a s Ads MCP tam, kde ho Meta pro účet zpřístupnila. Přidává skilly pro reklamy na webináře, testovací reklamy, správu UTM a vyhodnocení kampaní. Použijte místní Codex nebo Claude Code na macOS, Linuxu nebo Windows. Ve Windows spouští klient instalaci, připojení a kontroly přes WSL. [Postup pro každý systém](skills/meta-ads-setup/references/platforms.md)

## Start ze staženého repozitáře

1. Na GitHubu zvolte **Code → Download ZIP** a složku rozbalte.
2. V Codexu nebo Claude Code otevřete rozbalenou složku jako místní projekt. Pokud se aplikace zeptá na důvěru k projektu, potvrďte ji podle názvu a umístění složky.
3. Napište **Pomoz mi vytvořit propojení s Meta Ads.** Agent připraví místní připojení a pošle zbývající kroky v Metě s přímými odkazy. Celé nastavení můžete projít na jeden zátah i podle návodu. [Odkazy a postup v Metě](skills/meta-ads-setup/references/meta-browser.md) · [Ruční propojení v Terminálu](skills/meta-ads-setup/references/platforms.md#připojení-v-terminálu)

Pro používání ve všech místních projektech lze zkopírovat složky ze `skills/` do `~/.agents/skills/` v Codexu nebo `~/.claude/skills/` v Claude Code. Spusťte novou místní konverzaci a použijte stejnou větu. Podporovaný je i import přímo z GitHubu podle kroků níže. [Složky Codex skillů](https://learn.chatgpt.com/docs/build-skills) · [Složky Claude Code skillů](https://code.claude.com/docs/en/skills)

## Co skilly umí

| Skill | Co napsat agentovi |
| --- | --- |
| [Připojení Meta Ads](skills/meta-ads-setup/SKILL.md) | **Pomoz mi vytvořit propojení s Meta Ads.** |
| [Reklama na webinář](skills/meta-ads-webinar/SKILL.md) | **Založ mi pozastavenou reklamu na další webinář podle kampaně s ID … Použij přiložené bannery, video a okamžitý formulář. Rozpočet je celkem 3 500 Kč na 14 dní.** |
| [Testovací reklama](skills/meta-ads-test/SKILL.md) | **Založ mi pozastavený test. Použij přiložené podklady, odkaz a text. Rozpočet je 200 Kč denně.** |
| [Kontrola a oprava UTM](skills/meta-ads-utm/SKILL.md) | **Zkontroluj, jestli má reklama s ID … správně nastavené UTM.** Pro potvrzenou opravu napište **Oprav UTM u této reklamy.** |
| [Vyhodnocení kampaní](skills/meta-ads-evaluate/SKILL.md) | **Vyhodnoť tyto testy za posledních 7 celých dní. Porovnej útratu, počet leadů a cenu za lead.** |

Každý test má **jednu kampaň, jednu sadu a jednu reklamu**. Výchozí rozpočet v účtu s měnou CZK je **200 Kč denně na test**. Připravte cílovou stránku, podklady k reklamě, publikum a plán testu. Případný jiný rozpočet uveďte v zadání. Agent před spuštěním ověří UTM na uložené reklamě. U kampaně měřené ve FAPI mu doplňte také kód kampaně pro `ref_code`.

## Codex Desktop

1. Otevřete Codex v desktopové aplikaci a zvolte místní práci na vašem počítači.
2. Do chatu vložte tento text.

   > $skill-installer Nainstaluj mi skilly z https://github.com/fapi-cz/meta-ads. Použij cesty skills/meta-ads-setup, skills/meta-ads-webinar, skills/meta-ads-test, skills/meta-ads-utm a skills/meta-ads-evaluate. Pokud už tyto skilly mám, stáhni aktuální verzi do dočasné složky a aktualizuj instalované kopie. Zachovej moje připojení k Metě.

3. V novém místním chatu napište **Pomoz mi vytvořit propojení s Meta Ads.**

[Skilly v Codexu](https://learn.chatgpt.com/docs/build-skills)

## Claude Code v desktopové aplikaci

1. Otevřete **Customize → Plugins → Add → Add marketplace → Add from a repository** a vložte adresu repozitáře. [fapi-cz/meta-ads](https://github.com/fapi-cz/meta-ads)
2. Ze zdroje **fapi-ads** nainstalujte **fapi-meta-ads**. Otevřete kartu **Code** a spusťte místní relaci.
3. Napište **Pomoz mi vytvořit propojení s Meta Ads.**

U již nainstalovaného pluginu obnovte zdroj **fapi-ads**, aktualizujte **Meta Ads** a otevřete novou místní relaci.

[Přidání zdroje pluginů v Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) · [Místní relace Claude Code](https://code.claude.com/docs/en/desktop)

## Co si připravit

- **Reklamní účet a přístup ke kampaním.** ID najdete ve Správci reklam u názvu účtu. Pokud nastavení firemního portfolia spravuje kolega, může vám pomoct s vytvořením aplikace a přiřazením přístupů.
- **Token vložte do skryté výzvy v místním Terminálu.** Výzvu si připravte před vygenerováním tokenu. Na Macu ji může otevřít agent. Token se uloží do Klíčenky na macOS nebo do soukromého souboru na Linuxu a ve WSL. Do chatu stačí potvrzení uložení.
- **Pokud se některý krok v Metě nedaří, napište agentovi název dialogu nebo text chyby.** Postup a řešení jsou v knihovně. [Nastavení přístupu v Metě](skills/meta-ads-setup/references/meta-browser.md)

Agent ověří CLI a MCP samostatně. Pokud Meta účtu ještě nezpřístupnila MCP, stačí ověřené CLI. K pozdější kontrole napište **Ověř mi připojení k Meta Ads.** Pro výměnu přístupu napište **Vyměň Meta Ads MCP token.** [Dostupnost Ads MCP](https://en-gb.facebook.com/business/tools/ads-mcp-server)
