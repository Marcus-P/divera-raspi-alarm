#!/usr/bin/env bash
set -Eeuo pipefail
# Detect a supported SONOFF ZBDongle-P without committing host-specific paths.
# Never overwrite an existing Zigbee2MQTT configuration or pairing database.
OUT="${1:-/etc/divera-raspi-alarm/zigbee-adapter.env}"
ZCFG=/var/lib/zigbee2mqtt/configuration.yaml
[[ $EUID -eq 0 ]] || { echo "Root privileges required." >&2; exit 1; }

shopt -s nullglob
matches=()
for p in /dev/serial/by-id/*; do
  [[ -e "$p" ]] || continue
  n="${p##*/}"
  case "$n" in
    *ITead*Sonoff*Zigbee*Dongle*|*ITEAD*SONOFF*Zigbee*Dongle*)
      matches+=("$p") ;;
  esac
done

case ${#matches[@]} in
  0) echo "No supported SONOFF ZBDongle-P found under /dev/serial/by-id." >&2; exit 2 ;;
  1) found="${matches[0]}" ;;
  *) printf 'Multiple matching Zigbee adapters; refusing automatic selection:\n%s\n' "${matches[@]}" >&2; exit 3 ;;
esac

# If a configuration already exists, leave it entirely untouched.
# An existing serial.port must be verified rather than silently replaced.
if [[ -f "$ZCFG" ]]; then
  python3 - "$ZCFG" "$found" <<'PY'
import pathlib, re, sys
cfg = pathlib.Path(sys.argv[1]).read_text()
found = sys.argv[2]
# Check the serial.port only inside the top-level serial mapping.
match = re.search(r'(?m)^serial:\s*(?:#.*)?\n((?:^[ \t]+.*\n|^\s*\n)*)', cfg)
if not match:
    sys.exit("Existing Zigbee2MQTT configuration has no recognizable serial section; refusing to change it.")
port = re.search(r'(?m)^[ \t]+port:\s*["\']?([^\s"\'#]+)', match.group(1))
if not port:
    sys.exit("Existing Zigbee2MQTT configuration has no serial.port; refusing to change it.")
configured = port.group(1)
if configured != found and pathlib.Path(configured).resolve() != pathlib.Path(found).resolve():
    sys.exit(f"Existing Zigbee2MQTT serial.port differs ({configured}); refusing to overwrite it.")
PY
else
  if id zigbee2mqtt >/dev/null 2>&1; then
    install -d -o zigbee2mqtt -g zigbee2mqtt -m 0750 /var/lib/zigbee2mqtt
    tmp="$(mktemp "${ZCFG}.XXXXXX")"
    trap 'rm -f "$tmp"' EXIT
    cat >"$tmp" <<EOF
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
    chown zigbee2mqtt:zigbee2mqtt "$tmp"
    chmod 0640 "$tmp"
    mv -n "$tmp" "$ZCFG"
    trap - EXIT
  fi
fi

# Store only on this host; do not modify configuration when detection fails.
install -d -m 0755 "$(dirname "$OUT")"
tmp_env="$(mktemp "${OUT}.XXXXXX")"
trap 'rm -f "$tmp_env"' EXIT
printf 'ZIGBEE_ADAPTER=%s\nZIGBEE_ADAPTER_TYPE=zstack\n' "$found" >"$tmp_env"
chmod 0644 "$tmp_env"
mv -f "$tmp_env" "$OUT"
trap - EXIT
echo "Detected Zigbee adapter: $found"
