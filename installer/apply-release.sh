#!/usr/bin/env bash
set -Eeuo pipefail
# Privileged backend for the web updater. It intentionally accepts only a prepared
# release directory, version and SHA-256; network access stays in the unprivileged UI.
STAGE="${1:?stage directory}"; VERSION="${2:?version}"; EXPECTED="${3:?sha256}"
[[ "$VERSION" =~ ^v?[0-9]+\.[0-9]+\.[0-9]+([.-][A-Za-z0-9.-]+)?$ ]] || { echo "invalid version" >&2; exit 2; }
ARCHIVE="$STAGE/release.tar.gz"; [[ -f "$ARCHIVE" ]] || exit 3
printf '%s  %s\n' "$EXPECTED" "$ARCHIVE" | sha256sum -c -
ROOT=/opt/divera-raspi-alarm; DEST="$ROOT/releases/$VERSION"; PREV="$(readlink -f "$ROOT/current" 2>/dev/null || true)"
install -d -m 0755 "$ROOT/releases"; [[ ! -e "$DEST" ]] || { echo "version already installed" >&2; exit 4; }
mkdir "$DEST"; tar --no-same-owner --no-same-permissions -xzf "$ARCHIVE" -C "$DEST"
ln -sfn "$DEST" "$ROOT/current.new"; mv -Tf "$ROOT/current.new" "$ROOT/current"
systemctl daemon-reload
systemctl restart divera-admin divera-alarm
sleep 3
if ! curl -fsS --max-time 8 http://127.0.0.1:8765/health >/dev/null; then
 [[ -n "$PREV" ]] && { ln -sfn "$PREV" "$ROOT/current.rollback"; mv -Tf "$ROOT/current.rollback" "$ROOT/current"; systemctl restart divera-admin divera-alarm; }
 echo "health check failed; rolled back" >&2; exit 5
fi
