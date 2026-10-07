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
systemctl is-active --quiet divera-admin && curl -fsS --max-time 5 http://127.0.0.1:8765/health >/dev/null && ok "Admin UI" || bad "Admin UI"
systemctl is-active --quiet divera-alarm && ok "alarm worker" || bad "alarm worker"
systemctl is-enabled --quiet divera-healthcheck.timer && ok "health timer" || bad "health timer"
[[ -f /etc/divera-raspi-alarm/config.toml ]] && ok "persistent config" || bad "persistent config"
[[ ! -f /etc/divera-raspi-alarm/secrets.env ]] && ok "no plaintext secret store" || bad "plaintext secret store exists"
if grep -q '^ZIGBEE_ADAPTER=/dev/' /etc/divera-raspi-alarm/zigbee-adapter.env 2>/dev/null; then
 systemctl is-active --quiet zigbee2mqtt && ok "Zigbee2MQTT" || bad "Zigbee2MQTT with connected adapter"
else printf 'INFO Zigbee coordinator not connected yet\n'; fi
exit "$fail"
