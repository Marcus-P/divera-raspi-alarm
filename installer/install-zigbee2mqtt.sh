#!/usr/bin/env bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || exit 1
apt-get install -y curl git make g++ gcc libsystemd-dev
curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
apt-get install -y nodejs
corepack enable
id zigbee2mqtt >/dev/null 2>&1 || useradd --system --home /var/lib/zigbee2mqtt --shell /usr/sbin/nologin -G dialout zigbee2mqtt
if [[ ! -d /opt/zigbee2mqtt/.git ]]; then git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt; fi
cd /opt/zigbee2mqtt
corepack pnpm install --frozen-lockfile
install -d -o zigbee2mqtt -g zigbee2mqtt -m 0750 /var/lib/zigbee2mqtt
chown -R zigbee2mqtt:zigbee2mqtt /opt/zigbee2mqtt
install -m 0644 /opt/divera-raspi-alarm/services/zigbee2mqtt.service /etc/systemd/system/zigbee2mqtt.service
systemctl daemon-reload
