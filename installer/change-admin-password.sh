#!/usr/bin/env bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || exit 1
ADMIN_FILE=/var/lib/divera-raspi-alarm/admin-user
[[ -r "$ADMIN_FILE" ]] || exit 2
ADMIN="$(cat "$ADMIN_FILE")"
TARGET="${1:-}"
[[ -n "$ADMIN" && "$TARGET" == "$ADMIN" ]] || exit 3
IFS= read -r NEWPASS
[[ ${#NEWPASS} -ge 10 ]] || { echo "password too short" >&2; exit 4; }
printf '%s:%s\n' "$TARGET" "$NEWPASS" | chpasswd
unset NEWPASS
