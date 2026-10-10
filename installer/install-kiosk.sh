#!/usr/bin/env bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || exit 1
U="${SUDO_USER:-${1:-}}"; [[ -n "$U" && "$U" != root ]] || { echo "Kiosk-Benutzer fehlt" >&2; exit 1; }
H="$(getent passwd "$U"|cut -d: -f6)"; install -d -o "$U" -g "$U" "$H/.config/labwc"
cat >"$H/.config/labwc/autostart" <<EOF
(sleep 8; systemd-cat -t divera-kiosk /opt/divera-raspi-alarm/current/services/divera-kiosk.sh) &
systemd-cat -t divera-display-motion /opt/divera-raspi-alarm/current/venv/bin/python /opt/divera-raspi-alarm/current/services/display-motion.py &
EOF
chown "$U:$U" "$H/.config/labwc/autostart"
raspi-config nonint do_boot_behaviour B4 || true
