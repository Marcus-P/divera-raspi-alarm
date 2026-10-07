#!/usr/bin/env bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || { echo "root required" >&2; exit 1; }
NAME="${1:?credential name required}"
case "$NAME" in divera_access_key) ;; *) echo "unsupported credential" >&2; exit 2;; esac
install -d -m 0700 /etc/credstore.encrypted
TMP="$(mktemp -p /run divera-credential.XXXXXX)"; trap 'rm -f "$TMP"' EXIT
umask 077
cat >"$TMP"
[[ -s "$TMP" ]] || { echo "empty credential refused" >&2; exit 3; }
systemd-creds encrypt --name="$NAME" "$TMP" "/etc/credstore.encrypted/$NAME"
chmod 0600 "/etc/credstore.encrypted/$NAME"
systemctl try-restart divera-admin.service divera-alarm.service || true
