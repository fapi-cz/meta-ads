import json
import os
import re
import secrets
import stat
import sys
import tempfile
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs


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
<h1>Připojení Meta Ads</h1>
<p>Přístup se uloží do soukromé složky tohoto počítače.</p>
<form method="post" autocomplete="off">
<label for="account">ID reklamního účtu</label>
<input id="account" name="account" placeholder="act_123456789" required>
<label for="cli">Token pro Meta Ads CLI</label>
<input id="cli" name="cli" type="password" required>
<label for="mcp">Samostatný token pro Meta Ads MCP</label>
<input id="mcp" name="mcp" type="password" aria-describedby="mcp-help">
<p id="mcp-help">Pokud máte společný token, toto pole nechte prázdné.</p>
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


def connect():
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
            self.send_page(200, FORM)

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
                fields = parse_qs(self.rfile.read(length).decode("utf-8"), max_num_fields=3)
                account = fields.get("account", [""])[0].strip().removeprefix("act_")
                cli = fields.get("cli", [""])[0].strip()
                mcp = fields.get("mcp", [""])[0].strip() or cli
                if not re.fullmatch(r"[0-9]{1,32}", account):
                    raise ValueError
                if not all(re.fullmatch(r"[\x21-\x7e]{1,4096}", token) for token in (cli, mcp)):
                    raise ValueError
            except (UnicodeError, ValueError):
                self.send_page(400, '<meta charset="utf-8"><p>Zkontrolujte ID a oba tokeny.</p>' + FORM)
                return

            try:
                save_credentials({"account": f"act_{account}", "cli": cli, "mcp": mcp})
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
    print("Přístup uložen. Ověřte účet přes CLI i MCP.")


def run_tool(channel, arguments):
    if CREDENTIALS.is_symlink() or not CREDENTIALS.is_file():
        sys.exit("Otevřete nejdřív místní formulář pro přístup k Meta Ads.")
    if stat.S_IMODE(CREDENTIALS.stat().st_mode) & 0o077:
        sys.exit("Znovu uložte přístup ve formuláři, aby měl soubor správná oprávnění.")

    credentials = json.loads(CREDENTIALS.read_text(encoding="utf-8"))
    environment = os.environ.copy()
    for key in ("APP_ID", "APP_SECRET", "BUSINESS_ID", "ACCESS_TOKEN", "API_ACCESS_TOKEN"):
        environment.pop(key, None)
    os.chdir(STATE_DIR)

    if channel == "mcp":
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
        environment["ACCESS_TOKEN"] = credentials["cli"]
        environment["AD_ACCOUNT_ID"] = credentials["account"]
        command = [str(program), "ads", *arguments]

    os.execve(program, command, environment)


if __name__ == "__main__":
    if sys.argv[1] == "connect":
        connect()
    else:
        run_tool(sys.argv[1], sys.argv[2:])
