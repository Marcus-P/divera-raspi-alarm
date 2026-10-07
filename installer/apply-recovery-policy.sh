#!/usr/bin/env bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || exit 1
enabled="$(python3 - <<'PY'
import tomllib
c=tomllib.load(open("/var/lib/divera-raspi-alarm/config.toml","rb"))
print(str(c.get("monitoring",{}).get("reboot_escalation_enabled",False)).lower())
PY
)"
install -d -m 0755 /etc/systemd/system.conf.d
if [[ "$enabled" == true ]]; then
 cat >/etc/systemd/system.conf.d/60-divera-watchdog.conf <<'EOF'
[Manager]
RuntimeWatchdogSec=30s
RebootWatchdogSec=2min
EOF
else
 rm -f /etc/systemd/system.conf.d/60-divera-watchdog.conf
fi
systemctl daemon-reexec
