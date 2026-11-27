# Spuštění na macOS, Linuxu a Windows

Používej stejný spouštěč pro instalaci, zadání tokenu, kontrolu účtu, registraci MCP i kontroly kampaní a UTM. Vždy dosaď skutečné absolutní cesty.

V Codex Desktop lze místo příkazu `codex mcp add` použít **Settings → MCP servers → Add server → STDIO**. Zadej příkaz a argumenty pro daný systém. [Nastavení Codexu](https://learn.chatgpt.com/docs/extend/mcp#configure-in-the-chatgpt-desktop-app)

Oficiální balíček Meta Ads CLI 1.3.1 je publikovaný pro Mac s Apple Silicon a Linux s glibc na x86‑64 a ARM64. [Distribuce balíčku](https://pypi.org/project/meta-ads/1.3.1/#files)

## Připojení v Terminálu

Po [nastavení přístupu v Metě](meta-browser.md) otevřete Terminál v kořeni staženého repozitáře. Na Macu s Apple Silicon, v Linuxu a ve WSL můžete použít tento postup.

```bash
bash skills/meta-ads-setup/scripts/meta-ads.sh install-cli
bash skills/meta-ads-setup/scripts/meta-ads.sh connect-mcp
bash skills/meta-ads-setup/scripts/meta-ads.sh check-cli
```

`connect-mcp` uloží ID účtu a společný token pro oba nástroje. Po zadání ID vložte celý token do skryté výzvy a stiskněte Enter. Při výměně stačí uložené ID potvrdit Enterem. Na Macu skript ověří, že z Klíčenky načte přesně celý uložený token. V Linuxu a ve WSL se přístup ukládá do soukromého souboru v domovské složce.

Pro MCP spusťte `install-mcp` a `check-mcp` stejným způsobem. Pokud používáte jen MCP, spusťte `install-mcp` před zadáním tokenu. Po úspěšné kontrole zaregistrujte server podle platformy níže. Pokud Meta účtu ještě nepovolila Ads MCP, skilly mohou pracovat přes ověřené CLI.

## macOS a Linux

V terminálu macOS nebo Linuxu použij `bash '/absolutní/cesta/meta-ads.sh' PŘÍKAZ`. To platí i v terminálu otevřeném uvnitř WSL. Skripty ostatních skillů spouštěj přes `bash '/absolutní/cesta/meta-ads.sh' python '/absolutní/cesta/test_ads.py' ARGUMENTY`.

Na Macu použij `open-connect-mcp` nebo `open-connect-cli`, pokud má agent otevřít skrytou výzvu v Terminálu. Pokud otevření nepovolí systém, dej uživateli přesný příkaz `connect-mcp` nebo `connect-cli` pro už otevřený Terminál.

Pro STDIO použij `bash` jako příkaz a cestu ke spouštěči a `mcp` jako argumenty.

```bash
codex mcp add fapi-meta-ads -- bash '/absolutní/cesta/meta-ads.sh' mcp
claude mcp add --scope user --transport stdio fapi-meta-ads -- bash '/absolutní/cesta/meta-ads.sh' mcp
```

Na macOS lze Codex CLI spustit také z `/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex`, pokud je tam nainstalované. V Claude Code použij už funkční server z pluginu nebo projektu.

## Windows

Codex a Claude Code mohou běžet ve Windows. Instalaci a všechny kontroly spusť přes jednu distribuci WSL, protože oficiální Meta Ads CLI je dostupné pro macOS a Linux. [Požadavky Meta Ads CLI](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/setup/get-started)

1. V PowerShellu spusť `wsl.exe --list --verbose` a vezmi název dostupné distribuce. Pokud WSL chybí, uživatel ho nainstaluje příkazem `wsl.exe --install -d Ubuntu` v PowerShellu správce a dokončí první spuštění Ubuntu. [Instalace WSL](https://learn.microsoft.com/windows/wsl/install)
2. Pokud je spouštěč na disku Windows, převeď cestu pomocí `wslpath` ve zvolené distribuci. Pokud je knihovna uvnitř WSL, použij její absolutní linuxovou cestu.

   ```powershell
   $metaAdsDistro = 'Ubuntu'
   $metaAdsWindowsPath = 'C:\Users\Jana\.codex\skills\meta-ads-setup\scripts\meta-ads.sh'
   $metaAdsLauncher = wsl.exe --distribution $metaAdsDistro --exec wslpath -u $metaAdsWindowsPath
   if ($LASTEXITCODE -ne 0 -or !$metaAdsLauncher) { throw 'Cestu ke spouštěči ve WSL se nepodařilo převést.' }
   $metaAdsStdio = @('--distribution', $metaAdsDistro, '--exec', 'bash', $metaAdsLauncher)
   wsl.exe @metaAdsStdio status
   ```

3. Spouštěj další příkazy stejným způsobem, například `wsl.exe @metaAdsStdio check-mcp` a `wsl.exe @metaAdsStdio check-cli`. Pro skripty ostatních skillů použij `wsl.exe @metaAdsStdio python ABSOLUTNÍ_LINUXOVÁ_CESTA ARGUMENTY`. Pro soubory na disku Windows, včetně médií a vstupních JSON, převeď cesty stejně jako u spouštěče. Přístup se ukládá do domovské složky uživatele uvnitř této distribuce.
4. Pro zadání tokenu dej uživateli připravený příkaz `bash '/skutečná/linuxová/cesta/meta-ads.sh' connect-mcp` nebo `connect-cli` a napiš, kterou distribuci má otevřít ve Windows Terminalu. Tam má skrytá výzva vlastní interaktivní terminál.
5. Po úspěšném `check-mcp` zaregistruj v nativním klientovi STDIO server s příkazem `wsl.exe` a argumenty z `$metaAdsStdio` následovanými `mcp`. Tuto konfiguraci použij i pro Claude Code z pluginu ve Windows.

   ```powershell
   codex mcp add fapi-meta-ads -- wsl.exe --distribution $metaAdsDistro --exec bash $metaAdsLauncher mcp
   claude mcp add --scope user --transport stdio fapi-meta-ads -- wsl.exe --distribution $metaAdsDistro --exec bash $metaAdsLauncher mcp
   ```

Používej stále tutéž distribuci a uživatele pro MCP, CLI, uložené tokeny i kontroly reklam. [Spuštění linuxových příkazů z Windows](https://learn.microsoft.com/windows/dev-environment/wsl-interop)
