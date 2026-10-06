#!/usr/bin/env bash
set -Eeuo pipefail
CONFIG=/etc/divera-raspi-alarm/config.toml
DIVERA_URL="$(python3 -c 'import tomllib;print(tomllib.load(open("'"$CONFIG"'","rb"))["kiosk"]["divera_url"])')"
ADMIN_URL="$(python3 -c 'import tomllib;print(tomllib.load(open("'"$CONFIG"'","rb"))["kiosk"].get("admin_url","http://127.0.0.1:8765/"))')"
[[ -n "$DIVERA_URL" ]] || DIVERA_URL="http://127.0.0.1:8765/divera"
exec chromium "$DIVERA_URL" "$ADMIN_URL" --kiosk --noerrdialogs --disable-infobars --no-first-run --enable-features=OverlayScrollbar --start-maximized
