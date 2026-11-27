import fcntl
import json
import os
import re
import subprocess
import sys
import tempfile
import termios
import tty
from pathlib import Path
from urllib.parse import quote, quote_plus


STATE_DIR = Path(os.environ["FAPI_META_ADS_STATE_DIR"]).resolve()
CREDENTIALS = STATE_DIR / "credentials.json"
META_MCP_URL = "https://mcp.facebook.com/ads"
KEYCHAIN = "/usr/bin/security"
KEYCHAIN_REFERENCE = {"storage": "keychain"}
TOKEN_PATTERN = re.compile(r"[\x21-\x7e]{1,4096}")


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
    sys.exit("Uložte přístup k Meta Ads MCP příkazem connect-mcp v místním Terminálu.")


def keychain_item(channel, account):
    return ["-s", f"fapi-meta-ads-{channel}", "-a", account]


def read_token(channel, credentials):
    stored = credentials.get(channel)
    if stored != KEYCHAIN_REFERENCE:
        return stored if isinstance(stored, str) else ""

    message = f"Token {channel.upper()} v Klíčence je nepřístupný nebo neplatný. Použijte connect-{channel}."
    try:
        result = subprocess.run(
            [KEYCHAIN, "find-generic-password", *keychain_item(channel, credentials["account"]), "-w"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        sys.exit(message)
    token = result.stdout.rstrip("\r\n")
    if not TOKEN_PATTERN.fullmatch(token):
        sys.exit(message)
    return token


def hidden_input(prompt):
    descriptor = sys.stdin.fileno()
    original_mode = termios.tcgetattr(descriptor)
    # Canonical terminal input also limits long pasted lines on macOS.
    tty.setcbreak(descriptor)
    try:
        print(prompt, end="", flush=True)
        value = bytearray()
        while character := os.read(descriptor, 1):
            if character in (b"\r", b"\n"):
                return value.decode("ascii").strip()
            if character in (b"\b", b"\x7f"):
                del value[-1:]
            elif character == b"\x04":
                break
            else:
                value.extend(character)
        raise EOFError
    finally:
        termios.tcsetattr(descriptor, termios.TCSAFLUSH, original_mode)
        print(flush=True)


def prompt_token(channel, account):
    try:
        token = hidden_input(f"Vložte celý token {channel.upper()} a stiskněte Enter: ")
    except (OSError, termios.error):
        sys.exit("Terminál nepodporuje skryté zadání tokenu.")
    except UnicodeDecodeError:
        sys.exit("Zadaný token nemá platný formát.")
    if not TOKEN_PATTERN.fullmatch(token):
        sys.exit("Zadaný token nemá platný formát.")

    if sys.platform == "darwin":
        from macos_keychain import store_token

        try:
            store_token(f"fapi-meta-ads-{channel}", account, token)
        except OSError as error:
            status = f" ({error.errno})" if error.errno is not None else ""
            sys.exit(f"Token se nepodařilo uložit do Klíčenky{status}. Odemkněte ji a zopakujte connect-{channel}.")
        if read_token(channel, {"account": account, channel: KEYCHAIN_REFERENCE}) != token:
            sys.exit(f"Klíčenka nevrátila celý token. Zopakujte connect-{channel}.")
        return KEYCHAIN_REFERENCE
    return token


def update_credentials(channel, account):
    with (STATE_DIR / ".credentials.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        previous = load_credentials(required=False)
        if channel == "cli" and previous.get("account") != account:
            sys.exit("Reklamní účet byl mezitím změněn. Spusťte znovu connect-cli.")
        stored = prompt_token(channel, account)
        values = {**previous, channel: stored, "account": account}
        if channel == "mcp" and previous.get("account") != account:
            values.pop("cli", None)
        save_credentials(values)


def connect(channel):
    if not sys.stdin.isatty():
        sys.exit(f"Spusťte connect-{channel} v místním Terminálu pro skryté zadání tokenu.")

    try:
        if channel == "mcp":
            existing = load_credentials(required=False).get("account", "")
            prompt = f"ID reklamního účtu [{existing}]: " if existing else "ID reklamního účtu: "
            account = (input(prompt).strip() or existing).removeprefix("act_")
            if not re.fullmatch(r"[0-9]{1,32}", account):
                sys.exit("Zkontrolujte ID reklamního účtu.")
            account = f"act_{account}"
        else:
            account = load_credentials()["account"]
        update_credentials(channel, account)
    except (EOFError, KeyboardInterrupt):
        sys.exit("Zadávání přístupu bylo ukončeno.")
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
        token = read_token("mcp", credentials)
        if not token:
            sys.exit("Uložte token MCP příkazem connect-mcp v místním Terminálu.")
        program = STATE_DIR / "venv" / "bin" / "mcp-proxy"
        environment["API_ACCESS_TOKEN"] = token
        command = [str(program), "--transport", "streamablehttp", META_MCP_URL]
    else:
        if any(
            arg.split("=", 1)[0] in {"--debug", "--ad-account-id", "--business-id"}
            for arg in arguments
        ):
            sys.exit("Pro výběr účtu použijte connect-mcp.")
        program = STATE_DIR / "venv" / "bin" / "meta"
        token = read_token("cli" if credentials.get("cli") else "mcp", credentials)
        if not token:
            sys.exit("Uložte přístup příkazem connect-mcp nebo connect-cli v místním Terminálu.")
        environment["ACCESS_TOKEN"] = token
        environment["AD_ACCOUNT_ID"] = credentials["account"]
        options = ["--output", "json", "--no-input"] if channel == "cli-json" else []
        command = [str(program), *options, "ads", *arguments]
    if not program.is_file():
        sys.exit(f"Program {program.name} vyžaduje instalaci přes meta-ads-setup.")
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
        binaries = STATE_DIR / "venv/bin"
        print(json.dumps({
            "account": credentials.get("account"),
            "mcp_token": bool(credentials.get("mcp")),
            "separate_cli_token": bool(credentials.get("cli")),
            "cli_installed": os.access(binaries / "meta", os.X_OK),
            "mcp_installed": os.access(binaries / "mcp-proxy", os.X_OK),
        }))
    elif action in {"check-mcp", "check-cli"}:
        from verify_connection import verify_connection

        verify_connection(action, load_credentials())
    else:
        run_tool(action, sys.argv[2:])
