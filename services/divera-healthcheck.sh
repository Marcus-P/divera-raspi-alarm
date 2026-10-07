#!/usr/bin/env bash
set -u
bad=0
for s in mosquitto divera-admin; do systemctl is-active --quiet "$s" || { systemctl restart "$s"; bad=1; }; done
curl -fsS --max-time 5 http://127.0.0.1:8765/health >/dev/null || { systemctl restart divera-admin; bad=1; }
if [[ -e /etc/divera-raspi-alarm/zigbee-adapter.env ]] && grep -q '^ZIGBEE_ADAPTER=/dev/' /etc/divera-raspi-alarm/zigbee-adapter.env; then
 systemctl is-active --quiet zigbee2mqtt || { systemctl restart zigbee2mqtt; bad=1; }
fi
exit "$bad"
