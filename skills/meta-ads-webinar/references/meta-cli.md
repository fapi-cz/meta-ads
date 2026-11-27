# Pozastavená kampaň přes Meta Ads CLI

Příklady uvádějí příkazy po `meta-ads.sh cli-json`. Nahraď zástupné hodnoty skutečnými údaji z odsouhlaseného zadání. Při správě reklamy se nemění zdrojová kampaň.

## Okamžitý formulář

1. Použij `campaign create --objective OUTCOME_LEADS --lifetime-budget MINOR --status PAUSED` pro sjednanou částku za celou dobu. Při denním zadání použij `--daily-budget MINOR`. Rozpočet je na kampani.
2. Vytvoř sadu přes `adset create --campaign-id ID --destination-type ON_AD --optimization-goal LEAD_GENERATION --billing-event IMPRESSIONS --promoted-object '{"page_id":"PAGE_ID"}' --status PAUSED`. Doplň `--name`, schválené cílení, časy a u doručování v EU plátce a příjemce výhod. Termín konce uveď pomocí `--end-time`.
3. V kreativě použij `creative create --name NAZEV --object-story-spec @ABSOLUTNI_SOUBOR_JSON`. Pro obrazový podklad vychází spec z tohoto tvaru.

   ```json
   {
     "page_id": "PAGE_ID",
     "link_data": {
       "link": "http://fb.me/",
       "image_hash": "IMAGE_HASH",
       "message": "Schválený text",
       "call_to_action": {
         "type": "SIGN_UP",
         "value": { "lead_gen_form_id": "FORM_ID" }
       }
     }
   }
   ```

   Pro video použij `video_data` s `video_id`, platným náhledem a `call_to_action.value` s `link` a `lead_gen_form_id`. Použij skutečný hash nebo ID z knihovny správného účtu. Pro nové podklady využij podporovaný upload v Meta nástrojích, případně nahrání do knihovny účtu ve Správci reklam. Oficiální CLI bere při režimu `--object-story-spec` hotový spec, standardní přepínače obrázku a videa patří do jiného režimu. [Tvorba lead reklamy a videa](https://developers.facebook.com/docs/marketing-api/guides/lead-ads/create/v2.6/)
4. Pro každou připravenou kreativu vytvoř reklamu přes `ad create --name NAZEV --adset-id ID --creative-id ID --status PAUSED`. Pro varianty umístění použij jen Meta formát, který zachová vazbu na ohlašovaný formulář. Po nahrání videa ověř, že ho Meta zpracovala.

## Zpětná kontrola

Spusť přes `meta-ads.sh python`:

```sh
check_webinar.py --campaign-id ID --adset-id ID --ad-id ID --ad-id ID \
  --type lifetime --budget-minor 350000 --start-time ISO_ZACATEK --end-time ISO_KONEC \
  --form-id ID --page-id ID
```

Použij úplnou cestu ke skriptu a předej všechna vytvořená ID pomocí opakovaného `--ad-id`. Skript ověří účet, jednu sadu, očekávané reklamy, pozastavení, rozpočet, termíny a vazbu kreativy na formulář. Pro web vytvoř sadu s `--destination-type WEBSITE` a webovou kreativu s `--url-tags`. Místo `--form-id` a `--page-id` předej `--web-url URL` s připraveným odkazem pro nový webinář a podle potřeby `--ref-code`.

Zkontroluj Feed, Stories, Reels nebo další zvolená umístění v náhledu Mety. Pokud v připojeném nástroji chybí náhled daného umístění, dej účastníkovi ID reklamy a postup **Správce reklam → Reklamy → Náhled**. Zkontroluj čitelnost textu, ořez, CTA, zvuk i otevření formuláře či cílové stránky. Úspěch skriptu dokládá uložené nastavení v účtu. Výsledek vizuálního náhledu a ověřené potvrzení ze SmartEmailingu zaznamenej podle skutečně provedené kontroly. [Meta náhledy reklam](https://developers.facebook.com/docs/marketing-api/generatepreview/v8.0/)
