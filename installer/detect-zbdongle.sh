#!/usr/bin/env bash
set -Eeuo pipefail
OUT="${1:-/etc/divera-raspi-alarm/zigbee-adapter.env}"; ZCFG=/var/lib/zigbee2mqtt/configuration.yaml
found=""
for p in /dev/serial/by-id/*; do [[ -e "$p" ]] || continue; n="$(basename "$p")"; case "$n" in *SONOFF*|*Sonoff*|*ITead*|*CP2102*|*Silicon_Labs*) found="$p";break;; esac; done
install -d -m 0755 "$(dirname "$OUT")"
if [[ -z "$found" ]]; then printf 'ZIGBEE_ADAPTER=\nZIGBEE_ADAPTER_TYPE=zstack\n' >"$OUT"; exit 2; fi
printf 'ZIGBEE_ADAPTER=%s\nZIGBEE_ADAPTER_TYPE=zstack\n' "$found" >"$OUT"; chmod 0644 "$OUT"
if id zigbee2mqtt >/dev/null 2>&1; then
 install -d -o zigbee2mqtt -g zigbee2mqtt -m 0750 /var/lib/zigbee2mqtt
 cat >"$ZCFG" <<EOF
version: 5
mqtt:
  base_topic: zigbee2mqtt
  server: mqtt://127.0.0.1:1883
serial:
  port: $found
  adapter: zstack
frontend:
  enabled: true
  port: 8080
homeassistant:
  enabled: false
advanced:
  log_output: [console]
availability:
  enabled: true
permit_join: false
EOF
 chown zigbee2mqtt:zigbee2mqtt "$ZCFG"; chmod 0640 "$ZCFG"; systemctl try-restart zigbee2mqtt.service || true
fi
echo "$found"
