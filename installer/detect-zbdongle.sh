#!/usr/bin/env bash
set -Eeuo pipefail
OUT="${1:-/etc/divera-raspi-alarm/zigbee-adapter.env}"
mkdir -p "$(dirname "$OUT")"
found=""
for p in /dev/serial/by-id/*; do
  [[ -e "$p" ]] || continue
  name="$(basename "$p")"
  case "$name" in
    *SONOFF*|*Sonoff*|*ITead*|*CP2102*|*Silicon_Labs*) found="$p"; break ;;
  esac
done
if [[ -n "$found" ]]; then
  printf 'ZIGBEE_ADAPTER=%s\nZIGBEE_ADAPTER_TYPE=zstack\n' "$found" > "$OUT"
  chmod 0644 "$OUT"
  echo "$found"
  exit 0
fi
printf 'ZIGBEE_ADAPTER=\nZIGBEE_ADAPTER_TYPE=zstack\n' > "$OUT"
chmod 0644 "$OUT"
echo "Kein passender Zigbee-USB-Adapter erkannt." >&2
exit 2
