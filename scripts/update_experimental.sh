#!/bin/bash
# MiSTer Experimental Core Incubator updater helper
# SPDX-License-Identifier: MIT
set -euo pipefail

MISTER_ROOT="${MISTER_ROOT:-/media/fat}"
DROPIN_FILE="${MISTER_ROOT}/downloader_austinbland1_MiSTer-Experimental.ini"
DB_URL="${EXPERIMENTAL_DB_URL:-https://raw.githubusercontent.com/austinbland1/MiSTer-Experimental/db/db.json.zip}"
DB_ID="${EXPERIMENTAL_DB_ID:-austinbland1/MiSTer-Experimental}"

usage() {
  cat <<USAGE
Usage: $(basename "$0") [--install-only|--status|--remove]

Installs or removes the MiSTer Experimental Downloader drop-in configuration.
Run the normal MiSTer 'update' script afterward to install/update payloads.

Environment:
  MISTER_ROOT          MiSTer storage root (default: /media/fat)
  EXPERIMENTAL_DB_URL  Custom database URL
  EXPERIMENTAL_DB_ID   Downloader database section name
USAGE
}

install_dropin() {
  [[ -d "$MISTER_ROOT" ]] || { echo "ERROR: MiSTer root not found: $MISTER_ROOT" >&2; exit 1; }
  cat > "$DROPIN_FILE" <<INI
[${DB_ID}]
db_url = ${DB_URL}
INI
  chmod 0644 "$DROPIN_FILE"
  echo "Installed: $DROPIN_FILE"
}

case "${1:-}" in
  "") install_dropin; exit 0 ;;
  --install-only) install_dropin ;;
  --status)
    echo "MiSTer root: $MISTER_ROOT"
    echo "Drop-in: $DROPIN_FILE"
    if [[ -f "$DROPIN_FILE" ]]; then cat "$DROPIN_FILE"; else echo "not installed"; fi
    ;;
  --remove)
    rm -f "$DROPIN_FILE"
    echo "Removed: $DROPIN_FILE"
    ;;
  -h|--help) usage ;;
  *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
esac
