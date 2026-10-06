#!/usr/bin/env bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || { echo "Bitte mit sudo ausführen." >&2; exit 1; }
[[ "$(uname -m)" == "aarch64" ]] || { echo "Raspberry Pi OS 64-bit (aarch64) erforderlich." >&2; exit 1; }
. /etc/os-release
case "$ID" in debian|raspbian) ;; *) echo "Nicht unterstütztes OS: $PRETTY_NAME" >&2; exit 1;; esac
APP=/opt/divera-raspi-alarm
ETC=/etc/divera-raspi-alarm
STATE=/var/lib/divera-raspi-alarm
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-venv ca-certificates curl
id divera-alarm >/dev/null 2>&1 || useradd --system --home "$STATE" --shell /usr/sbin/nologin divera-alarm
install -d -m 0755 "$APP" "$ETC"
install -d -o divera-alarm -g divera-alarm -m 0750 "$STATE"
[[ -f "$APP/app/requirements.txt" ]] || { echo "Quellbaum unter $APP fehlt." >&2; exit 1; }
python3 -m venv "$APP/venv"
"$APP/venv/bin/pip" install --disable-pip-version-check --no-cache-dir -r "$APP/app/requirements.txt"
[[ -f "$ETC/config.toml" ]] || install -o root -g divera-alarm -m 0640 "$APP/config/app.example.toml" "$ETC/config.toml"
if [[ ! -f "$ETC/secrets.env" ]]; then printf '# Local secrets. Managed by UI. Never commit.\n' > "$ETC/secrets.env"; chown root:divera-alarm "$ETC/secrets.env"; chmod 0640 "$ETC/secrets.env"; fi
install -m 0644 "$APP/services/divera-admin.service" /etc/systemd/system/divera-admin.service
systemctl daemon-reload
systemctl enable --now divera-admin.service
echo "Grunddienst installiert."
