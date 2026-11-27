import json
import re
import sys
from pathlib import Path

from runtime import STATE_DIR, cli_result, tool_command


def account_id(value):
    match = re.fullmatch(r"(?:act_)?([0-9]{1,32})", str(value))
    return f"act_{match[1]}" if match else None


def find_account(payload, expected):
    if isinstance(payload, dict):
        for key in ("account_id", "ad_account_id", "id"):
            if account_id(payload.get(key)) == expected:
                return payload
        children = payload.values()
    elif isinstance(payload, list):
        children = payload
    else:
        return None
    for child in children:
        found = find_account(child, expected)
        if found is not None:
            return found
    return None


async def load_mcp_account(credentials):
    from anyio import fail_after
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    command, environment = tool_command("mcp", [], credentials)
    proxy = StdioServerParameters(command=command[0], args=command[1:], env=environment, cwd=STATE_DIR)
    with Path("/dev/null").open("w") as diagnostics:
        with fail_after(35):
            async with stdio_client(proxy, errlog=diagnostics) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    page = await session.list_tools()
                    while not any(tool.name == "ads_get_ad_accounts" for tool in page.tools):
                        if not page.nextCursor:
                            return None
                        page = await session.list_tools(cursor=page.nextCursor)
                    result = await session.call_tool("ads_get_ad_accounts", {})
                    if result.isError:
                        return None

    payloads = [result.structuredContent]
    for content in result.content:
        if content.type == "text":
            try:
                payloads.append(json.loads(content.text))
            except json.JSONDecodeError:
                continue
    return find_account(payloads, credentials["account"])


def verify_connection(action, credentials):
    expected = credentials["account"]
    if action == "check-mcp":
        try:
            from anyio import run

            account = run(load_mcp_account, credentials)
        except Exception:
            sys.exit("MCP neodpovědělo. Zkontrolujte spojení, token a oprávnění ads_mcp_management.")
        if account is None or account.get("is_ads_mcp_enabled") is False or account.get("is_queryable") is False:
            sys.exit(f"MCP nepotvrdilo použitelný účet {expected}. Zkontrolujte přiřazení účtu a oprávnění aplikace.")
        channel = "mcp"
    else:
        try:
            command, environment = tool_command("cli-json", ["adaccount", "get"], credentials)
            account = find_account(cli_result(command, environment), expected)
            if account is None:
                sys.exit(f"CLI nevrátilo očekávaný účet {expected}.")
            command, environment = tool_command("cli-json", ["campaign", "list", "--limit", "1", "--fields", "id"], credentials)
            campaigns = cli_result(command, environment)
            if not isinstance(campaigns, list) and not (
                isinstance(campaigns, dict) and isinstance(campaigns.get("data"), list)
            ):
                sys.exit("CLI nevrátilo očekávaný výpis kampaní.")
        except ValueError as error:
            sys.exit(str(error))
        channel = "cli"

    print(json.dumps({"channel": channel, "account": expected, "verified": True}, ensure_ascii=False))
