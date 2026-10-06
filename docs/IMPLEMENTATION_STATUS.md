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


## First-install progress
- automatic ZBDongle-P/CP210x discovery via stable /dev/serial/by-id
- hotplug discovery trigger and Zigbee2MQTT restart hook
- Mosquitto package included in base installer
- bounded journald configuration included
- Zigbee2MQTT configuration template uses zstack, local MQTT, availability, frontend and console-only logging
- public-repository bootstrap script prepared, but the current private repository still needs an authenticated/published bootstrap path before giving the user the final fresh-SD install command

## Still required before the promised installation hand-off
- install/pin Zigbee2MQTT itself and wire detected adapter into its generated configuration
- implement production kiosk startup for the pinned Raspberry Pi OS compositor
- implement GPIO23 display wake on that compositor
- implement usable first-run UI flows (DIVERA key, personnel/test recipients, schedule, pairing)
- implement DIVERA client with the Test-mode recipient guard
- implement password-change privileged helper safely
- add service functional health checks and initial recovery policies
- finalize private-repository bootstrap strategy
