#!/usr/bin/env bash
set -euo pipefail
umask 077

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export FAPI_META_ADS_STATE_DIR="${FAPI_META_ADS_STATE_DIR:-$HOME/.local/share/fapi-meta-ads-course}"
environment="$FAPI_META_ADS_STATE_DIR/venv"

install_runtime() {
    case "$(uname -s)" in
        Darwin|Linux) ;;
        *) printf '%s\n' 'Meta Ads CLI vyžaduje místní macOS nebo Linux (na Windows WSL).' >&2; exit 1 ;;
    esac

    mkdir -p "$FAPI_META_ADS_STATE_DIR"
    chmod 700 "$FAPI_META_ADS_STATE_DIR"
    if [[ -x "$environment/bin/meta" && -x "$environment/bin/mcp-proxy" ]]; then
        "$environment/bin/meta" --version
        return
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
    "$uv_command" pip install --python "$environment/bin/python" 'meta-ads==1.3.1' 'mcp-proxy==0.15.0'
    "$environment/bin/meta" --version
}

case "${1:-}" in
    install)
        install_runtime
        ;;
    connect|cli|mcp)
        if [[ ! -x "$environment/bin/python" ]]; then
            printf '%s\n' 'Nejdříve spusťte s agentem nastavení Meta Ads podle kurzu FAPI.' >&2
            exit 1
        fi
        exec "$environment/bin/python" "$script_dir/runtime.py" "$@"
        ;;
    *)
        printf '%s\n' 'Použití pro agenta: course-ads.sh install|connect|cli|mcp' >&2
        exit 2
        ;;
esac
