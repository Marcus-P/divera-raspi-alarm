#!/usr/bin/env bash
set -u
fail=0
systemctl is-active --quiet mosquitto || { systemctl restart mosquitto; fail=1; }
curl -fsS --max-time 5 http://127.0.0.1:8765/health >/dev/null || { systemctl restart divera-admin; fail=1; }
if systemctl is-enabled --quiet zigbee2mqtt 2>/dev/null; then
  systemctl is-active --quiet zigbee2mqtt || { systemctl restart zigbee2mqtt; fail=1; }
fi
exit "$fail"
