#!/bin/bash
# MiSTer Experimental Core Incubator updater
# SPDX-License-Identifier: MIT
set -euo pipefail

MISTER_ROOT="${MISTER_ROOT:-/media/fat}"
DOWNLOADER="${MISTER_ROOT}/Scripts/downloader.sh"
DROPIN_FILE="${MISTER_ROOT}/downloader_experimental.ini"
TMP_DIR="${TMPDIR:-/tmp}/mister-experimental"

# These are intentionally configurable so a fork can point at its own database.
EXPERIMENTAL_DB_URL="${EXPERIMENTAL_DB_URL:-https://raw.githubusercontent.com/austinbland1/MiSTer-Experimental/db/db.json.zip}"
EXPERIMENTAL_DB_ID="${EXPERIMENTAL_DB_ID:-austinbland1/MiSTer-Experimental}"

usage() {
    cat <<USAGE
Usage: $(basename "$0") [options]

Installs/refreshes the Experimental Core Incubator Downloader database and
then runs MiSTer Downloader with the normal MiSTer storage root.

Options:
  --install-only   Install/update the drop-in database, do not run Downloader.
  --run            Run Downloader after installing (default).
  --status         Show local installation status.
  --remove        Remove the experimental drop-in database.
  -h, --help       Show this help.

Environment:
  MISTER_ROOT          MiSTer storage root (default: /media/fat)
  EXPERIMENTAL_DB_URL  Custom database URL
  EXPERIMENTAL_DB_ID   Downloader database section name
USAGE
}

say() { printf '[experimental] %s\n' "$*"; }
fail() { printf '[experimental] ERROR: %s\n' "$*" >&2; exit 1; }

install_dropin() {
    [[ -d "$MISTER_ROOT" ]] || fail "MiSTer root does not exist: $MISTER_ROOT"
    # Downloader supports drop-in *.ini files, so we don't modify the user's
    # main downloader.ini. This file is safe to replace on each update.
    cat > "$DROPIN_FILE" <<INI
[${EXPERIMENTAL_DB_ID}]
db_url = ${EXPERIMENTAL_DB_URL}
INI

    chmod 0644 "$DROPIN_FILE"
    say "Installed database configuration: $DROPIN_FILE"
    say "Database: $EXPERIMENTAL_DB_URL"
}

remove_dropin() {
    if [[ -e "$DROPIN_FILE" ]]; then
        rm -f "$DROPIN_FILE"
        say "Removed $DROPIN_FILE"
    else
        say "Nothing to remove."
    fi
}

status() {
    echo "MiSTer root:       $MISTER_ROOT"
    echo "Downloader:        $DOWNLOADER"
    echo "Drop-in database:  $DROPIN_FILE"
    echo "Configured DB URL:  $EXPERIMENTAL_DB_URL"
    if [[ -f "$DROPIN_FILE" ]]; then
        echo "Installed:         yes"
        echo
        cat "$DROPIN_FILE"
    else
        echo "Installed:         no"
    fi
}

run_downloader() {
    [[ -x "$DOWNLOADER" ]] || fail "MiSTer Downloader launcher not found/executable: $DOWNLOADER"
    say "Starting MiSTer Downloader..."
    exec "$DOWNLOADER"
}

MODE="run"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --install-only) MODE="install" ;;
        --run)          MODE="run" ;;
        --status)       MODE="status" ;;
        --remove)       MODE="remove" ;;
        -h|--help)      usage; exit 0 ;;
        *)               fail "Unknown option: $1" ;;
    esac
    shift
done

case "$MODE" in
    install) install_dropin ;;
    remove)  remove_dropin ;;
    status)  status ;;
    run)
        install_dropin
        run_downloader
        ;;
esac
