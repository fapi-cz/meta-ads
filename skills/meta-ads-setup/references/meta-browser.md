# Nastavení přístupu v Metě

Použijte jeden reklamní účet z vlastního firemního portfolia. Ve Správci reklam ověřte jeho název a ID. K přiřazení aplikace a systémového uživatele pomůže správce portfolia, který má k těmto položkám přístup.

## 1. Přístup pro MCP

1. Pod svým Facebook profilem se zaregistrujte v Meta for Developers. Dokončete ověření, které Meta nabídne. [Registrace vývojáře](https://developers.facebook.com/documentation/development/register)
2. V **My Apps → Create App** založte nebo otevřete aplikaci pod portfoliem firmy. Přidejte použití **Create & manage ads with ads MCP server**. [Založení Meta aplikace](https://developers.facebook.com/documentation/development/create-an-app) · [Přístup k Meta Ads MCP](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-get-started)
3. V **Meta Business Suite → Business Settings → Users → System Users** vytvořte systémového uživatele s rolí **Employee**. V **Accounts → Apps → Assign Users** ho přiřaďte k aplikaci. Přes **Ad Accounts** mu přidělte vybraný reklamní účet a právo spravovat jeho kampaně. Pro tvorbu reklam mu přiřaďte i používanou Facebook stránku.
4. V **System Users → Generate Token** vyberte aplikaci a platnost. Pro MCP vyberte `ads_mcp_management` a `ads_management`. Token a ID účtu vložte do místního formuláře pro MCP, který připraví agent. Generování a uložení tokenu dělejte mimo videozáznam. [Oprávnění MCP](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-get-started#permissions)

## 2. Přístup pro CLI

Agent pokračuje po ověření MCP. Pokud uložený token umožní i čtení přes CLI, použije ho pro obě cesty. Pro samostatný token přidejte v aplikaci použití **Create & manage ads with Marketing API**. Pokud Meta u stávající aplikace tuto kombinaci nenabídne, založte druhou ve stejném portfoliu a přiřaďte jí systémového uživatele.

V **System Users → Generate Token** vyberte aplikaci pro Marketing API. Meta pro CLI uvádí `ads_management`, `business_management`, `pages_show_list`, `pages_read_engagement`, `pages_manage_ads` a `read_insights`. Vložte token do místního formuláře pro CLI. Agent použije ID účtu nastavené v prvním kroku. [Přístupy a oprávnění CLI](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/setup/get-started#authentication)

## Když krok nefunguje

| Co vidíte | Co zkontrolovat |
| --- | --- |
| **System Users** nebo přidělení přístupu chybí | Jste ve správném firemním portfoliu a přihlášený člověk má oprávnění měnit jeho nastavení. |
| Aplikaci nelze vybrat v **Generate Token** | Aplikace patří správnému portfoliu a je přiřazená systémovému uživateli. |
| V dialogu chybí <code>ads_mcp_management</code> | Aplikace nabízí použití pro Ads MCP. Ověřte jeho nastavení a případné požadavky na schválení v dashboardu aplikace. |
| MCP nenajde vybraný účet | Porovnejte jeho ID s tím ve Správci reklam. Ověřte přiřazení účtu a dostupnost MCP pro vybraný účet. |
| MCP funguje a CLI hlásí chybu přístupu | Ověřte použití pro Marketing API a oprávnění jeho tokenu. Po výměně tokenu nechte agenta opakovat kontrolu. |
