#!/usr/bin/env bash
set -u
fail=0
ok(){ printf 'OK   %s\n' "$1"; }
bad(){ printf 'FAIL %s\n' "$1" >&2; fail=1; }
[[ "$(uname -m)" == aarch64 ]] && ok "64-bit OS" || bad "64-bit OS"
command -v chromium >/dev/null && ok "Chromium" || bad "Chromium"
command -v wlopm >/dev/null && ok "wlopm" || bad "wlopm"
command -v systemd-creds >/dev/null && ok "encrypted credentials" || bad "systemd-creds"
systemctl is-active --quiet mosquitto && ok "Mosquitto" || bad "Mosquitto"
systemctl is-active --quiet divera-auth.socket && ok "admin PAM socket" || bad "admin PAM socket"
admin_ready=false
for attempt in 1 2 3 4 5 6 7 8 9 10; do
 if systemctl is-active --quiet divera-admin && \
    curl -fsS --max-time 2 http://127.0.0.1:8765/health >/dev/null 2>&1 && \
    curl -fsS --max-time 2 http://127.0.0.1:8765/api/display-config >/dev/null 2>&1; then
  admin_ready=true
  break
 fi
 sleep 1
done
[[ "$admin_ready" == true ]] && ok "Admin UI + display settings" || bad "Admin UI + display settings"
systemctl is-active --quiet divera-alarm && ok "alarm worker" || bad "alarm worker"
systemctl is-enabled --quiet divera-healthcheck.timer && ok "health timer" || bad "health timer"
[[ -f /var/lib/divera-raspi-alarm/config.toml ]] && ok "persistent config" || bad "persistent config"
[[ ! -f /etc/divera-raspi-alarm/secrets.env ]] && ok "no plaintext secret store" || bad "plaintext secret store exists"
if grep -q '^ZIGBEE_ADAPTER=/dev/' /etc/divera-raspi-alarm/zigbee-adapter.env 2>/dev/null; then
 systemctl is-active --quiet zigbee2mqtt && ok "Zigbee2MQTT" || bad "Zigbee2MQTT with connected adapter"
else printf 'INFO Zigbee coordinator not connected yet\n'; fi
exit "$fail"
