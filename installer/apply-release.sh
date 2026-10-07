#!/usr/bin/env bash
set -Eeuo pipefail
STAGE="${1:?stage}";VERSION="${2:?version}";EXPECTED="${3:?sha256}"
[[ "$STAGE" == /var/lib/divera-raspi-alarm/updates/v* ]] || exit 2
[[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+([.-][A-Za-z0-9.-]+)?$ ]] || exit 2
[[ "$EXPECTED" =~ ^[0-9a-fA-F]{64}$ ]] || exit 2
ARCHIVE="$STAGE/release.tar.gz";[[ -f "$ARCHIVE" ]] || exit 3
printf '%s  %s\n' "$EXPECTED" "$ARCHIVE"|sha256sum -c -
ROOT=/opt/divera-raspi-alarm;DEST="$ROOT/releases/$VERSION";PREV="$(readlink -f "$ROOT/current" 2>/dev/null||true)"
[[ ! -e "$DEST" ]] || exit 4
mkdir "$DEST"
python3 - "$ARCHIVE" "$DEST" <<'PY'
import sys,tarfile
with tarfile.open(sys.argv[1],"r:gz") as t:t.extractall(sys.argv[2],filter="data")
PY
[[ "$(tr -d '[:space:]' <"$DEST/VERSION")" == "$VERSION" ]] || { rm -rf "$DEST";exit 5; }
python3 -m venv --system-site-packages "$DEST/venv"
"$DEST/venv/bin/pip" install --no-cache-dir -r "$DEST/app/requirements.txt"
ln -sfn "$DEST" "$ROOT/current.new";mv -Tf "$ROOT/current.new" "$ROOT/current"
install -m 0644 "$DEST/services/divera-admin.service" "$DEST/services/divera-alarm.service" "$DEST/services/divera-healthcheck.service" "$DEST/services/divera-healthcheck.timer" /etc/systemd/system/
systemctl daemon-reload
systemctl restart divera-alarm divera-admin
sleep 5
if ! curl -fsS --max-time 8 http://127.0.0.1:8765/health >/dev/null;then
 if [[ -n "$PREV" ]];then ln -sfn "$PREV" "$ROOT/current.rollback";mv -Tf "$ROOT/current.rollback" "$ROOT/current";systemctl daemon-reload;systemctl restart divera-alarm divera-admin;fi
 echo "health check failed; rolled back" >&2;exit 6
fi
printf '%s\n' "$VERSION" >/var/lib/divera-raspi-alarm/last-successful-update
