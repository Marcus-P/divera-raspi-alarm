#!/usr/bin/env bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || { echo "root required" >&2; exit 1; }
NAME="${1:?credential name required}"
case "$NAME" in divera_access_key|divera_system_key) ;; *) echo "unsupported credential" >&2; exit 2;; esac
install -d -m 0700 /etc/credstore.encrypted
IFS= read -r SECRET
[[ -n "$SECRET" ]] || { echo "empty credential refused" >&2; exit 3; }
printf '%s' "$SECRET" | systemd-creds encrypt --name="$NAME" - "/etc/credstore.encrypted/$NAME"
unset SECRET
chmod 0600 "/etc/credstore.encrypted/$NAME"
# Delay the web service restart so its HTTP response can complete.
systemctl try-restart divera-alarm.service
systemd-run --quiet --collect --unit="divera-admin-refresh-$(date +%s%N)" --on-active=5s /usr/bin/systemctl try-restart divera-admin.service
