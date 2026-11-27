import fcntl
import json
import os
import re
import secrets
import subprocess
import sys
import tempfile
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, quote_plus


STATE_DIR = Path(os.environ["FAPI_META_ADS_STATE_DIR"]).resolve()
CREDENTIALS = STATE_DIR / "credentials.json"
META_MCP_URL = "https://mcp.facebook.com/ads"
FORM = """<!doctype html>
<html lang="cs"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Připojení Meta Ads</title>
<style>
body{font:1rem/1.5 system-ui;margin:3rem auto;padding:0 1.25rem;max-width:32rem}
label,input,button{display:block}input{box-sizing:border-box;width:100%;padding:.5rem;margin:.25rem 0 1rem}
button{font:inherit;padding:.5rem 1rem}
</style>
<h1>Připojení CHANNEL</h1>
<p>Přístup se uloží do soukromé složky tohoto počítače.</p>
<form method="post" autocomplete="off">
ACCOUNT_INPUT
<label for="token">Token pro CHANNEL</label>
<input id="token" name="token" type="password" required>
<button>Uložit přístup</button>
</form>
</html>"""


def save_credentials(values):
    with tempfile.NamedTemporaryFile(
        dir=STATE_DIR, prefix=".credentials-", mode="w", delete=False, encoding="utf-8"
    ) as pending:
        pending_path = Path(pending.name)
        try:
            json.dump(values, pending)
            pending.flush()
            pending_path.replace(CREDENTIALS)
        finally:
            pending_path.unlink(missing_ok=True)


def load_credentials(required=True):
    try:
        if not CREDENTIALS.is_symlink() and CREDENTIALS.is_file() and (CREDENTIALS.stat().st_mode & 0o077) == 0:
            values = json.loads(CREDENTIALS.read_text(encoding="utf-8"))
            if isinstance(values, dict) and re.fullmatch(r"act_[0-9]{1,32}", str(values.get("account"))):
                return values
    except (OSError, ValueError):
        pass
    if not required:
        return {}
    sys.exit("Uložte přístup k Meta Ads MCP pomocí místního formuláře.")


def update_credentials(channel, token, account):
    with (STATE_DIR / ".credentials.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        previous = load_credentials(required=False)
        if channel == "cli" and previous.get("account") != account:
            raise ValueError("Reklamní účet byl mezitím změněn. Otevřete nový formulář CLI.")
        values = {**previous, channel: token, "account": account}
        if channel == "mcp" and previous.get("account") != account:
            values.pop("cli", None)
        save_credentials(values)


def connect(channel):
    account_input = ""
    cli_account = None
    if channel == "mcp":
        account_input = (
            '<label for="account">ID reklamního účtu</label>'
            '<input id="account" name="account" placeholder="act_123456789" required>'
        )
    else:
        cli_account = load_credentials()["account"]
    form = FORM.replace("CHANNEL", f"Meta Ads {channel.upper()}").replace("ACCOUNT_INPUT", account_input)
    form_path = "/" + secrets.token_urlsafe(24)
    saved = False

    class ConnectionPage(BaseHTTPRequestHandler):
        def setup(self):
            self.request.settimeout(10)
            super().setup()

        def log_message(self, *_args):
            return

        def send_page(self, status, page):
            body = page.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Referrer-Policy", "same-origin")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'",
            )
            self.end_headers()
            self.wfile.write(body)

        def valid_request(self):
            return self.path == form_path and self.headers.get("Host") == host

        def do_GET(self):
            if not self.valid_request():
                self.send_page(404, "Odkaz na formulář není platný.")
                return
            self.send_page(200, form)

        def do_POST(self):
            nonlocal saved
            if not self.valid_request() or self.headers.get("Origin") != origin:
                self.send_page(403, "Otevřete formulář z odkazu v chatu.")
                return

            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 8192:
                    raise ValueError
                if self.headers.get_content_type() != "application/x-www-form-urlencoded":
                    raise ValueError
                fields = parse_qs(self.rfile.read(length).decode("utf-8"), max_num_fields=2)
                token = fields.get("token", [""])[0].strip()
                if not re.fullmatch(r"[\x21-\x7e]{1,4096}", token):
                    raise ValueError
                account = cli_account
                if channel == "mcp":
                    account = fields.get("account", [""])[0].strip().removeprefix("act_")
                    if not re.fullmatch(r"[0-9]{1,32}", account):
                        raise ValueError
                    account = f"act_{account}"
            except (UnicodeError, ValueError):
                self.send_page(400, '<meta charset="utf-8"><p>Zkontrolujte vyplněné údaje.</p>' + form)
                return

            try:
                update_credentials(channel, token, account)
            except ValueError as error:
                self.send_page(409, str(error))
                return
            except OSError:
                self.send_page(500, '<meta charset="utf-8"><p>Přístup se nepodařilo uložit. Vraťte se do chatu.</p>')
                return
            saved = True
            self.send_page(200, '<meta charset="utf-8"><p>Přístup je uložený. Vraťte se do chatu.</p>')

    with HTTPServer(("127.0.0.1", 0), ConnectionPage) as server:
        host = f"127.0.0.1:{server.server_port}"
        origin = f"http://{host}"
        print(f"{origin}{form_path}", flush=True)
        deadline = time.monotonic() + 600
        while not saved and time.monotonic() < deadline:
            server.timeout = min(1, deadline - time.monotonic())
            server.handle_request()

    if not saved:
        sys.exit("Platnost odkazu vypršela. Otevřete nový formulář z chatu.")
    print(f"Přístup {channel.upper()} uložen.")


