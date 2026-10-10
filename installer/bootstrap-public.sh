#!/usr/bin/env bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || { echo "Bitte mit sudo ausführen." >&2; exit 1; }
SRC="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="$(tr -d '[:space:]' <"$SRC/VERSION")"
ROOT=/opt/divera-raspi-alarm
DEST="$ROOT/releases/$VERSION"
install -d -m 0755 "$ROOT/releases"
if [[ -d "$DEST" ]]; then
  echo "Reusing existing staged version $VERSION after interrupted installation."
else
  mkdir "$DEST"
  cp -a "$SRC/." "$DEST/"
fi
ln -sfn "$DEST" "$ROOT/current.new";mv -Tf "$ROOT/current.new" "$ROOT/current"
exec bash "$ROOT/current/installer/install.sh"
