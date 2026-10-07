#!/usr/bin/env bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || { echo "Bitte mit sudo ausführen." >&2; exit 1; }
[[ "$(uname -m)" == "aarch64" ]] || { echo "Raspberry Pi OS 64-bit erforderlich." >&2; exit 1; }
. /etc/os-release; [[ "${VERSION_CODENAME:-}" == trixie ]] || echo "WARNUNG: Zielplattform ist Raspberry Pi OS Trixie."
APP=/opt/divera-raspi-alarm; ETC=/etc/divera-raspi-alarm; STATE=/var/lib/divera-raspi-alarm
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-venv python3-gpiozero ca-certificates curl git mosquitto mosquitto-clients chromium wlopm
id divera-alarm >/dev/null 2>&1 || useradd --system --home "$STATE" --shell /usr/sbin/nologin divera-alarm
install -d -m 0755 "$ETC"; install -d -o divera-alarm -g divera-alarm -m 0750 "$STATE"
python3 -m venv --system-site-packages "$APP/venv"; "$APP/venv/bin/pip" install --no-cache-dir -r "$APP/app/requirements.txt"
if [[ ! -f "$STATE/config.toml" ]]; then
 if [[ -f "$ETC/config.toml" ]]; then install -o divera-alarm -g divera-alarm -m 0640 "$ETC/config.toml" "$STATE/config.toml"; else install -o divera-alarm -g divera-alarm -m 0640 "$APP/config/app.example.toml" "$STATE/config.toml"; fi
fi
install -d -o root -g root -m 0700 /etc/credstore.encrypted
rm -f "$ETC/secrets.env"
if [[ ! -f /etc/credstore.encrypted/divera_access_key ]]; then printf "\n" | systemd-creds encrypt --name=divera_access_key - /etc/credstore.encrypted/divera_access_key; chmod 0600 /etc/credstore.encrypted/divera_access_key; fi
install -m 0644 "$APP/config/mosquitto-divera.conf" /etc/mosquitto/conf.d/divera.conf
install -m 0755 "$APP/installer/detect-zbdongle.sh" /usr/local/sbin/divera-detect-zbdongle
install -m 0755 "$APP/installer/set-credential.sh" /usr/local/sbin/divera-set-credential
chmod 0755 "$APP/services/divera-kiosk.sh" "$APP/services/divera-healthcheck.sh"
install -m 0644 "$APP/services/divera-admin.service" "$APP/services/divera-alarm.service" /etc/systemd/system/
install -m 0644 "$APP/services/divera-zigbee-detect.service" /etc/systemd/system/
install -m 0644 "$APP/services/divera-healthcheck.service" "$APP/services/divera-healthcheck.timer" /etc/systemd/system/
install -m 0644 "$APP/services/99-divera-zbdongle.rules" /etc/udev/rules.d/
install -d /etc/systemd/journald.conf.d; install -m 0644 "$APP/config/journald-divera.conf" /etc/systemd/journald.conf.d/60-divera-appliance.conf
bash "$APP/installer/install-zigbee2mqtt.sh"
bash "$APP/installer/install-kiosk.sh" "${SUDO_USER:-}"
udevadm control --reload; systemctl daemon-reload; systemctl restart systemd-journald mosquitto
systemctl enable --now mosquitto divera-admin.service divera-alarm.service divera-healthcheck.timer
/usr/local/sbin/divera-detect-zbdongle || true
systemctl enable zigbee2mqtt.service
echo "Installation abgeschlossen. Führe Selbsttest aus ..."
bash "$APP/installer/verify-install.sh"
echo "Selbsttest bestanden. Testmodus bleibt aktiv. Neustart: sudo reboot"
