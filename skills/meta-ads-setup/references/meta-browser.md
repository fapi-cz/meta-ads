# Nastavení přístupu v Metě

Použijte jeden reklamní účet z vlastního firemního portfolia. Ve Správci reklam ověřte jeho název a ID. K přiřazení aplikace a systémového uživatele pomůže správce portfolia, který má k těmto položkám přístup.

## 1. Vývojářský účet a aplikace

1. Pod svým Facebook profilem se zaregistrujte v Meta for Developers. Dokončete ověření, které Meta nabídne. [Registrace vývojáře](https://developers.facebook.com/documentation/development/register)
2. V **My Apps → Create App** založte aplikaci pod portfoliem firmy. Pro CLI vyberte použití **Create & manage ads with Marketing API**. Pro MCP přidejte **Create & manage ads with ads MCP server**. Pokud Meta nabídne obě použití spolu, použijte jednu aplikaci. Pokud druhé použití v dané aplikaci Meta nepovolí, založte samostatnou aplikaci ve stejném portfoliu. [Založení Meta aplikace](https://developers.facebook.com/documentation/development/create-an-app) · [Přístup k Meta Ads MCP](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-get-started)

## 2. Systémový uživatel

1. V **Meta Business Suite → Business Settings → Users → System Users** přidejte systémového uživatele s rolí **Employee**. Tato role funguje pro CLI a systémový token pro MCP ji vyžaduje.
2. V **Accounts → Apps → Assign Users** přiřaďte uživatele k aplikaci nebo oběma aplikacím.
3. Přiřaďte mu přes **Ad Accounts** vybraný účet s oprávněním ke správě kampaní. Pro tvorbu reklam mu přidělte i Facebook stránku, která bude u reklam vystupovat. [Přiřazení přístupů v Meta Business Suite](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/setup/get-started#authentication)

## 3. Token

V **System Users → Generate Token** vyberte aplikaci a požadovanou platnost. Pro CLI Meta uvádí <code>ads_management</code>, <code>business_management</code>, <code>pages_show_list</code>, <code>pages_read_engagement</code>, <code>pages_manage_ads</code> a <code>read_insights</code>. Pro MCP vyberte <code>ads_mcp_management</code> a <code>ads_management</code>. Vyberte sjednocená oprávnění u společné aplikace a samostatné sady při použití dvou aplikací. [Oprávnění CLI](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/setup/get-started#authentication) · [Oprávnění MCP](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-get-started#permissions)

Vložte token do místního formuláře, který poskytne agent. U společného tokenu stačí první pole. Generování a zobrazení tokenu provádějte mimo videozáznam.

## Když krok nefunguje

| Co vidíte | Co zkontrolovat |
| --- | --- |
| **System Users** nebo přidělení přístupu chybí | Jste ve správném firemním portfoliu a přihlášený člověk má oprávnění měnit jeho nastavení. |
| Aplikaci nelze vybrat v **Generate Token** | Aplikace patří správnému portfoliu a je přiřazená systémovému uživateli. |
| V dialogu chybí <code>ads_mcp_management</code> | Aplikace nabízí použití pro Ads MCP. Ověřte jeho nastavení a případné požadavky na schválení v dashboardu aplikace. |
| CLI načte účet a MCP vrací chybu | Ověřte token MCP, roli **Employee** a <code>ads_mcp_management</code>. Po uložení nového tokenu znovu načtěte server. |
| Účet se nezobrazuje ani v jednom výpisu | Porovnejte ID s tím ve Správci reklam a ověřte přiřazení reklamního účtu. Zkontrolujte platnost tokenu a správnou aplikaci. |
