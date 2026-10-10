#!/usr/bin/env bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || exit 1
VERSION="${Z2M_VERSION:-2.14.2}"
apt-get install -y curl git make g++ gcc libsystemd-dev
curl -fsSL https://deb.nodesource.com/setup_24.x | bash -
apt-get install -y nodejs
corepack enable
id zigbee2mqtt >/dev/null 2>&1 || useradd --system --home /var/lib/zigbee2mqtt --shell /usr/sbin/nologin -G dialout zigbee2mqtt
if [[ -d /opt/zigbee2mqtt/.git && -f /opt/zigbee2mqtt/package.json ]]; then
  echo "Zigbee2MQTT already installed; preserving installation and persistent state."
  install -d -o zigbee2mqtt -g zigbee2mqtt -m 0750 /var/lib/zigbee2mqtt
  install -m 0644 /opt/divera-raspi-alarm/current/services/zigbee2mqtt.service /etc/systemd/system/zigbee2mqtt.service
  systemctl daemon-reload
  exit 0
fi
[[ ! -e /opt/zigbee2mqtt ]] || { echo "Existing Zigbee2MQTT directory is not a recognized installation; refusing to overwrite." >&2; exit 1; }
rm -rf /opt/zigbee2mqtt.new
git clone --depth 1 --branch "$VERSION" https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt.new
cd /opt/zigbee2mqtt.new
corepack pnpm install --frozen-lockfile
mv /opt/zigbee2mqtt.new /opt/zigbee2mqtt
chown -R zigbee2mqtt:zigbee2mqtt /opt/zigbee2mqtt
install -d -o zigbee2mqtt -g zigbee2mqtt -m 0750 /var/lib/zigbee2mqtt
install -m 0644 /opt/divera-raspi-alarm/current/services/zigbee2mqtt.service /etc/systemd/system/zigbee2mqtt.service
systemctl daemon-reload
