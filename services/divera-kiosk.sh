#!/usr/bin/env bash
set -Eeuo pipefail
C=/etc/divera-raspi-alarm/config.toml
while true; do
 D="$(python3 -c 'import tomllib;print(tomllib.load(open("'"$C"'","rb"))["kiosk"]["divera_url"])')"
 A="$(python3 -c 'import tomllib;print(tomllib.load(open("'"$C"'","rb"))["kiosk"].get("admin_url","http://127.0.0.1:8765/"))')"
 [[ -n "$D" ]] || D="http://127.0.0.1:8765/"
 chromium "$D" "$A" --kiosk --noerrdialogs --disable-infobars --no-first-run --disable-session-crashed-bubble --enable-features=OverlayScrollbar --start-maximized || true
 sleep 3
done
