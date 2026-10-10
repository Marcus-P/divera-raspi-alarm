#!/usr/bin/env bash
set -Eeuo pipefail
# The desktop account has no access to the private application state.
# Read only non-secret display settings from the loopback admin endpoint.
get_urls() {
 python3 - <<'PY'
import json
import urllib.request
try:
    with urllib.request.urlopen("http://127.0.0.1:8765/api/display-config", timeout=3) as response:
        settings = json.load(response)
except Exception:
    settings = {}
admin = settings.get("admin_url") or "http://127.0.0.1:8765/"
print(settings.get("divera_url") or admin)
print(admin)
PY
}
while true; do
 mapfile -t URLS < <(get_urls)
 D="${URLS[0]:-http://127.0.0.1:8765/}"
 A="${URLS[1]:-http://127.0.0.1:8765/}"
 chromium --kiosk --password-store=basic --no-default-browser-check --noerrdialogs --disable-infobars --no-first-run --disable-session-crashed-bubble --disable-breakpad --disk-cache-size=52428800 --media-cache-size=52428800 --enable-features=OverlayScrollbar --start-maximized "$D" "$A" || true
 sleep 3
done