def redact(text, token):
    for value in {token, quote(token, safe=""), quote_plus(token)} - {""}:
        text = text.replace(value, "[token]")
    return text


def tool_command(channel, arguments, credentials):
    environment = os.environ.copy()
    for key in ("APP_ID", "APP_SECRET", "BUSINESS_ID", "ACCESS_TOKEN", "API_ACCESS_TOKEN"):
        environment.pop(key, None)
    if channel == "mcp":
        if not credentials.get("mcp"):
            sys.exit("Uložte nejdřív token MCP v místním formuláři.")
        program = STATE_DIR / "venv" / "bin" / "mcp-proxy"
        environment["API_ACCESS_TOKEN"] = credentials["mcp"]
        command = [str(program), "--transport", "streamablehttp", META_MCP_URL]
    else:
        if any(
            arg.split("=", 1)[0] in {"--debug", "--ad-account-id", "--business-id"}
            for arg in arguments
        ):
            sys.exit("Pro výběr účtu použijte formulář pro připojení.")
        program = STATE_DIR / "venv" / "bin" / "meta"
        token = credentials.get("cli") or credentials.get("mcp")
        if not token:
            sys.exit("Nejprve uložte přístup v místním formuláři.")
        environment["ACCESS_TOKEN"] = token
        environment["AD_ACCOUNT_ID"] = credentials["account"]
        options = ["--output", "json", "--no-input"] if channel == "cli-json" else []
        command = [str(program), *options, "ads", *arguments]
    if not program.is_file():
        sys.exit(f"Program {program.name} vyžaduje instalaci přes kurzový skill.")
    return command, environment


def cli_result(command, environment):
    try:
        result = subprocess.run(
            command, env=environment, cwd=STATE_DIR, capture_output=True, text=True, timeout=60
        )
    except subprocess.TimeoutExpired:
        raise ValueError("Meta Ads CLI neodpovědělo v časovém limitu.") from None
    token = environment["ACCESS_TOKEN"]
    if result.returncode:
        diagnostic = redact((result.stderr or result.stdout).strip(), token)
        raise ValueError(diagnostic or "Dotaz Meta Ads CLI selhal.")
    try:
        return json.loads(redact(result.stdout, token))
    except json.JSONDecodeError:
        raise ValueError("Meta Ads CLI nevrátilo očekávaný výpis v JSON.") from None


def run_tool(channel, arguments):
    command, environment = tool_command(channel, arguments, load_credentials())
    if channel == "cli-json" and arguments[:2] == ["insights", "get"] and not {"--help", "-h"}.intersection(arguments):
        try:
            payload = cli_result(command, environment)
            print(json.dumps({"data": payload["data"], "has_more": bool((payload.get("paging") or {}).get("next"))}))
        except (ValueError, KeyError, TypeError, AttributeError) as error:
            sys.exit(str(error))
        return
    os.chdir(STATE_DIR)
    os.execve(command[0], command, environment)


if __name__ == "__main__":
    action = sys.argv[1]
    if action.startswith("connect-"):
        connect(action.split("-", 1)[1])
    elif action == "status":
        credentials = load_credentials(required=False)
        print(json.dumps({"account": credentials.get("account"), "mcp_token": bool(credentials.get("mcp")), "separate_cli_token": bool(credentials.get("cli"))}))
    elif action in {"check-mcp", "check-cli"}:
        from verify_connection import verify_connection

        verify_connection(action, load_credentials())
    else:
        run_tool(action, sys.argv[2:])
