#!/usr/bin/env bash
set -Eeuo pipefail
REPO_URL="${DRA_REPO_URL:-https://github.com/Marcus-P/divera-raspi-alarm.git}"
BRANCH="${DRA_BRANCH:-develop}"
APP=/opt/divera-raspi-alarm
[[ $EUID -eq 0 ]] || { echo "Bitte mit sudo ausführen." >&2; exit 1; }
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends git ca-certificates
rm -rf "$APP.new"
git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$APP.new"
rm -rf "$APP"
mv "$APP.new" "$APP"
exec "$APP/installer/install.sh"
