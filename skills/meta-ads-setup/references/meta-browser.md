# Nastavení přístupu v Metě

Použijte firemní portfolio, které vlastní nebo spravuje zamýšlený reklamní účet. K přiřazení aplikace a systémového uživatele potřebujete přístup správce portfolia nebo jeho pomoc.

## Registrace vývojáře

1. Přihlaste se svým stávajícím Facebook profilem a v Meta for Developers klikněte na **Get Started**. [Registrace](https://developers.facebook.com/async/registration)
2. Potvrďte podmínky a pravidla pro vývojáře. Ověřte telefon a e-mail podle výzev Mety.
3. Vyberte nejbližší povolání nebo roli a dokončete registraci. Výsledek ověřte v **My Apps**. [Postup registrace](https://developers.facebook.com/documentation/development/register)

## Založení aplikace

1. V **My Apps → Create App** zadejte například **Správa reklam MojeFirma** a firemní kontaktní e-mail. Pro jméno použijte svůj firemní název a účel aplikace. [Vytvořit aplikaci](https://developers.facebook.com/apps/creation/) · [Pravidla názvů](https://developers.facebook.com/docs/app-review/resources/logos/)
2. V **Use cases** zvolte **Create & manage ads with ads MCP server**. Pokud Meta v téže aplikaci nabízí kompatibilní použití pro Marketing API, přidejte ho pro CLI. V **Business** vyberte portfolio vybraného reklamního účtu. [Nastavení pro Meta Ads MCP](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-get-started) · [Kombinace použití aplikace](https://developers.facebook.com/documentation/development/create-an-app#what-are-use-cases)
3. Projděte **Requirements** podle toho, co Meta zobrazuje pro váš případ. V **Overview** zkontrolujte název, portfolio a použití a klikněte na **Go to dashboard**. V dashboardu potvrďte, že vidíte aplikaci se správným použitím. [Postup založení aplikace](https://developers.facebook.com/documentation/development/create-an-app#app-creation-steps)

## Systémový uživatel

1. Ve správném portfoliu otevřete **Meta Business Suite → Business Settings → Users → System Users → Add**. Zadejte například **Správa reklam** a vyberte roli **Employee**.
2. V **Accounts → Apps** vyberte aplikaci, klikněte na **Assign Users** a přiřaďte systémového uživatele. V **Accounts → Ad Accounts** mu přidělte vybraný reklamní účet a právo spravovat kampaně.
3. Pro tvorbu reklam přiřaďte používanou Facebook stránku přímo systémovému uživateli přes **System Users → Assign Assets → Pages** a povolte inzerci na této stránce. Zkontrolujte přiřazení aplikace, účtu a stránky. Ve Správci reklam si poznamenejte ID vybraného reklamního účtu. [Přiřazení aplikace, reklamního účtu a stránky](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/setup/get-started#authentication)

## Token pro MCP

V **System Users → Generate Token** vyberte připojenou aplikaci. V nabídce platnosti zvolte **Never**, pokud chcete token bez časového omezení a Meta tuto možnost pro vaše portfolio nabízí. Některá portfolia musí používat 60denní token. I token bez expirace lze odvolat. [Platnost systémových tokenů](https://developers.facebook.com/docs/business-management-apis/system-users/install-apps-and-generate-tokens/)

Zaškrtněte `ads_mcp_management` a `ads_management` pro správu reklam. Pro společný token přidejte také [oprávnění pro CLI](#token-pro-cli), pokud je aplikace nabízí. Token zadejte na svém počítači do skryté výzvy příkazu `connect-mcp`, který vám agent připraví. ID lze zadat s předponou `act_` i jako číslo. V chatu stačí potvrdit uložení. [Oprávnění MCP](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-get-started#permissions)

## Token pro CLI

Knihovna používá CLI ke kontrole uložené kampaně, rozpočtu a UTM. Po připojení MCP agent ověří CLI na stejném účtu. Začne společným tokenem. Pokud aplikace nenabízí potřebná oprávnění pro CLI, využijte kompatibilní použití pro Marketing API nebo druhou aplikaci ve stejném portfoliu se stejným systémovým uživatelem.

Meta pro CLI uvádí `ads_management`, `business_management`, `pages_show_list`, `pages_read_engagement`, `pages_manage_ads` a `read_insights`. Pro samostatný token zvolte v **System Users → Generate Token** aplikaci pro Marketing API a vložte token do skryté výzvy příkazu `connect-cli`. Agent ověří stejné ID účtu. [Oprávnění CLI](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/setup/get-started#authentication)

## Když krok nefunguje

| Co vidíte | Co zkontrolovat |
| --- | --- |
| **System Users** nebo přiřazení přístupu chybí | Otevřete správné portfolio a ověřte přístup správce. |
| Aplikace chybí v **Generate Token** | Ověřte, že je ve správném portfoliu a přiřazená systémovému uživateli. |
| Chybí `ads_mcp_management` | Ověřte použití pro Ads MCP a požadavky uvedené v dashboardu aplikace. |
| MCP nevrací vybraný účet | Porovnejte ID ze Správce reklam, přiřazení účtu a oprávnění tokenu. |
| macOS žádá o přístup ke Klíčence | Zkontrolujte, že jde o položku `fapi-meta-ads-mcp` nebo `fapi-meta-ads-cli` pro zadané ID účtu, a povolte čtení. |
| MCP funguje a CLI hlásí chybu přístupu | Ověřte použití pro Marketing API a oprávnění tokenu. |
| Meta hlásí limit Marketing API | Vyčkejte na obnovení kvóty pro daný reklamní účet a typ použití. Tato kvóta platí i při práci přes druhý nástroj. [Limity Marketing API](https://developers.facebook.com/docs/graph-api/overview/rate-limiting/#buc-rate-limits) |
