# Nastavení přístupu v Metě

Použijte firemní portfolio, které vlastní nebo spravuje zamýšlený reklamní účet. K přiřazení aplikace a systémového uživatele potřebujete přístup správce portfolia nebo jeho pomoc.

## Registrace vývojáře

1. Přihlaste se svým stávajícím Facebook profilem a v Meta for Developers klikněte na **Get Started**. [Registrace](https://developers.facebook.com/async/registration)
2. Potvrďte podmínky a pravidla pro vývojáře. Ověřte telefon a e-mail podle výzev Mety.
3. Vyberte nejbližší povolání nebo roli a dokončete registraci. Výsledek ověřte v **My Apps**. [Postup registrace](https://developers.facebook.com/documentation/development/register)

## Založení aplikace

1. V **My Apps → Create App** zadejte například **Správa reklam MojeFirma** a firemní kontaktní e-mail. Pro jméno použijte svůj firemní název a účel aplikace. [Vytvořit aplikaci](https://developers.facebook.com/apps/creation/) · [Pravidla názvů](https://developers.facebook.com/docs/app-review/resources/logos/)
2. V **Use cases** zvolte **Create & manage ads with ads MCP server**. V **Business** vyberte portfolio vybraného reklamního účtu. [Nastavení pro Meta Ads MCP](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-get-started)
3. Projděte **Requirements** podle toho, co Meta zobrazuje pro váš případ. V **Overview** zkontrolujte název, portfolio a použití a klikněte na **Go to dashboard**. V dashboardu potvrďte, že vidíte aplikaci se správným použitím. [Postup založení aplikace](https://developers.facebook.com/documentation/development/create-an-app#app-creation-steps)

## Systémový uživatel

1. Ve správném portfoliu otevřete **Meta Business Suite → Business Settings → Users → System Users → Add**. Zadejte například **Správa reklam** a vyberte roli **Employee**.
2. V **Accounts → Apps** vyberte aplikaci, klikněte na **Assign Users** a přiřaďte systémového uživatele. V **Accounts → Ad Accounts** mu přidělte vybraný reklamní účet a právo spravovat kampaně. Pro tvorbu reklam přiřaďte také používanou Facebook stránku.
3. Zkontrolujte přiřazenou aplikaci a účet. Ve Správci reklam si poznamenejte ID vybraného reklamního účtu. [Systémoví uživatelé](https://developers.facebook.com/docs/business-management-apis/system-users) · [Přiřazení aplikace a účtu](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/setup/get-started#authentication)

## Token pro MCP

V **System Users → Generate Token** vyberte připojenou aplikaci. V nabídce platnosti zvolte **Never**, pokud chcete token bez časového omezení a Meta tuto možnost pro vaše portfolio nabízí. Některá portfolia musí používat 60denní token. I token bez expirace lze odvolat. [Platnost systémových tokenů](https://developers.facebook.com/docs/business-management-apis/system-users/install-apps-and-generate-tokens/)

Zaškrtněte `ads_mcp_management` a `ads_management` pro správu reklam. Token zadejte na svém počítači do skryté výzvy příkazu `connect-mcp`, který vám agent připraví. ID lze zadat s předponou `act_` i jako číslo. V chatu stačí potvrdit uložení. [Oprávnění MCP](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-mcp-server/ads-mcp-server-get-started#permissions)

## Token pro CLI

Agent nejdřív ověří, zda stejný token funguje i v CLI. Pro samostatný token přidejte v aplikaci použití **Create & manage ads with Marketing API**. Pokud Meta tuto kombinaci nenabídne, založte druhou aplikaci ve stejném portfoliu a přiřaďte jí systémového uživatele.

V **System Users → Generate Token** vyberte aplikaci pro Marketing API. Meta pro CLI uvádí `ads_management`, `business_management`, `pages_show_list`, `pages_read_engagement`, `pages_manage_ads` a `read_insights`. Token zadejte do skryté výzvy příkazu `connect-cli`. Agent ověří stejné ID účtu. [Oprávnění CLI](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/setup/get-started#authentication)

## Když krok nefunguje

| Co vidíte | Co zkontrolovat |
| --- | --- |
| **System Users** nebo přiřazení přístupu chybí | Otevřete správné portfolio a ověřte přístup správce. |
| Aplikace chybí v **Generate Token** | Ověřte, že je ve správném portfoliu a přiřazená systémovému uživateli. |
| Chybí `ads_mcp_management` | Ověřte použití pro Ads MCP a požadavky uvedené v dashboardu aplikace. |
| MCP nevrací vybraný účet | Porovnejte ID ze Správce reklam, přiřazení účtu a oprávnění tokenu. |
| macOS žádá o přístup ke Klíčence | Zkontrolujte, že jde o položku `fapi-meta-ads-mcp` nebo `fapi-meta-ads-cli` pro zadané ID účtu, a povolte čtení. |
| MCP funguje a CLI hlásí chybu přístupu | Ověřte použití pro Marketing API a oprávnění tokenu. |
