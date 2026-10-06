# Implementation status

## Implemented foundation
- secret hygiene and example-only secret configuration
- typed application configuration
- local FastAPI administration service skeleton
- minimal local admin/status/health endpoints
- hardened systemd unit with automatic restart
- 64-bit OS installer preflight
- fixed PIR contract: BCM GPIO23 / physical pin 16
- Ethernet-only architecture

## Safety gates still intentionally disabled
- live DIVERA transmission until current API and recipient behavior are validated
- real smoke/test MQTT interpretation until the purchased detector is observed
- GPIO motion daemon until the production OS GPIO backend/session is pinned
- kiosk wake implementation until the production compositor/session is pinned
- Zigbee serial path until the real ZBDongle-P /dev/serial/by-id is known
- reboot escalation until functional health checks prevent reboot loops

No current placeholder can generate a real fire alarm.
