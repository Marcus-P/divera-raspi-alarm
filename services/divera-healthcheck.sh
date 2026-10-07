#!/usr/bin/env bash
set -u
bad=0;failed=()
restart(){ failed+=("$1");systemctl restart "$1"||true;bad=1; }
for s in mosquitto divera-admin divera-alarm;do systemctl is-active --quiet "$s"||restart "$s";done
curl -fsS --max-time 5 http://127.0.0.1:8765/health >/dev/null||restart divera-admin
if grep -q '^ZIGBEE_ADAPTER=/dev/' /etc/divera-raspi-alarm/zigbee-adapter.env 2>/dev/null;then systemctl is-active --quiet zigbee2mqtt||restart zigbee2mqtt;fi
COUNT=/run/divera-health-failures
if ((bad));then
 n=$(cat "$COUNT" 2>/dev/null||echo 0);n=$((n+1));printf '%s\n' "$n">"$COUNT"
 if [[ "$n" -eq 1 ]];then for component in "${failed[@]}";do systemctl start "divera-technical-notify@${component}.service"||true;done;fi
 read -r enabled attempts < <(python3 - <<'PY'
import tomllib
try:
 c=tomllib.load(open("/var/lib/divera-raspi-alarm/config.toml","rb"))["monitoring"]
 print(str(c.get("reboot_escalation_enabled",False)).lower(),int(c.get("service_recovery_attempts",3)))
except Exception:print("false 3")
PY
)
 if [[ "$enabled" == true && "$n" -ge "$attempts" ]];then logger -t divera-health "Recovery failed $n times; rebooting";systemctl reboot;fi
 exit 1
fi
rm -f "$COUNT";exit 0
