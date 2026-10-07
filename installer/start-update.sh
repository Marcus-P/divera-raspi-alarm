#!/usr/bin/env bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || exit 1
STAGE="${1:?}";VERSION="${2:?}";HASH="${3:?}"
[[ "$STAGE" == /var/lib/divera-raspi-alarm/updates/v* ]] || exit 2
[[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+([.-][A-Za-z0-9.-]+)?$ ]] || exit 2
[[ "$HASH" =~ ^[0-9a-fA-F]{64}$ ]] || exit 2
exec systemd-run --unit="divera-update-$VERSION" --collect /opt/divera-raspi-alarm/current/installer/apply-release.sh "$STAGE" "$VERSION" "$HASH"
