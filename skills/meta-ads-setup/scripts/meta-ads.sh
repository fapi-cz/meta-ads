#!/usr/bin/env bash
set -euo pipefail
umask 077

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
state_dir="$HOME/.local/share/fapi-meta-ads"
if [[ ! -e "$state_dir" && -d "$state_dir-course" ]]; then
    state_dir="$state_dir-course"
fi
export FAPI_META_ADS_STATE_DIR="${FAPI_META_ADS_STATE_DIR:-$state_dir}"
environment="$FAPI_META_ADS_STATE_DIR/venv"

require_python() {
    if [[ ! -x "$environment/bin/python" ]]; then
        printf '%s\n' 'Začněte instalací připojení Meta Ads MCP.' >&2
        return 1
    fi
}

install_component() {
    local command_name="$1"
    local package="$2"
    case "$(uname -s)" in
        Darwin|Linux) ;;
        *) printf '%s\n' 'Spusťte instalační příkaz v macOS nebo Linuxu. Ve Windows použijte wsl.exe.' >&2; exit 1 ;;
    esac

    mkdir -p "$FAPI_META_ADS_STATE_DIR"
    chmod 700 "$FAPI_META_ADS_STATE_DIR"
    if [[ -x "$environment/bin/$command_name" ]]; then
        return 0
    fi

    if command -v uv >/dev/null 2>&1; then
        uv_command="$(command -v uv)"
    else
        uv_command="$FAPI_META_ADS_STATE_DIR/bin/uv"
        if [[ ! -x "$uv_command" ]]; then
            installer="$(mktemp "$FAPI_META_ADS_STATE_DIR/uv-install.XXXXXX")"
            trap 'rm -f -- "$installer"' EXIT
            curl --fail --silent --show-error --location --proto '=https' \
                'https://astral.sh/uv/0.11.32/install.sh' --output "$installer"
            UV_UNMANAGED_INSTALL="$FAPI_META_ADS_STATE_DIR/bin" /bin/sh "$installer"
        fi
    fi

    if [[ ! -x "$environment/bin/python" ]]; then
        "$uv_command" venv --python 3.12 "$environment"
    fi
    "$uv_command" pip install --python "$environment/bin/python" "$package"
}

case "${1:-}" in
    install-mcp)
        install_component mcp-proxy 'mcp-proxy==0.15.0'
        ;;
    install-cli)
        require_python
        "$environment/bin/python" "$script_dir/runtime.py" check-mcp
        install_component meta 'meta-ads==1.3.1'
        "$environment/bin/meta" --version
        ;;
    python)
        require_python
        shift
        exec "$environment/bin/python" "$@"
        ;;
    status|connect-mcp|connect-cli|check-mcp|check-cli|cli|cli-json|mcp)
        require_python
        exec "$environment/bin/python" "$script_dir/runtime.py" "$@"
        ;;
    *)
        printf '%s\n' 'Použití: meta-ads.sh install-mcp|connect-mcp|check-mcp|install-cli|connect-cli|check-cli|status|python|cli|cli-json|mcp' >&2
        exit 2
        ;;
esac
