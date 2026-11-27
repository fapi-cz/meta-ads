import json
import subprocess
from pathlib import Path


LAUNCHER = Path(__file__).with_name("course-ads.sh")


def launcher_json(*arguments):
    try:
        result = subprocess.run(
            ["bash", str(LAUNCHER), *arguments],
            capture_output=True,
            text=True,
            timeout=75,
        )
    except subprocess.TimeoutExpired:
        raise ValueError("Čtení z Meta Ads překročilo časový limit.") from None
    if result.returncode:
        raise ValueError(f"Selhalo čtení Meta Ads ({' '.join(arguments[:3])}).")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        raise ValueError("Meta Ads vrátila neplatný JSON.") from None


def cli_read(*arguments):
    return launcher_json("cli-json", *arguments)


def selected_account():
    account = launcher_json("status").get("account")
    if not account:
        raise ValueError("Nejprve připojte reklamní účet pomocí startovacího skillu.")
    return account


def require_account(entity, expected):
    if str(entity.get("account_id")).removeprefix("act_") != expected.removeprefix("act_"):
        raise ValueError(f"Objekt {entity.get('id')} v Metě nepatří k účtu {expected}.")


def rows(payload):
    data = payload.get("data") if isinstance(payload, dict) else payload
    if not isinstance(data, list) or any(not isinstance(row, dict) for row in data):
        raise ValueError("Meta Ads nevrátila očekávané řádky.")
    return data
